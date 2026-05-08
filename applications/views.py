from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from opportunities.models import Opportunity
from .models import Application


@login_required
def apply_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, status='approved')

    if request.user.is_staff or request.user.role == 'agency':
        messages.error(request, _("Agencies cannot register for volunteer opportunities."))
        return redirect('opportunities:opportunity_list')

    existing_application = Application.objects.filter(
        student=request.user,
        opportunity=opportunity
    ).first()

    if existing_application:
        return render(request, "applications/apply.html", {
            "opportunity": opportunity,
            "already_applied": True,
            "application": existing_application,
        })

    if request.method == "POST":
        Application.objects.create(
            student=request.user,
            opportunity=opportunity
        )

        return render(request, "applications/apply.html", {
            "opportunity": opportunity,
            "success": True,
        })

    return render(request, "applications/apply.html", {
        "opportunity": opportunity,
    })
