from .models import Services
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from auth_app.utils import token_required


# Create your views here.

def services(request):
    services_list = list(Services.objects.values(
        'id', 'title', 'description', 'details_url'
    ))   
    return JsonResponse({'services':services_list})


def fetch_service_details(request, service_id):
    try:
        service = Services.objects.get(id=service_id)
    except Services.DoesNotExist:
        return JsonResponse({"error": "Details not found"}, status=404)
    details_data = {
        "title": service.title,
        "description": service.description,
        "details_url": service.details_url,
        "content": service.content 
    }
    return JsonResponse(details_data)

@csrf_exempt
@token_required
def add_service(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            service = Services.objects.create(
                title=data.get('title',''),
                description=data.get('description',''),
                details_url=data.get('details_url',''),
                content = data.get('content','')
            )
            return JsonResponse({'success':True,'id':service.id})
        except Exception as e:
            return JsonResponse({'success':False, 'error':str(e)}, status=400)
    return JsonResponse({'error':'POST MEthod is required'}, status=405)

@csrf_exempt
def update_service(request, service_id):
    if request.method in ['PUT', 'PATCH']:
        try:
            service = Services.objects.get(id=service_id)
            data = json.loads(request.body)
            
            service.title = data.get('title',service.title)
            service.description = data.get('description',service.description)
            service.details_url = data.get('details_url',service.details_url)
            service.content = data.get('content',service.content)
            service.save()
            return JsonResponse({'success':True})
        except Services.DoesNotExist:
            return JsonResponse({'error':'Services not Found'}, status=400)
    return JsonResponse({'error':'Check your Method'}, status=405)

@csrf_exempt
@token_required
def delete_service(request, service_id):
    if request.method == 'DELETE':
        try:
            service = Services.objects.get(id=service_id)
            service.delete()
            return JsonResponse({'success':True})
        except Services.DoesNotExist:
            return JsonResponse({'error':'Services not found'},status=400)
    return JsonResponse({'error':'Check your Method'}, status=405)