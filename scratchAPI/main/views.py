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
    domestic_destinations = list(DomesticTrip.objects.values('id','title','description','details_url'))
    return JsonResponse({"domestic_destination": domestic_destinations})

def fetch_domestic_trip_details(request, trip_id):
    try:
        trip = DomesticTrip.objects.get(id=trip_id)
    except DomesticTrip.DoesNotExist:
        return JsonResponse({"error":"Domestic Trip not found"}, status=404)
    details_data = {
        "title":trip.title,
        "description":trip.description,
        "details_url":trip.details_url
    }
    if trip.details_url:
        response = requests.get(trip.details_url)
        if response.status_code==200:
            soup = BeautifulSoup(response.content, 'html.parser')
            overview = soup.select_one('div#overview .overview')
            itinerary = soup.select_one('div#itinerary .ckEditor')
            included = soup.select_one('div#included-excluded div:nth-child(1) div')
            excluded = soup.select_one('div#included-excluded div:nth-child(2) div')

            # Save scraped data to database
            trip.overview = overview.get_text(strip=True) if overview else ""
            trip.itinerary = itinerary.get_text(strip=True) if itinerary else ""
            trip.included = included.get_text(strip=True) if included else ""
            trip.excluded = excluded.get_text(strip=True) if excluded else ""
            trip.save()

            # Prepare response
            details_data.update({
                "overview": trip.overview,
                "itinerary": trip.itinerary,
                "included": trip.included,
                "excluded": trip.excluded
            })
        else:
            details_data["error"] = "Unable to fetch details"
    else:
        details_data["error"] = "No details URL provided"
    return JsonResponse(details_data)


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
    international_destinations = list(InternationalTrip.objects.values('id','title','description','details_url'))
    return JsonResponse({"international_destination": international_destinations})

def fetch_international_trip_details(request, trip_id):
    try:
        trip = InternationalTrip.objects.get(id=trip_id)
    except InternationalTrip.DoesNotExist:
        return JsonResponse({"error":"International Trip not found"}, status=404)
    details_data = {
        "title":trip.title,
        "description":trip.description,
        "details_url":trip.details_url
    }
    if trip.details_url:
        response = requests.get(trip.details_url)
        if response.status_code==200:
            soup = BeautifulSoup(response.content, 'html.parser')
            overview = soup.select_one('div#overview .overview')
            itinerary = soup.select_one('div#itinerary .ckEditor')
            included = soup.select_one('div#included-excluded div:nth-child(1) div')
            excluded = soup.select_one('div#included-excluded div:nth-child(2) div')

            # Save scraped data to database
            trip.overview = overview.get_text(strip=True) if overview else ""
            trip.itinerary = itinerary.get_text(strip=True) if itinerary else ""
            trip.included = included.get_text(strip=True) if included else ""
            trip.excluded = excluded.get_text(strip=True) if excluded else ""
            trip.save()

            # Prepare response
            details_data.update({
                "overview": trip.overview,
                "itinerary": trip.itinerary,
                "included": trip.included,
                "excluded": trip.excluded
            })
        else:
            details_data["error"] = "Unable to fetch details"
    else:
        details_data["error"] = "No details URL provided"
    return JsonResponse(details_data)
