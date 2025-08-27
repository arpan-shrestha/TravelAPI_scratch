from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('refresh-token/', views.refresh_token_view, name='refresh_token'),
]
