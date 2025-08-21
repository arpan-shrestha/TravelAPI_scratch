from django.contrib import admin
from .models import DomesticTrip, InternationalTrip

@admin.register(DomesticTrip)
class DomesticTripAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  
    search_fields = ('title', 'description')             

@admin.register(InternationalTrip)
class InternationalTripAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
