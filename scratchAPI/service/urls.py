from django.urls import path
from . import views

urlpatterns = [
    path('', views.services, name='services'),
    path('<int:service_id>/', views.fetch_service_details, name='fetch_service_details'),
    path('add_service/', views.add_service, name='add_service'),
    path('<int:service_id>/update/', views.update_service),
    path('<int:service_id>/delete/', views.delete_service),
]