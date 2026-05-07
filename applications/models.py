from django.db import models
from django.conf import settings


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    opportunity = models.ForeignKey('opportunities.Opportunity', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    volunteer_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.opportunity.title} - {self.status}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status == 'completed':
            from users.models import Certificate
            from accounts.models import Notification

            if not Certificate.objects.filter(
                user=self.student,
                opportunity=self.opportunity
            ).exists():
                Certificate.objects.create(
                    user=self.student,
                    opportunity=self.opportunity
                )

            message = f"Congratulations! Your certificate for {self.opportunity.title} is ready."

            if not Notification.objects.filter(
                user=self.student,
                message=message
            ).exists():
                Notification.objects.create(
                    user=self.student,
                    message=message
                )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'opportunity'],
                name='unique_student_opportunity_application'
            )
        ]