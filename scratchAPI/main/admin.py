from django.contrib import admin
from .models import DomesticTrip, InternationalTrip

@admin.register(DomesticTrip)
class DomesticTripAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  
    search_fields = ('title', 'description')  

    verbose_name = "Domestic Trip"
    verbose_name_plural = "Domestic Trips"           

@admin.register(InternationalTrip)
class InternationalTripAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

    verbose_name = "International Trip"
    verbose_name_plural = "International Trips"
