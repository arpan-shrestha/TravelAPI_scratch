from django.db import models
from django.contrib.auth.models import User

class AuthToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, unique=True)
    refresh_token = models.CharField(max_length=255, unique=True)
    access_token_expire = models.DateTimeField()
    refresh_token_expire = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"AuthToken for {self.user.username}"
