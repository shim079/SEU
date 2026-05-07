from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Opportunity(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    )

    title = models.CharField(max_length=200, verbose_name=_('Title'))
    location = models.CharField(max_length=200, verbose_name=_('Location'))
    description = models.TextField(verbose_name=_('Description'))
    date = models.DateField(null=True, blank=True, verbose_name=_('Date'))
    hours = models.IntegerField(default=1, verbose_name=_('Hours'))
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Category'))
    organization = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Organization'))
    capacity = models.IntegerField(default=0, verbose_name=_('Capacity'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_('Status'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='opportunities', null=True, blank=True, verbose_name=_('Created by'))

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title

    class Meta:
        verbose_name = _('Opportunity')
        verbose_name_plural = _('Opportunities')
