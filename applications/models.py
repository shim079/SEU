from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('rejected', _('Rejected')),
        ('completed', _('Completed')),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Student'))
    opportunity = models.ForeignKey('opportunities.Opportunity', on_delete=models.CASCADE, verbose_name=_('Opportunity'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    volunteer_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name=_('Volunteer hours'))
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Applied at'))
    participation_confirmed = models.BooleanField(default=False, verbose_name=_('Participation confirmed'))

    def __str__(self):
        return f"{self.student.username} - {self.opportunity.title} - {self.status}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        from accounts.models import Notification

        if self.status == 'accepted':
            message = _("Congratulations! Your application for '%(title)s' has been accepted.") % {'title': self.opportunity.title}

            if not Notification.objects.filter(
                user=self.student,
                message=message
            ).exists():
                Notification.objects.create(
                    user=self.student,
                    message=message
                )

        if self.status == 'completed':
            from users.models import Certificate

            if not Certificate.objects.filter(
                user=self.student,
                opportunity=self.opportunity
            ).exists():
                Certificate.objects.create(
                    user=self.student,
                    opportunity=self.opportunity
                )

            message = _("Congratulations! Your certificate for %(title)s is ready.") % {'title': self.opportunity.title}

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
        verbose_name = _('Application')
        verbose_name_plural = _('Applications')
