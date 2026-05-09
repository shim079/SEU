from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models import Sum
from opportunities.models import Opportunity
from applications.models import Application
from accounts.models import Notification
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
    #calculate opporunities
    opportunities = Opportunity.objects.filter(created_by=request.user).order_by('-id')
    total_opportunities = opportunities.count()

    #calculate applications
    applications = Application.objects.filter(
        opportunity__in=opportunities
    ).select_related(
        'student',
        'opportunity'
    ).order_by('-applied_at')
    total_applications = applications.count()

    #calculate volunteer hours
    total_hours = Application.objects.filter(
        opportunity__created_by=request.user,
        status='completed'
    ).aggregate(
        total=Sum('volunteer_hours')
    )['total'] or 0

    context = {
        'opportunities': opportunities,
        'applications': applications,
        'total_hours': total_hours,
        'total_applications': total_applications,
        'total_opportunities': total_opportunities,
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

    approved_requests = Opportunity.objects.filter(status="approved").order_by('-id')
    approved_requests_count = approved_requests.count()

    total_completed_hours = Application.objects.filter(
    status="completed").aggregate(total=Sum("volunteer_hours"))["total"] or 0

    rejected_requests = Application.objects.filter(status="rejected").count()

    context = {
        'total_users': total_users,
        'active_opportunities': active_opportunities,
        'pending_requests': pending_requests,
        'opportunities': opportunities,
        "approved_requests_count": approved_requests_count,
        'total_completed_hours': total_completed_hours,
        'rejected_requests': rejected_requests,
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

    return render(
        request,
        'dashboard/add_opportunity.html'
    )


@login_required
def view_volunteers(request):

    if request.user.role != 'agency' and not request.user.is_staff:
        return redirect('home')

    opportunities = Opportunity.objects.filter(created_by=request.user)

    volunteers = Application.objects.filter(
        opportunity__in=opportunities,
        participation_confirmed=True
    ).select_related('student', 'opportunity').order_by('-applied_at')

    return render(
        request,
        'dashboard/view_volunteers.html',
        {'volunteers': volunteers}
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
def accept_application(request, pk):

    if request.user.role != 'agency':
        return redirect('home')

    application = Application.objects.select_related('opportunity').get(pk=pk)

    if application.opportunity.created_by != request.user:
        messages.error(request, _("You can only manage applications for your own opportunities."))
        return redirect('dashboard:agency_dashboard')

    application.status = 'accepted'
    application.save()

    return redirect('dashboard:agency_dashboard')


@login_required
def confirm_participation(request, pk):

    if request.user.role != 'agency':
        return redirect('home')

    application = Application.objects.select_related('opportunity').get(pk=pk)

    if application.opportunity.created_by != request.user:
        messages.error(request, _("You can only manage applications for your own opportunities."))
        return redirect('dashboard:agency_dashboard')

    application.participation_confirmed = True
    application.save()

    return redirect('dashboard:agency_dashboard')


@login_required
def reject_application(request, pk):

    if request.user.role != 'agency':
        return redirect('home')

    application = Application.objects.select_related('opportunity').get(pk=pk)

    if application.opportunity.created_by != request.user:
        messages.error(request, _("You can only manage applications for your own opportunities."))
        return redirect('dashboard:agency_dashboard')

    application.status = "rejected"
    application.save()

    return redirect('dashboard:agency_dashboard')


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



# ===================== RADAR CHART View ===================== 
def agency_radar_data(request):
    if request.user.role != 'agency':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    opportunities = Opportunity.objects.filter(created_by=request.user)
    apps = Application.objects.filter(opportunity__in=opportunities)

    total_applications = apps.count()
    total_hours = apps.filter(status='completed').aggregate(total=Sum('volunteer_hours'))['total'] or 0
    unique_volunteers = apps.values('student').distinct().count()
    max_hours = opportunities.aggregate(total=Sum('hours'))['total'] or 1
    max_volunteers = apps.values('student').distinct().count() or 1

    approved_completed = apps.filter(status__in=['accepted', 'completed']).count()
    completed = apps.filter(status='completed').count()
    confirmed = apps.filter(participation_confirmed=True).count()

    approval_rate = round((approved_completed / total_applications) * 100, 1) if total_applications > 0 else 0
    completion_rate = round((completed / total_applications) * 100, 1) if total_applications > 0 else 0
    confirmation_rate = round((confirmed / total_applications) * 100, 1) if total_applications > 0 else 0

    return JsonResponse({
        'total_applications': total_applications,
        'total_hours': float(total_hours),
        'max_hours': float(max_hours),
        'unique_volunteers': unique_volunteers,
        'max_volunteers': max_volunteers,
        'approval_rate': approval_rate,
        'completion_rate': completion_rate,
        'confirmation_rate': confirmation_rate,
    })

# ===================== AGENCY PERFORMANCE DATA View =====================
@login_required
def agency_performance_data(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        agencies = User.objects.filter(role='agency')
        rows = []

        for agency in agencies:
            apps = Application.objects.filter(opportunity__created_by=agency)

            total = apps.count()
            approved_completed = apps.filter(status__in=['accepted', 'completed']).count()
            completed = apps.filter(status='completed').count()
            pending = apps.filter(status='pending').count()
            active_users = apps.values('student').distinct().count()

            approval_rate = (approved_completed / total * 100) if total > 0 else 0

            rows.append({
                'agency': agency.get_full_name() or agency.username,
                'approval_rate': approval_rate,
                'completed': completed,
                'active_users': active_users,
                'pending': pending,
            })

        if not rows:
            return JsonResponse([], safe=False)

        max_completed = max(r['completed'] for r in rows) or 1
        max_active = max(r['active_users'] for r in rows) or 1
        max_pending = max(r['pending'] for r in rows) or 1

        for r in rows:
            norm_completed = (r['completed'] / max_completed) * 100
            norm_active = (r['active_users'] / max_active) * 100
            norm_pending = (r['pending'] / max_pending) * 100

            score = (
                r['approval_rate'] * 0.4
                + norm_completed * 0.3
                + norm_active * 0.2
                - norm_pending * 0.1
            )

            r['score'] = round(score, 1)
            r['approval_rate'] = round(r['approval_rate'], 1)

        rows.sort(key=lambda x: x['score'], reverse=True)

        return JsonResponse(rows, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


