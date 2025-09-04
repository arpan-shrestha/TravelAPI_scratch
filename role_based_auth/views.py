from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
import json
# Create your views here.

@csrf_exempt
def update_role(request):
    if request.method != "POST":
        return JsonResponse({'error':'POST Method Required'},status=405)
    data = json.loads(request.body)
    new_role = data.get('role')

    if new_role not in dict(CustomUser.ROLE_CHOICES).keus():
        return JsonResponse({'error':'Invalid role'}, status=400)
    try:
        user = CustomUser.objects.get(id= user.id)
        user.role = new_role
        user.save()
        return JsonResponse({'message':f'Role updated to {new_role}'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'error':'User not found'}, status=404)
    