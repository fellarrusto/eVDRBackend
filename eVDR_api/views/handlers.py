from django.http import JsonResponse

def indizio(request):
    # Example URL. Replace with your actual logic to generate or fetch the URL
    indizio_url = "http://www.corsarineri.it/training2023/indizio07.png"
    return JsonResponse({"url": indizio_url}, status=200)
