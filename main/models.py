from django.db import models

class DomesticTrip(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    details_url = models.URLField(max_length=500,blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    itinerary = models.JSONField(default=list,blank=True, null=True)
    included = models.TextField(blank=True, null=True)
    excluded = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class InternationalTrip(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    details_url = models.URLField(max_length=500, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    itinerary = models.JSONField(default=list, blank=True, null=True)
    included = models.TextField(blank=True, null=True)
    excluded = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
