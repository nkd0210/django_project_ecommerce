from pathlib import Path
import cloudinary
import dj_database_url
import mongoengine
import os
from decouple import config
from rest_framework.pagination import PageNumberPagination

mongoengine.connect(
    db='mobiledb',
    host='localhost',
    port=27017,
    alias='default'  
)

mongoengine.connect(
    db='bookdb',  
    host='localhost',  
    port=27017,  
    alias='book_db'
)

mongoengine.connect(
    db='mobiledb',
    host='localhost',
    port=27017,
    alias='mobile_db'
)

mongoengine.connect(
    db='clothesdb',
    host='localhost',
    port=27017,
    alias='clothes_db'
)

mongoengine.connect(
    db='shoesdb',
    host='localhost',
    port=27017,
    alias='shoes_db'
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'  # URL to access the media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS =  ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'cloudinary',
    'cloudinary_storage',
    'customer',
    'book',
    'cart',
    'order',
    'paying',
    'shipping',
    'mobile',
    'shoes',
    'clothes',
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

ROOT_URLCONF = 'dung_project2.urls'

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

WSGI_APPLICATION = 'dung_project2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mysql_customer': dj_database_url.config(default=config('MYSQL_URL')),
    'mongo_book': {
        'ENGINE': '',  
        'NAME': 'bookdb',  
        'HOST': 'localhost',  
        'PORT': 27017,  
    },
    'mongo_mobile': {
        'ENGINE': '',  
        'NAME': 'mobiledb',  
        'HOST': 'localhost',  
        'PORT': 27017,  
    },
    'mongo_clothes': {
        'ENGINE': '',  
        'NAME': 'clothesdb',  
        'HOST': 'localhost',  
        'PORT': 27017,  
    },
    'mongo_shoes': {
        'ENGINE': '',  
        'NAME': 'shoesdb',  
        'HOST': 'localhost',  
        'PORT': 27017,  
    },
    'postgres_cart': dj_database_url.config(default=config('POSTGRES_URL_CART')),
    'postgres_order': dj_database_url.config(default=config('POSTGRES_URL_ORDER')),
}

DATABASE_ROUTERS = [
    'dung_project2.routers.CustomerRouter',
    'dung_project2.routers.BookRouter',
    'dung_project2.routers.CartRouter',
    'dung_project2.routers.OrderRouter',
]


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
