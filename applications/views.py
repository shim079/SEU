from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.translation import gettext as _
from opportunities.models import Opportunity
from .models import Application
from accounts.models import Notification


@login_required
def apply_opportunity(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk, status='approved')

    if request.user.is_staff or request.user.role == 'agency':
        messages.error(request, _("Agencies cannot register for volunteer opportunities."))
        return redirect('opportunities:opportunity_list')

    if opportunity.application_deadline < timezone.now():
        messages.error(request, _("The application deadline for this opportunity has passed."))
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

        Notification.objects.create(
            user=request.user,
            message=_("Your application for '%(title)s' has been submitted successfully. It is currently under review. We will update you soon.") % {'title': opportunity.title}
        )

        if opportunity.created_by:
            Notification.objects.create(
                user=opportunity.created_by,
                message=_("A new application has been submitted by %(student)s for '%(title)s'. Please review it as soon as possible.") % {'student': request.user.get_full_name() or request.user.username, 'title': opportunity.title}
            )

        return render(request, "applications/apply.html", {
            "opportunity": opportunity,
            "success": True,
        })

    return render(request, "applications/apply.html", {
        "opportunity": opportunity,
    })
