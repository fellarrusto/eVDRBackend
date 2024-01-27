from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from ..models import AuthorizedPhoneNumber, Chat, UserMessage, UserStats
import json

@require_http_methods(["GET"])
def chat_ids(request):
    authenticated_chats = Chat.objects.filter(authorization_flag=True).values_list('chat_id', 'phone_number')
    return JsonResponse({'authenticated_chats': list(authenticated_chats)})


@require_http_methods(["GET"])
def chat_messages(request):
    chat_id = request.GET.get('chat_id', None)
    if chat_id is None:
        return JsonResponse({'reply': 'Chat ID is required'}, status=400)

    try:
        chat = Chat.objects.get(chat_id=chat_id)
        messages = UserMessage.objects.filter(chat=chat).values('message', 'timestamp')
        return JsonResponse({'messages': list(messages)})
    except Chat.DoesNotExist:
        return JsonResponse({'reply': 'Chat ID not found'}, status=404)
    

@require_http_methods(["GET"])
def chat_score(request):
    chat_id = request.GET.get('chat_id', None)
    if chat_id is None:
        return JsonResponse({'reply': 'Chat ID is required'}, status=400)

    try:
        user_stats = UserStats.objects.get(chat__chat_id=chat_id)
        score = user_stats.score
        return JsonResponse({'score': score})
    except UserStats.DoesNotExist:
        return JsonResponse({'reply': 'UserStats for the given Chat ID not found'}, status=404)
    except Chat.DoesNotExist:
        return JsonResponse({'reply': 'Chat ID not found'}, status=404)
    
@require_http_methods(["GET"])
def all_chats_scores(request):
    try:
        # Fetch all UserStats entries and related Chat information, ordered by score in descending order
        user_stats = UserStats.objects.select_related('chat').order_by('-score').values('chat__chat_id', 'chat__phone_number', 'score')

        # Create a list of dictionaries, each representing a chat with its score
        chats_scores = [
            {'chat_id': stat['chat__chat_id'], 'phone_number': stat['chat__phone_number'], 'score': stat['score']}
            for stat in user_stats
        ]

        return JsonResponse({'chats_scores': chats_scores})
    except ObjectDoesNotExist:
        return JsonResponse({'reply': 'Error retrieving chats and scores'}, status=500)
    
@csrf_exempt
@require_http_methods(["POST"])
def upload_phone_numbers(request):
    # Check if there is a file in the request
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)

    file = request.FILES['file']
    success_count = 0
    error_count = 0

    # Read file line by line
    for line in file:
        phone_number = line.strip().decode('utf-8')
        # Validate and save phone number
        if phone_number and len(phone_number) <= 15:
            try:
                AuthorizedPhoneNumber.objects.create(phone_number=phone_number)
                success_count += 1
            except Exception as e:
                # Handle errors (e.g., duplicate number)
                error_count += 1

    return JsonResponse({'success': success_count, 'errors': error_count})
