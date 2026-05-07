from django.db import models
from django.conf import settings

class Opportunity(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    hours = models.IntegerField(default=1)
    category = models.CharField(max_length=100, blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    capacity = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='opportunities', null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title