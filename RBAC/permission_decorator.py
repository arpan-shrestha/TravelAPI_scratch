from django.http import JsonResponse
from .models import UserProfile, RolePermission, Permission
from auth_app.models import AuthToken
from django.utils import timezone

def permission_required(permission_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({'error':'Unauthorized'}, status=401)
            token = auth_header.split(" ")[1]
            try:
                auth_token=AuthToken.objects.get(access_token=token, is_active=True)
            except AuthToken.DoesNotExist:
                return JsonResponse({'error':'Invalid or Expired Token'},status=401)
            if auth_token.access_token_expire < timezone.now():
                return JsonResponse({'error':'Access Token Expired'}, status=401)
            request.user = auth_token.user

            profile = UserProfile.objects.get(user=auth_token.user)
            if not RolePermission.objects.filter(role=profile.role,permission__name=permission_name).exists():
                return JsonResponse({'error':'Permission Denied'},status=403)
            return view_func(request, *args,**kwargs)
        return wrapper
    return decorator
