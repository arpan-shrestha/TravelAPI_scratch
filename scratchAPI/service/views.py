from .models import Services
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Create your views here.

def services(request):
    url = "https://www.antholidays.com/services"
    services_list = []
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
    services_list = list(Services.objects.values())
    return JsonResponse({'services':services_list})