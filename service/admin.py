from django.contrib import admin
from .models import Services

# Register your models here.
@admin.register(Services)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title','description')
    search_fields = ('title', 'description')

    verbose_name = "Service"
    verbose_name_plural = "Services"