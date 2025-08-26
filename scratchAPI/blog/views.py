from django.shortcuts import render
from django.http import JsonResponse
from .models import Blog
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def blogs(request):
    blog_list = list(Blog.objects.values(
        'id','title','description','details_url','published_date'
    ))
    return JsonResponse({'Blog':blog_list})


@csrf_exempt
def add_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            blog = Blog.objects.create(
                title = data.get('title',''),
                description = data.get('description',''),
                details_url = data.get('details_url',''),
                published_date = data.get('published_date',''),
                content = data.get('content','')
            )
            return JsonResponse({'success':True,'id':blog.id})
        except Exception as e:
            return JsonResponse({'success':False,'error':str(e)}, status=400)
    return JsonResponse({'error':'POST Method is required'}, status=405)

@csrf_exempt
def update_blog(request, blog_id):
    if request.method in ['PATCH','PUT']:
        try:
            blog = Blog.objects.get(id=blog_id)
            data = json.loads(request.body)

            blog.title = data.get('title','')
            blog.description = data.get('description','')
            blog.details_url = data.get('details_url','')
            blog.published_date = data.get('published_date','')
            blog.content = data.get('content','')
            blog.save()
            return JsonResponse({
                'success':True
            })
        except Blog.DoesNotExist:
            return JsonResponse({'error':'Blog not found'}, status=400)
    return JsonResponse({'error':'Check Your Method'}, status=405)

@csrf_exempt
def delete_blog(request, blog_id):
    if request.method == 'DELETE':
        try:
            blog = Blog.objects.get(id=blog_id)
            blog.delete()
            return JsonResponse({
                'success':True
            })
        except Blog.DoesNotExist:
            return JsonResponse({
                'error':'Blog not found'
            },status=400)
    return JsonResponse({
        'error':'Check your Method'
    }, status=405)

