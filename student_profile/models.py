from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)

    major = models.CharField(max_length=100, blank=True)
    interests = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username