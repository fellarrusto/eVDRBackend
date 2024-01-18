from django.http import JsonResponse
import json

def indizio(request):
    # Example URL. Replace with your actual logic to generate or fetch the URL
    indizio_url = "http://www.corsarineri.it/training2023/indizio07.png"
    return JsonResponse({"url": indizio_url}, status=200)

def conversation(request):
    # Parse the incoming JSON data from the request body
    try:
        data = json.loads(request.body)
        message = data.get('message')
    except json.JSONDecodeError:
        return JsonResponse({'reply': 'Invalid JSON'}, status=400)

    # Check if the message is not empty
    if message:
        # Simply echo the message back
        return JsonResponse({'reply': f"Mi hai scritto: {message}"})
    else:
        # If no message was provided in the request, return an error message
        return JsonResponse({'reply': 'No message received'}, status=400)

