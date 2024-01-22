from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from ..models import AuthorizedPhoneNumber, Chat, UserMessage
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
