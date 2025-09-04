from django.contrib import admin
from .models import Blog
# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','description','published_date')
    search_fields = ('title', 'description')

    verbose_name = "Blog"
    verbose_name_plural = "Blogs"