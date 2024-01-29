from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
import json

from eVDR_api.models import AuthorizedPhoneNumber, Chat, Indizi, UserMessage, UserStats

from ..logic import messages



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
    
    # Get the latest Indizi record
    try:
        latest_indizio = Indizi.objects.latest('id')  # Assuming 'id' as the field to determine the latest
        indizio_url = latest_indizio.path
    except Indizi.DoesNotExist:
        return JsonResponse({'reply': 'No indizi found'}, status=404)

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
    
    # Store message

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
        # Save conversation
        UserMessage.objects.create(chat=chat, message="user:" + message)
        answer = handle_message(message, chat_id)
        # Check if answer is not None
        if answer is not None:
            UserMessage.objects.create(chat=chat, message="bot:" + answer)
            return JsonResponse({'reply': answer})
        else:
            return JsonResponse({'reply': 'Bot not available'}, status=400)
    else:
        # If no message was provided in the request, return an error message
        return JsonResponse({'reply': 'No message received'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def auth(request):
    if request.method == 'POST':
            data = json.loads(request.body)
            phone_number = clean_phone_number(data.get('phone_number'))
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

# Utils

def clean_phone_number(phone_number):
    # Remove all spaces
    phone_number = phone_number.replace(" ", "")

    # Check if the phone number starts with '+39' and remove it
    if phone_number.startswith('+39'):
        phone_number = phone_number[3:]

    return phone_number

def handle_message(msg, chat_id):
    msg_lower = msg.lower()

    if msg_lower.startswith("proposta soluzione"):
        res = messages.evaluate_vdr(msg)
        if(res.lower().startswith("soluzione corretta")):
            if(update_user_stats(chat_id)):
                return "Soluzione corretta!"
            else:
                return "Soluzione corretta, ma forse questo indizio l'avevi già risolto. In ogni caso il punto ti è già stato assegnato. Grazie....Gombilmendi"
        return res
    else:
        return f"Per richiedere un VDR è necessario scrivere un messaggio che comincia con \"Proposta soluzione:\", ecco un esempio:\n\nProposta soluzione:\n\nL'indizio della settimana ha una soluzione e questa soluzione porta a Crapolla."
    

def update_user_stats(chat_id):
    # Get the latest Indizi ID
    latest_indizi_id = Indizi.objects.aggregate(Max('id'))['id__max']

    # Try to retrieve the UserStats object for the given chat_id
    try:
        user_stats = UserStats.objects.get(chat__chat_id=chat_id)

        # Check if the latest puzzle solved is different
        if user_stats.latest_puzzle_solved != latest_indizi_id:
            user_stats.score += 1
            user_stats.latest_puzzle_solved = latest_indizi_id
            user_stats.save()
            return True  # Score updated
        else:
            return False  # Score not updated, puzzle already solved

    except UserStats.DoesNotExist:
        # Fetch the Chat object
        try:
            chat = Chat.objects.get(chat_id=chat_id)
        except Chat.DoesNotExist:
            # Handle the case where the Chat object does not exist
            return {'error': 'Chat object does not exist for this chat_id'}

        # Create a new UserStats object if it doesn't exist
        user_stats = UserStats.objects.create(
            chat=chat,
            score=1,
            latest_puzzle_solved=latest_indizi_id
        )
        return True  # New UserStats created and score initialized
