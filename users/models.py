from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Phone'))
    university_id = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('University ID'))
    bio = models.TextField(blank=True, null=True, verbose_name=_('Bio'))
    major = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Major'))
    interests = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Interests'),
        help_text=_("Write interests separated by commas, e.g. teaching, environment, community")
    )

    ROLE_CHOICES = (
        ('student', _('Student')),
        ('agency', _('Agency')),
        ('admin', _('Admin')),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name=_('Role'))

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_agency(self):
        return self.role == 'agency'

    def __str__(self):
        return self.username


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('User'))
    opportunity = models.ForeignKey('opportunities.Opportunity', on_delete=models.CASCADE, verbose_name=_('Opportunity'))
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Issued at'))

    def __str__(self):
        return f"{self.opportunity.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'opportunity'],
                name='unique_user_opportunity_certificate'
            )
        ]
        verbose_name = _('Certificate')
        verbose_name_plural = _('Certificates')
