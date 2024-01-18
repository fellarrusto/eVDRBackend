from django.http import HttpResponse

def ready(request):
    return HttpResponse("App is ready", status=200)
