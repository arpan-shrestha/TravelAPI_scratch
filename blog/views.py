from django.shortcuts import render
from django.http import JsonResponse
from .models import Blog
from django.views.decorators.csrf import csrf_exempt
import json
from RBAC.permission_decorator import permission_required
# Create your views here.

@permission_required("view_blog")
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

# def fetch_blog_details(request, blog_id):
#     try:
#         blog = Blog.objects.get(id=blog_id)
#     except Blog.DoesNotExist:
#         return JsonResponse({"error":"Details not found"}, status=404)
#     details_data = {
#         "title":blog.title,
#         "description":blog.description,
#         "details_url":blog.details_url,
#         "published_date":blog.published_date
#     }
#     if blog.details_url:
#         response = requests.get(blog.details_url)
#         if response.status_code ==200:
#             soup = BeautifulSoup(response.content, 'html.parser')
#             content = soup.select_one('div.ckEditor.blog')
#             # blog.content = content.get_text(strip=True) if content else ""
#             if content:
#                 # Split content by h2 and h3 headings to structure it
#                 structured_content = []
#                 for element in content.find_all(["h2", "h3", "p", "ul"]):
#                     if element.name in ["h2", "h3"]:
#                         structured_content.append({"heading": element.get_text(strip=True), "content": []})
#                     elif element.name == "p":
#                         if structured_content:
#                             structured_content[-1]["content"].append(element.get_text(strip=True))
#                         else:
#                             structured_content.append({"heading": None, "content": [element.get_text(strip=True)]})
#                     elif element.name == "ul":
#                         items = [li.get_text(strip=True) for li in element.find_all("li")]
#                         if structured_content:
#                             structured_content[-1]["content"].extend(items)
#                         else:
#                             structured_content.append({"heading": None, "content": items})

#                 blog.content = structured_content
#                 blog.save()

#             details_data.update({
#                 "content":blog.content
#             })
#         else:
#             details_data["error"] = "Unable to fetch details"
#     else:
#         details_data["error"] = "No details URL provided"
#     return JsonResponse(details_data)