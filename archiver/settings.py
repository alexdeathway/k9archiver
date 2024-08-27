"""
Django settings for archiver project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from .secgen import generate_secret_key
from archiver import is_available,storage_backend
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
 
# try:
#     from .secret_keys import SECRET_KEY
# except ModuleNotFoundError:
#     SETTINGS_DIR=os.path.abspath(os.path.dirname(__file__))
#     generate_secret_key(os.path.join(SETTINGS_DIR,"secret_keys.py"))
#     from .secret_keys import SECRET_KEY 


SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.getenv('DEBUG')
#SECRET_KEY=""
DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
    'archiver',
    'cluster.apps.ClusterConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    "crispy_forms",
    'crispy_tailwind',
    'django_summernote',
    'storages',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'archiver.middleware.CacheIfSlowMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'archiver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
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

WSGI_APPLICATION = 'archiver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "CONN_MAX_AGE": int(os.environ.get("POSTGRES_CONN_MAX_AGE", 60))
    },
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATICFILES_DIRS = [
     os.path.join(BASE_DIR,'static'),
 ]
STATIC_URL='/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

MEDIA_ROOT=os.path.join(BASE_DIR,'media')
MEDIA_URL='/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL="users.User"
CRISPY_TEMPLATE_PACK="tailwind"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL='home'

#email settings
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL=os.environ.get('DEFAULT_FROM_EMAIL')
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey' for sendgrid
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#enforces limit of 1MB for file upload
FILE_SIZE_LIMIT=1024*1024

#django summer note settings
X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_CONFIG = {
    'summernote':{
        'toolbar': [
                        ['style', ['style']],
                        ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript',
                                  'strikethrough', 'clear']],
                        ['fontname', ['fontname']],
                        ['fontsize', ['fontsize']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['height', ['height']],
                        ['table', ['table']],
                        ['insert', ['link', 'picture', 'video', 'hr']],
                        ['view', ['fullscreen', 'codeview']],
                        ['help', ['help']],
                    ],
                },
        'attachment_filesize_limit':FILE_SIZE_LIMIT,
        'attachment_require_authentication': True,
        'attachment_absolute_uri': True,
        'attachment_storage_class':'archiver.storage_backend.MediaStorage',

}


#DEFAULT_FILE_STORAGE = 'archiver.storage_backend.MediaStorage'
DEFAULT_FILE_STORAGE = "storages.backends.dropbox.DropboxStorage"
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  
STATICFILES_STORAGE ="whitenoise.storage.CompressedManifestStaticFilesStorage"
#dropbox settings
DROPBOX_ROOT_PATH = '/k9archiver/'
DROPBOX_APP_KEY = os.environ.get('DROPBOX_APP_KEY')
DROPBOX_APP_SECRET = os.environ.get('DROPBOX_APP_SECRET')
DROPBOX_OAUTH2_REFRESH_TOKEN=os.environ.get('DROPBOX_OAUTH2_REFRESH_TOKEN')

#[V-dev4.1.0] AWS/Backblaze settings for Media Storage
AWS_ACCESS_KEY_ID =os.environ.get('AWS_ACCESS_KEY_ID')             #b2 application key id if using backblaze'
AWS_SECRET_ACCESS_KEY =os.environ.get('AWS_SECRET_ACCESS_KEY')     #your b2 application key
AWS_STORAGE_BUCKET_NAME =os.environ.get('AWS_STORAGE_BUCKET_NAME') #'<a public bucket>'
AWS_S3_REGION_NAME =os.environ.get('AWS_S3_REGION_NAME')           #'<your b2 region - e.g. us-west-001>'

AWS_S3_ENDPOINT = f's3.{AWS_S3_REGION_NAME}.backblazeb2.com'
AWS_S3_ENDPOINT_URL = f'https://{AWS_S3_ENDPOINT}'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': os.environ.get('CACHE_TIMEOUT', 60),  
    }
}


#STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT}/"
#django debug toolbar and other settings for development
if DEBUG:
    #if DEBUG is False then we are in production and we want to use postgres.  
    #Error will be raised if postgres is not available.
    #otherwise in development we want to use sqlite or postgres if available.
    if not(is_available.postgres_connection()):
        DATABASES['default'] = DATABASES['sqlite'] 

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    INTERNAL_IPS = ['127.0.0.1', ]

    
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

    #django storages settings for development
    #if USE_LOCAL_STORAGE is True then we will use local storage in development
    USE_LOCAL_STORAGE=os.environ.get('USE_LOCAL_STORAGE', False) == 'True'
    if USE_LOCAL_STORAGE:
        STATIC_URL='/static/'
        MEDIA_URL='/media/'
        STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
