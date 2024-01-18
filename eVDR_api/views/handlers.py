from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from eVDR_api.models import AuthorizedPhoneNumber, Chat

@csrf_exempt
@require_http_methods(["POST"])
def indizio(request):
    # Parse the incoming JSON data from the request body
    try:
        data = json.loads(request.body)
        chat_id = data.get('chat_id')
    except json.JSONDecodeError:
        return JsonResponse({'reply': 'Invalid JSON'}, status=400)
    
    # Check if chat_id is provided
    if chat_id is None:
        return JsonResponse({'reply': 'Chat ID is required'}, status=400)
    
    # Query the Chat model to check authorization
    try:
        chat = Chat.objects.get(chat_id=chat_id)
        if not chat.authorization_flag:
            return JsonResponse({'reply': 'Unauthorized'}, status=401)
    except Chat.DoesNotExist:
        return JsonResponse({'reply': 'Chat ID not found'}, status=401)
    
    # Example URL. Replace with your actual logic to generate or fetch the URL
    indizio_url = "http://www.corsarineri.it/training2023/indizio07.png"
    return JsonResponse({"url": indizio_url}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def conversation(request):
    # Parse the incoming JSON data from the request body
    try:
        data = json.loads(request.body)
        message = data.get('message')
        chat_id = data.get('chat_id')
    except json.JSONDecodeError:
        return JsonResponse({'reply': 'Invalid JSON'}, status=400)

    # Check if chat_id is provided
    if chat_id is None:
        return JsonResponse({'reply': 'Chat ID is required'}, status=400)

    # Query the Chat model to check authorization
    try:
        chat = Chat.objects.get(chat_id=chat_id)
        if not chat.authorization_flag:
            return JsonResponse({'reply': 'Unauthorized'}, status=401)
    except Chat.DoesNotExist:
        return JsonResponse({'reply': 'Chat ID not found'}, status=401)

    # Check if the message is not empty
    if message:
        # Proceed with the conversation
        return JsonResponse({'reply': f"Mi hai scritto: {message}, il tuo ChatID è {chat_id}"})
    else:
        # If no message was provided in the request, return an error message
        return JsonResponse({'reply': 'No message received'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def auth(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            phone_number = data.get('phone_number')
            chat_id = data.get('chat_id')

            # Check if chat_id exists in Chat table
            try:
                chat = Chat.objects.get(chat_id=chat_id)
                if chat.authorization_flag:
                    return JsonResponse({'success': True})
                else:
                    # Check if phone_number is authorized
                    if AuthorizedPhoneNumber.objects.filter(phone_number=phone_number).exists():
                        chat.authorization_flag = True
                        chat.save()
                        return JsonResponse({'success': True})
            except Chat.DoesNotExist:
                # If chat_id does not exist, check if phone_number is authorized
                if AuthorizedPhoneNumber.objects.filter(phone_number=phone_number).exists():
                    Chat.objects.create(chat_id=chat_id, phone_number=phone_number, authorization_flag=True)
                    return JsonResponse({'success': True})

            return JsonResponse({'success': False})

@csrf_exempt  
@require_http_methods(["POST"])  # Restrict this view to POST requests only
def reset_chat_table(request):

    # Delete all records in the Chat table
    Chat.objects.all().delete()

    return JsonResponse({'status': 'success', 'message': 'Chat table reset to original state'})