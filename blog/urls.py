from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    # path('<int:blog_id>/', views.fetch_blog_details, name='fetch_blog_details'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('<int:blog_id>/update/', views.update_blog),
    path('<int:blog_id>/delete/', views.delete_blog),
]