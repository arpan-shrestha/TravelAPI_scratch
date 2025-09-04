from django.http import JsonResponse
from .models import UserProfile
from auth_app.models import AuthToken
from django.utils import timezone

def token_required(required_role=None):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({'error':'Unauthorized'},status=401)
            
            token = auth_header.split(" ")[1]
            try:
                auth_token = AuthToken.objects.get(access_token=token, is_active=True)
            except AuthToken.DoesNotexist:
                return JsonResponse({'error':'Invalid or expired token'}, status=401)
            
            if auth_token.access_token_expire < timezone.now():
                return JsonResponse({'error':'Access Token expired'}, status=401)
            request.user = auth_token.user

            if required_role:
                profile = UserProfile.objects.get(user=auth_token.user)
                if profile.role != required_role:
                    return JsonResponse({'error':'Permission denied'}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator