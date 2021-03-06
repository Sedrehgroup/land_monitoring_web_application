import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x&m%i30j%q-&be1f)6x15g5nyszn*hg=nc)m4au8+$$=jyxck$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'download_images.apps.DownloadImagesConfig',
    'image_analysis.apps.ImageAnalysisConfig',
    'geoserver.apps.GeoserverConfig',
    # third party packages
    'django_celery_beat',
    'rest_framework',
    'corsheaders',
    'storages',
]

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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


POSTGRESQL = {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': os.environ.get('DB_NAME'),
    'USER': os.environ.get('DB_USER'),
    'PASSWORD': os.environ.get('DB_PASS'),
    'HOST': os.environ.get('DB_HOST'),
    'PORT': os.environ.get('DB_PORT'),
    'SCHEMA': os.environ.get('DB_SCHEMA'),
}

DATABASES = {
    'default': POSTGRESQL
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GEOSERVER = {
    'HOST': os.environ.get('GEOSERVER_HOST'),
    'IP': os.environ.get('GEOSERVER_HOST_IP'),
    'USERNAME': os.environ.get('GEOSERVER_USERNAME'),
    'PASSWORD': os.environ.get('GEOSERVER_PASSWORD'),
    'WORKSPACE': os.environ.get('GEOSERVER_WORKSPACE'),
    'NAMESPACE': os.environ.get('GEOSERVER_NAMESPACE'),
    'MEDIA_ROOT': 'media/geoserver/',
    'RASTER_URL': os.path.join(BASE_DIR, 'images'),
    'GEOSERVER_URL': '/opt/geoserver/data_dir',
    'PORT': os.environ.get('GEOSERVER_PORT')
}

CORS_ORIGIN_ALLOW_ALL = True

# arvan cloud storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = '48eff7b6-df4d-421d-aaf4-c27a7cae8cd9'
AWS_SECRET_ACCESS_KEY = 'e8bf430121a86ab69b9b24539444ff154bc7d59dce0c5fe9dd8f4fced82d77a2'
AWS_S3_ENDPOINT_URL = 'https://s3.ir-thr-at1.arvanstorage.com'
AWS_STORAGE_BUCKET_NAME = 'landmonitoring'
AWS_SERVICE_NAME = 's3'
AWS_S3_FILE_OVERWRITE = True