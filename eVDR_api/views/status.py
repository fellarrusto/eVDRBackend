from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from eVDR_api.models import Chat

def ready(request):
    return HttpResponse("App is ready", status=200)

@csrf_exempt  
@require_http_methods(["POST"])  # Restrict this view to POST requests only
def reset_chat_table(request):

    # Delete all records in the Chat table
    Chat.objects.all().delete()

    return JsonResponse({'status': 'success', 'message': 'Chat table reset to original state'})

