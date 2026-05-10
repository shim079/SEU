from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Case, When, BooleanField, Value

from .models import Opportunity
from applications.models import Application
from accounts.models import Notification

User = get_user_model()


@login_required
def opportunity_list(request):

    now = timezone.now()

    opportunities = Opportunity.objects.filter(
        is_active=True, status='approved'
    ).annotate(
        is_expired=Case(
            When(application_deadline__lt=now, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).order_by('is_expired', '-created_at')

    applied_opportunity_ids = Application.objects.filter(
        student=request.user
    ).values_list('opportunity_id', flat=True)

    return render(request, "opportunities/opportunity_list.html", {
        "opportunities": opportunities,
        "applied_opportunity_ids": applied_opportunity_ids,
        "now": now,
    })


@login_required
def opportunity_detail(request, pk):

    opportunity = get_object_or_404(
        Opportunity,
        pk=pk,
        is_active=True,
        status='approved'
    )

    return render(request, "opportunities/opportunity_detail.html", {
        "opportunity": opportunity,
        "now": timezone.now(),
    })


@login_required
def create_opportunity(request):

    if request.user.role != 'agency':
        return redirect('home')

    if request.method == "POST":

        deadline_str = request.POST.get("application_deadline")
        deadline = timezone.now()
        if deadline_str:
            try:
                deadline = timezone.datetime.fromisoformat(deadline_str)
                if timezone.is_naive(deadline):
                    deadline = timezone.make_aware(deadline)
            except ValueError:
                deadline = timezone.now()

        opportunity = Opportunity.objects.create(
            title=request.POST.get("name") or request.POST.get("title"),
            description=request.POST.get("description"),
            location=request.POST.get("location"),
            date=request.POST.get("date"),
            hours=request.POST.get("hours") or 1,
            capacity=request.POST.get("capacity") or 0,
            category=request.POST.get("category"),
            organization=request.POST.get("organization") or "SEU Volunteer Agency",
            application_deadline=deadline,
            status='pending',
            is_active=True,
            created_by=request.user
        )

        admin_users = User.objects.filter(is_staff=True)
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message=_("A new opportunity '%(title)s' has been submitted by %(agency)s and is awaiting your approval.") % {'title': opportunity.title, 'agency': request.user.get_full_name() or request.user.username}
            )

        return redirect("dashboard:agency_dashboard")

    return render(request, "opportunities/create_opportunity.html")


@login_required
def edit_opportunity(request, pk):

    if request.user.role != 'agency':
        return redirect('home')

    opportunity = get_object_or_404(Opportunity, pk=pk, created_by=request.user)

    if request.method == "POST":

        opportunity.title = request.POST.get("name") or request.POST.get("title")
        opportunity.description = request.POST.get("description")
        opportunity.location = request.POST.get("location")
        opportunity.date = request.POST.get("date")
        opportunity.hours = request.POST.get("hours") or 1
        opportunity.capacity = request.POST.get("capacity") or 0
        opportunity.category = request.POST.get("category")
        opportunity.organization = request.POST.get("organization") or "SEU Volunteer Agency"
        deadline_str = request.POST.get("application_deadline")
        if deadline_str:
            try:
                deadline = timezone.datetime.fromisoformat(deadline_str)
                if timezone.is_naive(deadline):
                    deadline = timezone.make_aware(deadline)
                opportunity.application_deadline = deadline
            except ValueError:
                pass

        # يرجع Pending بعد التعديل
        opportunity.status = 'pending'

        opportunity.save()

        return redirect("dashboard:agency_dashboard")

    return render(request, "opportunities/edit_opportunity.html", {
        "opportunity": opportunity
    })


@login_required
def delete_opportunity(request, pk):

    if request.user.role == 'agency':
        opportunity = get_object_or_404(Opportunity, pk=pk, created_by=request.user)
        redirect_url = 'dashboard:agency_dashboard'
    elif request.user.role == 'admin':
        opportunity = get_object_or_404(Opportunity, pk=pk)
        redirect_url = 'dashboard:admin_dashboard'
    else:
        return redirect('home')

    if request.method == "POST":
        opportunity.delete()

    return redirect(redirect_url)


@login_required
def approve_opportunity(request, pk):

    if request.user.role != 'admin':
        return redirect('home')

    opportunity = get_object_or_404(Opportunity, pk=pk)

    opportunity.status = 'approved'
    opportunity.save()

    if opportunity.created_by:
        Notification.objects.create(
            user=opportunity.created_by,
            message=_("Your opportunity '%(title)s' has been approved by the admin and is now available for students.") % {'title': opportunity.title}
        )

    return redirect('dashboard:admin_dashboard')


@login_required
def reject_opportunity(request, pk):

    if request.user.role != 'admin':
        return redirect('home')

    opportunity = get_object_or_404(Opportunity, pk=pk)

    opportunity.status = 'rejected'
    opportunity.save()

    return redirect('dashboard:admin_dashboard')