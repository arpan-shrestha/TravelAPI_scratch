from .models import DomesticTrip, InternationalTrip
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json
from django.views.decorators.csrf import csrf_exempt

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
            details_url = item.find('a', href=True)['href'] if item.find('a', href=True) else None
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
            if itinerary:
                text = itinerary.get_text("\n", strip=True)
                day_blocks = re.split(r'(Day\s*\d+)', text)
                structured_itinerary = []
                for i in range(1, len(day_blocks), 2):  
                    day = day_blocks[i] 
                    details = day_blocks[i+1].strip()
                    structured_itinerary.append(f"{day}: {details}")
                trip.itinerary = structured_itinerary
            else:
                trip.itinerary = []
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
            details_url = item.find('a', href=True)['href'] if item.find('a', href=True) else None
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
            if itinerary:
                text = itinerary.get_text("\n", strip=True)
                day_blocks = re.split(r'(Day\s*\d+)', text)
                structured_itinerary = []
                for i in range(1, len(day_blocks), 2):  
                    day = day_blocks[i] 
                    details = day_blocks[i+1].strip()
                    structured_itinerary.append(f"{day}: {details}")
                trip.itinerary = structured_itinerary
            else:
                trip.itinerary = []
            trip.included = included.get_text(strip=True) if included else ""
            trip.excluded = excluded.get_text(strip=True) if excluded else ""
            trip.save()

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


@csrf_exempt
def add_domestic_trip(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            trip = DomesticTrip.objects.create(
                title = data.get('title',''),
                description = data.get('description',''),
                details_url = data.get('details_url',''),
                overview = data.get('overview',''),
                itinerary = data.get('itinerary',[]),
                included = data.get('included',''),
                excluded = data.get('excluded',''),
            )
            return JsonResponse({'success':True, 'id':trip.id})
        except Exception as e:
            return JsonResponse({'success':False,'error':str(e)}, status=400)
    return JsonResponse({'error':'POST Method is required'}, status=405)



@csrf_exempt
def add_international_trip(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            trip = InternationalTrip.objects.create(
                title=data.get('title',''),
                description = data.get('description',''),
                details_url=data.get('details_url',''),
                overview = data.get('overview',''),
                itinerary = data.get('itinerary',[]),
                included = data.get('included',''),
                excluded = data.get('excluded','')
            )
            return JsonResponse({'success':True,'id':trip.id})
        except Exception as e:
            return JsonResponse({'success':False,'error':str(e)}, status=400)
    return JsonResponse({'error':'POST Method is required'}, status=405)
