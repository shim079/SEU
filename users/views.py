from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Certificate
from accounts.models import Notification
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa

@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(user=request.user).order_by('-issued_at')
    notifications_count = Notification.objects.filter(user=request.user).count()

    return render(request, 'users/my_certificates.html', {
        'certificates': certificates,
        'notifications_count': notifications_count,
    })


@login_required
def certificate_detail(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    return render(request, 'users/certificate_detail.html', {
        'certificate': certificate
    })


@login_required
def certificate_detail_ar(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    return render(request, 'users/certificate_detail_ar.html', {
        'certificate': certificate
    })


def download_certificate_pdf(request, certificate_id):

    certificate = Certificate.objects.get(id=certificate_id)

    template = get_template(
        'users/certificate_detail_ar.html'
    )

    html = template.render({
        'certificate': certificate
    })

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="certificate_{certificate.id}.pdf"'
    )

    pisa.CreatePDF(
        html,
        dest=response
    )

    return response