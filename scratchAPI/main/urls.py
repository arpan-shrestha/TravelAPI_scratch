from django.urls import path
from . import views

urlpatterns = [
    path('domestic-destinations/', views.fetch_domestic_trips, name='fetch_domestic_trips'),
    path('international-destinations/',views.fetch_international_trips,name='fetch_international_trips'),
]