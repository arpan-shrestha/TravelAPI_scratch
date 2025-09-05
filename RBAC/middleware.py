from django.http import JsonResponse
from django.utils import timezone
from .models import UserProfile
from auth_app.models import AuthToken

class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        access_path = ['/auth/login/','/auth/refresh-token/']
        if request.path in access_path:
            return self.get_response(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error":"Unauthorized"},status=401)
        token = auth_header.split(" ")[1]
        try:
            auth_token = AuthToken.objects.get(access_token=token, is_active=True)
        except AuthToken.DoesNotExist:
            return JsonResponse({'error':'Invalid token or expired token'}, status=401)
        if auth_token.access_token_expire < timezone.now():
            return JsonResponse({'error':'Token Expired'}, status=401)
            
        request.user = auth_token.user
        try:
            profile = UserProfile.objects.get(user=auth_token.user)
            request.user_role = profile.role
        except UserProfile.DoesNotExist:
            return JsonResponse({'error':'User profile not found'}, status=404)
        
        response = self.get_response(request)
        return response
        
