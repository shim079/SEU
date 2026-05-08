from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.translation import gettext as _

from opportunities.models import Opportunity
from applications.models import Application
from dashboard.ai_recommendation import recommend_opportunities

User = get_user_model()


def home(request):
    total_volunteers = User.objects.filter(role='student').count()
    total_organizations = User.objects.filter(role='agency').count()
    total_opportunities = Opportunity.objects.filter(is_active=True).count()
    total_hours = Application.objects.filter(
        status='completed'
    ).aggregate(
        total=Sum('volunteer_hours')
    )['total'] or 0

    return render(request, 'home.html', {
        'total_volunteers': total_volunteers,
        'total_organizations': total_organizations,
        'total_opportunities': total_opportunities,
        'total_hours': total_hours,
    })


def login_view(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_staff:
                return redirect('dashboard:admin_dashboard')

            elif user.role == 'agency':
                return redirect('dashboard:agency_dashboard')

            else:
                return redirect('dashboard:student_dashboard')

        messages.error(request, _('Invalid username or password.'))

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role', 'student')

        valid_roles = ['student', 'agency']
        if role not in valid_roles:
            role = 'student'

        if not email or email.strip() == "":
            messages.error(request, _('Email is required.'))
            return render(request, 'registration/signup.html')

        email = email.strip()

        if password != confirm_password:
            messages.error(request, _('Passwords do not match.'))
            return render(request, 'registration/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, _('Email already exists.'))
            return render(request, 'registration/signup.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        user.first_name = first_name or ""
        user.role = role
        user.save()

        login(request, user)

        if user.is_staff:
            return redirect('dashboard:admin_dashboard')
        elif user.role == 'agency':
            return redirect('dashboard:agency_dashboard')
        else:
            return redirect('dashboard:student_dashboard')

    return render(request, 'registration/signup.html')


@login_required
def dashboard(request):

    if request.user.is_staff:
        return redirect('dashboard:admin_dashboard')

    elif request.user.role == 'agency':
        return redirect('dashboard:agency_dashboard')

    else:
        return redirect('dashboard:student_dashboard')


@login_required
def student_dashboard(request):

    if request.user.role != 'student':
        return redirect('home')

    opportunities = Opportunity.objects.filter(
    is_active=True
)

    total_opportunities = opportunities.count()

    total_applications = Application.objects.filter(
        student=request.user
    ).count()

    total_hours = Application.objects.filter(
        student=request.user,
        status="completed"
    ).aggregate(
        total=Sum("volunteer_hours")
    )["total"] or 0

    user_profile = getattr(request.user, 'profile', None)
    
    user_data = {
        "major": (getattr(user_profile, "major", "") or "") if user_profile else "",
        "interests": (getattr(user_profile, "interests", "") or "") if user_profile else "",
        "skills": (getattr(user_profile, "skills", "") or "") if user_profile else "",
        "department": (getattr(user_profile, "department", "") or "") if user_profile else "",
        "location": (getattr(user_profile, "location", "") or "") if user_profile else "",
    }

    recommended = recommend_opportunities(
        user_data,
        opportunities
    )

    registrations = Application.objects.filter(
        student=request.user
    ).select_related('opportunity')

    context = {
        "total_opportunities": total_opportunities,
        "total_applications": total_applications,
        "total_hours": total_hours,
        "recommended": recommended,
        "registrations": registrations,
    }

    return render(
        request,
        'dashboard/student_dashboard.html',
        context
    )


@login_required
def agency_dashboard(request):

    if request.user.role != 'agency':
        return redirect('home')

    opportunities = Opportunity.objects.filter(created_by=request.user).order_by('-id')

    applications = Application.objects.filter(
        opportunity__in=opportunities
    ).select_related(
        'student',
        'opportunity'
    ).order_by('-applied_at')

    context = {
        'opportunities': opportunities,
        'applications': applications,
    }

    return render(
        request,
        'dashboard/agency_dashboard.html',
        context
    )


@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect('home')

    opportunities = Opportunity.objects.all().order_by('-id')

    total_users = User.objects.count()

    active_opportunities = Opportunity.objects.filter(
        status='approved'
    ).count()

    pending_requests = Opportunity.objects.filter(
        status='pending'
    ).count()

    context = {
        'total_users': total_users,
        'active_opportunities': active_opportunities,
        'pending_requests': pending_requests,
        'opportunities': opportunities,
    }

    return render(
        request,
        'dashboard/admin_dashboard.html',
        context
    )


@login_required
def add_opportunity(request):

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

    return render(
        request,
        'dashboard/add_opportunity.html'
    )


@login_required
def view_volunteers(request):

    if request.user.role != 'agency' and not request.user.is_staff:
        return redirect('home')

    return render(
        request,
        'dashboard/view_volunteers.html'
    )


@login_required
def manage_users(request):

    if not request.user.is_staff:
        return redirect('home')

    users = User.objects.all().order_by('id')

    return render(
        request,
        'dashboard/manage_users.html',
        {
            'users': users
        }
    )


@login_required
def approve_hours(request):

    if not request.user.is_staff:
        return redirect('home')

    registrations = Application.objects.select_related(
        'student',
        'opportunity'
    ).order_by('-applied_at')

    return render(
        request,
        'dashboard/approve_hours.html',
        {
            'registrations': registrations
        }
    )


@login_required
def complete_application(request, pk):

    if not request.user.is_staff:
        return redirect('home')

    application = Application.objects.get(pk=pk)

    application.status = 'completed'
    application.volunteer_hours = application.opportunity.hours

    application.save()

    return redirect('dashboard:approve_hours')


@login_required
def toggle_user_status(request, pk):

    if not request.user.is_staff:
        return redirect('home')

    user = User.objects.get(pk=pk)

    if user != request.user:
        user.is_active = not user.is_active
        user.save()

    return redirect('dashboard:manage_users')


@login_required
def delete_user(request, pk):

    if not request.user.is_staff:
        return redirect('home')

    user = User.objects.get(pk=pk)

    if user != request.user:
        user.delete()

    return redirect('dashboard:manage_users')
