from .models import DomesticTrip, InternationalTrip
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

def fetch_domestic_trips(request):
    url = "https://www.antholidays.com/destination-domestic/"
    domestic_destinations=[]
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.select('div.hover\\:shadow-lg.border')

        for item in items:
            title = item.find('h2').text.strip() if item.find('h2') else 'No Title'
            description = item.find('p').text.strip() if item.find('p') else 'No Description'

            DomesticTrip.objects.get_or_create(
                title=title, 
                description=description
            )
    domestic_destinations = list(DomesticTrip.objects.values())
    return JsonResponse({"domestic_destination": domestic_destinations})

def fetch_international_trips(request):
    url = "https://www.antholidays.com/destination-international"
    international_destinations=[]
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.select('div.hover\\:shadow-lg.border')

        for item in items:
            title = item.find('h2').text.strip() if item.find('h2') else 'No Title'
            description = item.find('p').text.strip() if item.find('p') else 'No Description'

            InternationalTrip.objects.get_or_create(
                title=title,
                description=description,
            )
    international_destinations = list(InternationalTrip.objects.values())
    return JsonResponse({"international_destination": international_destinations})

