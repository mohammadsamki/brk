"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-37-4s(juv*056khn(-u62oqk2l$lkt^#(1r7x0l+9p$=h%k1!8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['185.177.59.47','b-clubs.com','www.bclubscm.cm','www.bclubscm.cm','www.bcllub.mp','bcllub.mp','www.bclubc.mp','bclubc.mp','biub.mp','www.biub.mp','www.b-clubs.com','briansclubcm.mp','www.bclub.cc','bclubcm.mp','145.239.98.12','bclubcc.mp','https-briansclub.bclub.cc','bclub.briansclub.mp','b-club.mp', 'briansclub.bclub.cc', 'official.bclub.cc', 'store.bclub.cc', 'store.bclun.cc', 'shop.bclub.cc', 'mp.bclub.cc', 'cm.bclub.cc', 'bclub.briansclub.mp'
'bclubcc.mp', 'bclub.cm.bclub.cc', 'ww25.bclub.cc', 'bclub.cc', 'www.briansclub.net', 'briansclub.net', 'bclub.org', 'briancrab.com', 'briansclubs.mp', 'brinsclub.com', 'brianszclub.cc', 'bclubs.us', 'brainsclubc.cm', 'brianscclub.com', 'brianclub.io',
                 'brianscleb.com', 'briansclub.com.cm', 'briansclub.fr',
                 'briascluz', ' ', 'brlansclub.net', 'brlansclub.store',
                 'mp.bclub.cc', 'briansclubl.cm', 'briansclub.mp', 'briansclubn.cm',
                 'briansclub.bclub.cc', 'briansclubv.cm', 'briansclubx.cm', 'briansclubz.cm',
                 'briansclup.cm', 'brianscreb.cm', 'bclubc.cm', 'bclubcc.com',
                 'brlansclubs.com', 'brlansclub.store', 'brlansclub.net', 'https-bclub.com',
                 '79.137.207.210', 'bclubcc.com', 'briansclubl.cm', 'bclubc.cm', 'briansclub.io',
                 'briansculb.cm', 'briansclubz.cm', 'briansclub.mp', 'briansclubc.cm',
                 '127.0.0.1', 'localhost']

# AUTH_USER_MODEL = 'api.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'briansclub',
    'crispy_forms',
    'django.contrib.sitemaps',
    'payment',
    'rest_framework',

    'api',
    'captcha',
    'sslserver',
    "django_check_seo",
    # 'django.contrib.sites',
    # 'seo',

    # 'meta',

]
RECAPTCHA_PUBLIC_KEY = '6Lc6V_MnAAAAACMrPkASj9P1Q3Jp4BKVdLFhV_f1'
RECAPTCHA_PRIVATE_KEY = '6Lc6V_MnAAAAAFL_jNFHTsrTCy51pxDmt47qbBl2'

CRONJOBS = [
    ('0 */2 * * *', 'briansclub.tasks.send_auto_reply', '>> /tmp/cron.log')
]
# SITE_ID = 1
CRISPY_TEMPLATE_PACK = 'bootstrap4'

ASGI_APPLICATION = 'DjangoBlog.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'briansclub.middleware.RequestLoggerMiddleware',
    'briansclub.inactive_user_middleware.InactiveUserMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'meta.middleware.MetaMiddleware',
        # 'briansclub.middleware.BlockCurlMiddleware',
                    # 'briansclub.middleware.RedirectMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]
# settings.py
from django.http import HttpRequest

CSRF_COOKIE_SECURE = False

CORS_ALLOWED_ORIGINS = [
    'https://briansclubc.cm',
]

CSRF_TRUSTED_ORIGINS = [
    'https://briansclubc.cm'
]

# CSRF_COOKIE_SECURE = False
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'briancom',
        'USER': 'samaki',
        'PASSWORD': 'Xh%B&8RuhQ+r34HG1',
        'HOST': '128.140.116.14',
        'PORT': '',

    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'briancom',
#         'USER': 'sam',
#         'PASSWORD': 'Xh%B&8RuhQ+r34HG',
#         'HOST': 'postgresql-166513-0.cloudclusters.net',
#         'PORT': '18442',

#     }
# }
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'tasklist'
CORS_ALLOW_ALL_ORIGINS = True  # Be cautious with this in production!


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = 'static/'
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAdminUser',
#     ],
# }
# CSRF_COOKIE_DOMAIN = '127.0.0.1'
# TIME_FORMAT = 'H:i'
# DATE_FORMAT = 'Y-m-d'
# DATETIME_FORMAT = 'Y-m-d H:i'
# SECURE_SSL_REDIRECT = True
# # SESSION_COOKIE_SECURE = True
# # CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_DOMAIN = 'bclub.cc'
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = 'bclub.cc'
CSRF_TRUSTED_ORIGINS = ['https://*.bclub.cc', 'https://*.bclub.cc', 'https://bclub.cc']

