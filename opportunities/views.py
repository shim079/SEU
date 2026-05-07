from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Opportunity
from applications.models import Application


@login_required
def opportunity_list(request):

    opportunities = Opportunity.objects.filter(is_active=True)

    applied_opportunity_ids = Application.objects.filter(
        student=request.user
    ).values_list('opportunity_id', flat=True)

    return render(request, "opportunities/opportunity_list.html", {
        "opportunities": opportunities,
        "applied_opportunity_ids": applied_opportunity_ids,
    })


@login_required
def opportunity_detail(request, pk):

    opportunity = get_object_or_404(
        Opportunity,
        pk=pk,
        is_active=True
    )

    return render(request, "opportunities/opportunity_detail.html", {
        "opportunity": opportunity
    })


@login_required
def create_opportunity(request):

    if request.user.role != 'agency':
        return redirect('home')

    if request.method == "POST":

        Opportunity.objects.create(
            title=request.POST.get("name") or request.POST.get("title"),
            description=request.POST.get("description"),
            location=request.POST.get("location"),
            date=request.POST.get("date"),
            hours=request.POST.get("hours") or 1,
            capacity=request.POST.get("capacity") or 0,
            category=request.POST.get("category"),
            organization=request.POST.get("organization") or "SEU Volunteer Agency",
            status='pending',
            is_active=True,
            created_by=request.user
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

        # يرجع Pending بعد التعديل
        opportunity.status = 'pending'

        opportunity.save()

        return redirect("dashboard:agency_dashboard")

    return render(request, "opportunities/edit_opportunity.html", {
        "opportunity": opportunity
    })


@login_required
def delete_opportunity(request, pk):

    if request.user.role != 'agency':
        return redirect('home')

    opportunity = get_object_or_404(Opportunity, pk=pk, created_by=request.user)

    if request.method == "POST":
        opportunity.delete()

    return redirect("dashboard:agency_dashboard")


@login_required
def approve_opportunity(request, pk):

    if request.user.role != 'admin':
        return redirect('home')

    opportunity = get_object_or_404(Opportunity, pk=pk)

    opportunity.status = 'approved'
    opportunity.save()

    return redirect('dashboard:admin_dashboard')


@login_required
def reject_opportunity(request, pk):

    if request.user.role != 'admin':
        return redirect('home')

    opportunity = get_object_or_404(Opportunity, pk=pk)

    opportunity.status = 'rejected'
    opportunity.save()

    return redirect('dashboard:admin_dashboard')