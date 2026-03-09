from pathlib import Path
import json
import sys
from django.core.exceptions import ImproperlyConfigured
import os



BASE_DIR = Path(__file__).resolve().parent.parent


SECRETS_FILE = BASE_DIR / 'secrets.json'
try:
    with open(SECRETS_FILE, 'r', encoding='utf-8') as f:
        SECRETS = json.load(f)
except FileNotFoundError:
    SECRETS = {}

def get_secret(key, default=None):
    """Return secret value for `key`. If not found, return `default` (if provided)
    otherwise raise ImproperlyConfigured.
    """
    if key in SECRETS:
        return SECRETS[key]
    if default is not None:
        return default
    raise ImproperlyConfigured(f"Missing required secret: {key}")

# Secret key (prefer secrets.json)
SECRET_KEY = get_secret('SECRET_KEY', 'django-insecure-your-secret-key')
DEBUG = True
ALLOWED_HOSTS = ['syntheseed.com', 'www.syntheseed.com', '127.0.0.1', 'localhost']


# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'contact',
    'blogs',
    'Careers',
    'ckeditor',
    'ckeditor_uploader',

]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'company_backend.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'company_backend.wsgi.application'

# Database (PostgreSQL)
# Prefer a `DATABASES` mapping inside secrets.json, otherwise fall back to
# individual keys: DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT.
if 'DATABASES' in SECRETS and isinstance(SECRETS['DATABASES'], dict):
    DATABASES = SECRETS['DATABASES']
else:
    DATABASES = {
        'default': {
            'ENGINE': get_secret('DB_ENGINE', 'django.db.backends.postgresql'),
            'NAME': get_secret('DB_NAME'),
            'USER': get_secret('DB_USER'),
            'PASSWORD': get_secret('DB_PASSWORD'),
            'HOST': get_secret('DB_HOST'),
            'PORT': get_secret('DB_PORT'),
            'OPTION': {
                'sslmode': 'require',
            }
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/syntheseedbe/company_backend/static/'
MEDIA_URL = "/media/"
MEDIA_ROOT ='/var/www/syntheseedbe/company_backend/media/'
BASE_BACKEND_URL = "http://127.0.0.1:8000"

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'extraPlugins': ','.join(['uploadimage', 'image2']),
        'removePlugins': 'image',
        'forcePasteAsPlainText': False,
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React local
    "http://localhost:5173",  # Vite local
    "https://syntheseed.com",  # Production
    "https://www.syntheseed.com"  # Production (www)
]

# CORS_ALLOW_ALL_ORIGINS = True  # uncomment for testing only

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} — {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',  # 👈 shows request-related debug info
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'rest_framework': {
            'handlers': ['console'],
            'level': 'DEBUG',  # 👈 shows auth + permission details
            'propagate': False,
        },
    },
}



# Add this if you’re accessing the API from your React dev server
CORS_ALLOW_ALL_ORIGINS = True

# Email / Microsoft Graph configuration (prefer secrets.json values)
# We prefer using Microsoft Graph (client credentials) for sending mail.
# SMTP-related settings were removed to avoid accidental basic-auth attempts.

# Default from address and notification recipients
DEFAULT_FROM_EMAIL = get_secret('DEFAULT_FROM_EMAIL', get_secret('AZURE_SENDER_UPN', None))
NOTIFY_CONTACT_RECIPIENTS = get_secret('NOTIFY_CONTACT_RECIPIENTS', None)

# Azure AD / Microsoft Graph client credentials (for app-only mail sending)
AZURE_CLIENT_ID = get_secret('AZURE_CLIENT_ID', None)
AZURE_CLIENT_SECRET = get_secret('AZURE_CLIENT_SECRET', None)
AZURE_TENANT_ID = get_secret('AZURE_TENANT_ID', None)
AZURE_SENDER_UPN = get_secret('AZURE_SENDER_UPN', None)

# Optionally send a copy of notifications to the sender mailbox (useful for testing)
# Set this to true in secrets.json to include the sender in recipients.
SEND_COPY_TO_SENDER = get_secret('SEND_COPY_TO_SENDER', False)



