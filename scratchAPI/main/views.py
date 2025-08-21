from .models import DomesticTrip, InternationalTrip
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import urllib.parse

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
            a_tag = item.find('a', href=True)
            details_url = a_tag['href'] if a_tag else None
            if details_url:
                details_url = urllib.parse.urljoin("https://www.antholidays.com", details_url)

            DomesticTrip.objects.get_or_create(
                title=title,
                defaults={
                    "description":description,
                    "details_url":details_url
                } 
            )
    domestic_destinations = list(DomesticTrip.objects.values())
    return JsonResponse({"domestic_destination": domestic_destinations})

# def fetch_domestic_trip_details(request, slug):


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
            a_tag = item.find('a', href=True)
            details_url = a_tag['href'] if a_tag else None
            if details_url:
                details_url = urllib.parse.urljoin("https://www.antholidays.com", details_url)

            InternationalTrip.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "details_url": details_url
                }
            )
    international_destinations = list(InternationalTrip.objects.values())
    return JsonResponse({"international_destination": international_destinations})

