from django.http import JsonResponse
from django.utils import timezone
from .models import UserProfile
from auth_app.models import AuthToken

class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip authentication for public endpoints
        public_paths = ['/auth/login/', '/auth/refresh-token/', '/admin/']
        if any(request.path.startswith(path) for path in public_paths):
            return self.get_response(request)

        # Check for token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"error": "Token required"}, status=401)
            
        token = auth_header.split(" ")[1]
        
        # Validate token
        try:
            auth_token = AuthToken.objects.get(access_token=token, is_active=True)
            if auth_token.access_token_expire < timezone.now():
                return JsonResponse({'error': 'Token expired'}, status=401)
        except AuthToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid token'}, status=401)
            
        # Set user and role in request
        request.user = auth_token.user
        try:
            profile = UserProfile.objects.get(user=auth_token.user)
            request.user_role = profile.role.role  # Get role name as string
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=404)
        
        # Simple role-based access control
        if not self.check_access(request, profile.role.role):
            return JsonResponse({'error': 'Access denied'}, status=403)
        
        return self.get_response(request)
    
    def check_access(self, request, user_role):
        """Simple role-based access control"""
        method = request.method
        path = request.path
        
        # Admin can do everything
        if user_role == 'admin':
            return True
        
        # Editor can read and create/update, but not delete
        if user_role == 'editor':
            if method == 'DELETE':
                return False
            return True
        
        # Viewer can only read
        if user_role == 'viewer':
            return method == 'GET'
        
        # Default: deny access
        return False
        
