from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from dashboard import views as dashboard_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', dashboard_views.home, name='home'),
    path('login/', dashboard_views.login_view, name='login'),
    path('logout/', dashboard_views.logout_view, name='logout'),
    path('signup/', dashboard_views.register_view, name='signup'),
    path('register/', dashboard_views.register_view, name='register'),

    path('dashboard/', include('dashboard.urls')),
    path('opportunities/', include('opportunities.urls')),
    path('applications/', include('applications.urls')),
    path('users/', include('users.urls')),
    path('profile/', include('student_profile.urls')),
    path('', include('accounts.urls')),

    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)