from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    university_id = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # For AI Recommendation
    major = models.CharField(max_length=100, blank=True, null=True)
    interests = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Write interests separated by commas, e.g. teaching, environment, community"
    )

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('agency', 'Agency'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_agency(self):
        return self.role == 'agency'

    def __str__(self):
        return self.username


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opportunity = models.ForeignKey('opportunities.Opportunity', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
     return f"{self.opportunity.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'opportunity'],
                name='unique_user_opportunity_certificate'
            )
        ]
        