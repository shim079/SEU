from django.db import models
from django.conf import settings


class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return self.title


class Registration(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')
    hours = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.opportunity.title}"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"