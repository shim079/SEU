from django.urls import path
from .views import certificate_detail, certificate_detail_ar, my_certificates

urlpatterns = [
    path('certificate/<int:certificate_id>/', certificate_detail, name='certificate_en'),
    path('certificate/ar/<int:certificate_id>/', certificate_detail_ar, name='certificate_ar'),
    path('my-certificates/', my_certificates, name='my_certificates'),
]
