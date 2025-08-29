from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateField(blank=True, null=True)
    details_url = models.URLField(max_length=500, blank=True, null=True)
    content = models.JSONField(default=list,blank=True, null=True)


    def __str__(self):
        return self.title
    