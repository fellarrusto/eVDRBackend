from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ..models import Indizi, SystemDescription
import json

@csrf_exempt
@require_http_methods(["POST"])
def create_indizio(request):
    # Parse the incoming JSON data from the request body
    try:
        data = json.loads(request.body)
        path = data.get('path')
        solution = data.get('solution')
    except json.JSONDecodeError:
        return JsonResponse({'reply': 'Invalid JSON'}, status=400)

    # Check if both path and solution are provided
    if not path or not solution:
        return JsonResponse({'reply': 'Both path and solution are required'}, status=400)

    # Create and save the new Indizi object
    new_indizio = Indizi.objects.create(path=path, solution=solution)

    return JsonResponse({'reply': f'Indizio created with ID {new_indizio.id}'})


@csrf_exempt
@require_http_methods(["POST"])
def update_system_description(request):
    # Parse the incoming JSON data from the request body
    try:
        data = json.loads(request.body)
        description = data.get('description')
    except json.JSONDecodeError:
        return JsonResponse({'reply': 'Invalid JSON'}, status=400)

    # Check if description is provided
    if not description:
        return JsonResponse({'reply': 'Description is required'}, status=400)

    # Retrieve the latest SystemDescription or create a new one if none exists
    system_desc, created = SystemDescription.objects.get_or_create(
        id=1,  # Assuming we want to keep updating the same record
        defaults={'description': description}
    )

    # If the record was not newly created, update its description
    if not created:
        system_desc.description = description
        system_desc.save()

    action = "created" if created else "updated"
    return JsonResponse({'reply': f'System description {action} successfully'})