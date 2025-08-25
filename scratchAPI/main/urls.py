from django.urls import path
from . import views

urlpatterns = [
    path('domestic-destinations/', views.fetch_domestic_trips, name='fetch_domestic_trips'),
    path('domestic-destinations/<int:trip_id>/', views.fetch_domestic_trip_details, name='fetch_domestic_trip_details'),
    path('add_domestic_trip/', views.add_domestic_trip, name='add_domestic_trip'),
    path('domestic-destinations/<int:trip_id>/update/', views.update_domestic_trip),
    path('domestic-destinations/<int:trip_id>/delete/', views.delete_domestic_trip),

    path('international-destinations/',views.fetch_international_trips,name='fetch_international_trips'),
    path('international-destinations/<int:trip_id>/', views.fetch_international_trip_details, name='fetch_domestic_trip_details'),
    path('add_international_trip/', views.add_international_trip, name='add_international_trip'),
    path('domestic-destinations/<int:trip_id>/update/', views.update_domestic_trip),
    path('international-destinations/<int:trip_id>/delete/', views.delete_international_trip),

]