from django.db import models

class Services(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    details_url = models.URLField(max_length=500, blank=True,null=True)

    def __str__(self):
        return self.title
    
