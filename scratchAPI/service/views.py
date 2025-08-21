from .models import Services
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

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

            Services.objects.get_or_create(
                title=title,
                description=description,
            )
    services_list = list(Services.objects.values())
    return JsonResponse({'services':services_list})