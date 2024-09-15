from pathlib import Path
from .config import ELASTICSEARCH_DSL, MONGO_CONFIG, CORS_ALLOW_HEADERS, CORS_ALLOWED_ORIGINS, ENGINE, DJONGO_DB_NAME, DJANGO_DB_HOST, DJANGO_DB_PORT, SECRET_KEY, DEBUG, ALLOWED_HOSTS

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = SECRET_KEY
DEBUG = DEBUG
ALLOWED_HOSTS = ALLOWED_HOSTS

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_elasticsearch_dsl',
    'rest_framework',
    'corsheaders',
    'mic_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS
CORS_ALLOW_HEADERS = CORS_ALLOW_HEADERS

# Elasticsearch settings
ELASTICSEARCH_DSL = ELASTICSEARCH_DSL

# MongoDB Database configuration
MONGO_URI = MONGO_CONFIG['URI']
DB_NAME = MONGO_CONFIG['DB_NAME']
COLLECTIONS = MONGO_CONFIG['COLLECTION_NAME']

# Database settings
DATABASES = {
    'default': {
        'ENGINE': ENGINE,
        'NAME': DJONGO_DB_NAME,
        'HOST': DJANGO_DB_HOST,
        'PORT': DJANGO_DB_PORT,
    }
}

# Template settings
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

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Root URL configuration and WSGI application
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
