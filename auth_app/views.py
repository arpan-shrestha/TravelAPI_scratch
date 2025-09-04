import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.timezone import make_aware
from .models import AuthToken
from .utils import generate_token
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Create your views here.

@csrf_exempt
def login_view(request):
    if request.method !='POST':
        return JsonResponse({'error':'POST Method Required'},status=405)
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)

    if not user:
        return JsonResponse({'error':'Invalid username or password'}, status=401)
    
    AuthToken.objects.filter(user=user,is_active=True).update(is_active=False)
    tokens = generate_token(user, with_refresh=True)

    AuthToken.objects.create(
        user=user,
        access_token=tokens['access_token'],
        refresh_token=tokens['refresh_token'],
        access_token_expire=make_aware(tokens['access_token_expire']),
        refresh_token_expire=make_aware(tokens['refresh_token_expire']),
        is_active=True,
    )

    return JsonResponse({
        'access_token': tokens['access_token'],
        'refresh_token': tokens['refresh_token'],
        'access_token_expire':tokens['access_token_expire'].isoformat(),
        'refresh_token_expire':tokens['refresh_token_expire'].isoformat(),
    })


@csrf_exempt
def refresh_token_view(request):
    if request.method != 'POST':
        return JsonResponse({'error':'POST Method required'}, status=405)
    data = json.loads(request.body)
    refresh_token = data.get('refresh_token')
    try:
        token_obj = AuthToken.objects.get(refresh_token=refresh_token, is_active=True)
    except AuthToken.DoesNotExist:
        return JsonResponse({'error':'Invalid refresh token'}, status=401)
    
    if token_obj.refresh_token_expire < timezone.now():
        token_obj.is_active =False
        token_obj.save()
        return JsonResponse({'error':'Refresh token expired'}, status=401)
    
 
    tokens = generate_token(token_obj.user, with_refresh=False)
    
    token_obj.access_token = tokens['access_token']
    token_obj.access_token_expire = make_aware(tokens['access_token_expire'])


    token_obj.save(
        update_fields=[
            'access_token',
            'access_token_expire',
        ]
    )
    return JsonResponse({
        'access_token':tokens['access_token'],
        'refresh_token':token_obj.refresh_token,
        'access_token_expire':tokens['access_token_expire'].isoformat(),
        'refresh_token_expire':token_obj.refresh_token_expire.isoformat(),
    })


@csrf_exempt
def logout_view(request):
    if request.method != 'POST':
        return JsonResponse({'error':'POST Method Required'},status=405)
    data = json.loads(request.body)
    access_token=data.get('access_token')
    if not access_token:
        return JsonResponse({'error':'Access token required'},status=400)
    try:
        token_obj=AuthToken.objects.get(access_token=access_token, is_active=True)
    except AuthToken.DoesNotExist:
        return JsonResponse({'error':'Invalid access tokem'}, status=401)
    
    token_obj.is_active=False
    token_obj.save(update_fields=['is_active'])
    return JsonResponse({'msg':'Logged out'})


