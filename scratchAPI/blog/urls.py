from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('<int:blog_id>/', views.fetch_blog_details, name='fetch_blog_details'),
]