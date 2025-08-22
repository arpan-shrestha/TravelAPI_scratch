from .models import Services
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import urllib.parse
from django.views.decorators.csrf import csrf_exempt
import json


# Create your views here.

def services(request):
    services_list = list(Services.objects.values('id', 'title', 'description', 'details_url'))
    if not services_list:
        url = "https://www.antholidays.com/services"
        try:
            response = requests.get(url)
            if response.status_code ==200:
                soup = BeautifulSoup(response.content, 'html.parser')
                items = soup.select('div.hover\\:shadow-lg.border')
                for item in items:
                    title = item.find('h2').text.strip() if item.find('h2') else 'No Title'
                    description = item.find('p').text.strip() if item.find('p') else 'No Description'
                    a_tag = item.find('a', href=True)
                    details_url = a_tag['href'] if a_tag else None
                    if details_url:
                        details_url = urllib.parse.urljoin("https://www.antholidays.com", details_url)
                        Services.objects.get_or_create(
                            title=title,
                            defaults={
                                "description":description,
                                "details_url":details_url
                            }
)
            services_list = list(Services.objects.values('id', 'title', 'description', 'details_url'))
        except Exception as e:
            return JsonResponse({"error":"Could not fetch website, and no data in DB.","details":str(e)}, status=500)    
    return JsonResponse({'services':services_list})


def fetch_service_details(request, service_id):
    try:
        service = Services.objects.get(id=service_id)
    except Services.DoesNotExist:
        return JsonResponse({"error":"Details not found"}, status=404)
    details_data = {
        "title":service.title,
        "description":service.description,
        "details_url":service.details_url
    }
    if service.details_url:
        response = requests.get(service.details_url)
        if response.status_code==200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.select_one('div.ckEditor.blog') 
            service.content = content.get_text(strip=True) if content else ""
            service.save()

            details_data.update({
                "content":service.content
            })
        else:
            details_data["error"] = "Unable to fetch details"
    else:
        details_data["error"] = "No details URL provided"
    return JsonResponse(details_data)


@csrf_exempt
def add_service(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            service = Services.objects.create(
                title=data.get('title',''),
                description=data.get('description',''),
                details_url=data.get('details_url',''),
            )
            return JsonResponse({'success':True,'id':service.id})
        except Exception as e:
            return JsonResponse({'success':False, 'error':str(e)}, status=400)
    return JsonResponse({'error':'POST MEthod is required'}, status=405)