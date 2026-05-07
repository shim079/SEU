
"""
Django settings for config project.
"""
import dj_database_url
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'django-insecure-0*djcwk-n#5bon1vdp(at)j(5l)h1#7qhe0a%$o2j%1+x4z$xi'
DEBUG = True
ALLOWED_HOSTS = ['*']

# APPS

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-0*djcwk-n#5bon1vdp(at)j(5l)h1#7qhe0a%$o2j%1+x4z$xi'
DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users.apps.UsersConfig',
    'dashboard',
    'opportunities',
    'applications',
    'accounts',
    'student_profile',
]

 #maryam-merge-fix
# MIDDLEWARE


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#maryam-merge-fix
# URLS
ROOT_URLCONF = 'config.urls'

# TEMPLATES

ROOT_URLCONF = 'config.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

 #maryam-merge-fix
# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# DATABASE

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

 #maryam-merge-fix
# PASSWORDS


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

 #maryam-merge-fix
# LANGUAGE
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

#maryam-merge-fix
LANGUAGES = [
    ('ar', _('Arabic')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# STATIC FILES


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

 #maryam-merge-fix
# DEFAULT FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# USER
AUTH_USER_MODEL = 'users.CustomUser'

# AUTH REDIRECTS
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

ALLOWED_HOSTS = ['*']