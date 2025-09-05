from .models import DomesticTrip, InternationalTrip
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from collections import OrderedDict
from RBAC.decorator import token_required


def fetch_domestic_trips(request):
    domestic_destinations = list(DomesticTrip.objects.values(
        'id', 'title', 'description', 'details_url'
    ))
    return JsonResponse({"domestic_destinations": domestic_destinations})

def fetch_domestic_trip_details(request, trip_id):
    try:
        trip = DomesticTrip.objects.get(id=trip_id)
    except DomesticTrip.DoesNotExist:
        return JsonResponse({"error": "Domestic Trip not found"}, status=404)
    ordered_itinerary = []
    for item in trip.itinerary or []:
        ordered_itinerary.append(
            OrderedDict([
                ("heading", item.get("heading", "")),
                ("details", item.get("details", ""))
            ])
        )
    details_data = {
        'title': trip.title,
        'description': trip.description,
        'details_url': trip.details_url,
        'overview': trip.overview or "",
        'itinerary': ordered_itinerary,
        'included': trip.included or "",
        'excluded': trip.excluded or "",
    }

    return JsonResponse(details_data)


def fetch_international_trips(request):
    international_destinations=list(InternationalTrip.objects.values(
        'id','title','description','details_url'
        ))
    return JsonResponse({"international_destination": international_destinations})

def fetch_international_trip_details(request, trip_id):
    try:
        trip = InternationalTrip.objects.get(id=trip_id)
    except InternationalTrip.DoesNotExist:
        return JsonResponse({"error":"International Trip not found"}, status=404)
    ordered_itinerary = []
    for item in trip.itinerary or []:
        ordered_itinerary.append(
            OrderedDict([
                ("heading", item.get("heading", "")),
                ("details", item.get("details", ""))
            ])
        )
    details_data = {
        'title': trip.title,
        'description': trip.description,
        'details_url': trip.details_url,
        'overview': trip.overview or "",
        'itinerary': ordered_itinerary,
        'included': trip.included or "",
        'excluded': trip.excluded or "",
    }
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
def update_domestic_trip(request, trip_id):
    if request.method in ['PUT', 'PATCH']:
        try:
            trip = DomesticTrip.objects.get(id=trip_id)
            data = json.loads(request.body)

            trip.title = data.get('title', trip.title)
            trip.description = data.get('description',trip.description)
            trip.details_url = data.get('details_url',trip.details_url)
            trip.overview = data.get('overview', trip.overview)
            trip.itinerary = data.get('itinerary', trip.itinerary)
            trip.included = data.get('included', trip.included)
            trip.excluded = data.get('excluded', trip.excluded)
            
            trip.save()
            return JsonResponse({'success':True})
        except DomesticTrip.DoesNotExist:
            return JsonResponse({'error':'Domestic Trip not found'}, status=400)
    return JsonResponse({'error':'Check your Method'},status=405)


@csrf_exempt
def delete_domestic_trip(request, trip_id):
    if request.method == 'DELETE':
        try:
            trip = DomesticTrip.objects.get(id=trip_id)
            trip.delete()
            return JsonResponse({'success':True})
        except DomesticTrip.DoesNotExist:
            return JsonResponse({'error':'Domestic Trip not found'},status=400)
    return JsonResponse({'error':'Delete Method required'}, status=405)

@csrf_exempt
def update_international_trip(request, trip_id):
    if request.method in ['PUT', 'PATCH']:
        try:
            trip = InternationalTrip.objects.get(id=trip_id)
            data = json.loads(request.body)

            trip.title = data.get('title', trip.title)
            trip.description = data.get('description',trip.description)
            trip.details_url = data.get('details_url',trip.details_url)
            trip.overview = data.get('overview', trip.overview)
            trip.itinerary = data.get('itinerary', trip.itinerary)
            trip.included = data.get('included', trip.included)
            trip.excluded = data.get('excluded', trip.excluded)
            
            trip.save()
            return JsonResponse({'success':True})
        except InternationalTrip.DoesNotExist:
            return JsonResponse({'error':'Domestic Trip not found'}, status=400)
    return JsonResponse({'error':'Check your Method'},status=405)


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


@csrf_exempt
def delete_international_trip(request, trip_id):
    if request.method == 'DELETE':
        try:
            trip = InternationalTrip.objects.get(id=trip_id)
            trip.delete()
            return JsonResponse({'success':True})
        except InternationalTrip.DoesNotExist:
            return JsonResponse({'error':'International Trip not found'},status=400)
    return JsonResponse({'error':'Delete Method required'}, status=405)





