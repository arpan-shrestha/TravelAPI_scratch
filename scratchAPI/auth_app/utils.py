from django.shortcuts import render
import secrets, datetime
from django.utils import timezone
from django.http import JsonResponse
from .models import AuthToken

def generate_token(user, with_refresh=True):
    access_token = secrets.token_urlsafe(32)
    now = datetime.datetime.now()
    access_token_expire = now + datetime.timedelta(hours=1)

    token_data = {
        "access_token":access_token,
        "access_token_expire":access_token_expire,    
    }

    if with_refresh:
        refresh_token = secrets.token_urlsafe(32)
        refresh_token_expire = now +datetime.timedelta(days=15)
        token_data.update({
            "refresh_token":refresh_token,
            "refresh_token_expire":refresh_token_expire,
        })
    return token_data

def token_required(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({'error':'Unauthorized'}, status=401)
        token = auth_header.split(" ")[1]
        try:
            auth_token = AuthToken.objects.get(access_token=token, is_active=True)
        except AuthToken.DoesNotExist:
            return JsonResponse({'error':'Invalid or expired token'}, status=401)
        
        if auth_token.access_token_expire < timezone.now():
            return JsonResponse({'error':'Access token expired'}, status=401)
        
        request.user = auth_token.user
        return view_func(request, *args, **kwargs)
    return wrapper 
