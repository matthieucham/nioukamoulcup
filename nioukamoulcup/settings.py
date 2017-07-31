"""
Django settings for nioukamoulcup project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
# from accounts.models import GamerProfile

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+8(y4pj(v%!phea+a43dmy)&b^8!7#vm2i%e%7bx71(fj9asd7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

INTERNAL_IPS = [
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # 'debug_toolbar',

    'rules.apps.AutodiscoverRulesConfig',
    'inline_actions',

    # dj-userena
    #'userena',
    #'guardian',
    #'easy_thumbnails',


    'mptt',
    'tagging',
    'zinnia',
    'django_comments',

    # dj-wiki
    # 'django_nyt',
    # 'sekizai',
    # 'sorl.thumbnail',
    # 'wiki',
    # 'wiki.plugins.attachments',
    # 'wiki.plugins.notifications',
    # 'wiki.plugins.images',
    # 'wiki.plugins.macros',

    'graphos',

    'colorful',
    'svg',

    'rest_framework',

    'game',
    #'accounts',
    'ligue1',

    'webpack_loader',
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    # 'userena.backends.UserenaAuthenticationBackend',
    # 'guardian.backends.ObjectPermissionBackend',
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'nioukamoulcup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'zinnia.context_processors.version',  # Optional
                'sekizai.context_processors.sekizai',
            ],
            'loaders': [
                'app_namespace.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

# TEMPLATE_CONTEXT_PROCESSORS = ['django.contrib.auth.context_processors.auth']

WSGI_APPLICATION = 'nioukamoulcup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    # 'default': {
    # 'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nioukamoulcup',
        'USER': 'nioukamoulcupuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    # 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
    # We do this so that django's collectstatic copies or our bundles to the STATIC_ROOT or syncs them to whatever storage we use.
)
# STATIC_URL = 'http://localhost:82/www/static/'
STATIC_URL = '/static/'
STATIC_ROOT = 'D:\dev\git\www\static'
MEDIA_URL = '/media/'
MEDIA_ROOT = 'D:\dev\git\www\media'

# Sites framework : https://docs.djangoproject.com/en/1.10/ref/contrib/sites/
SITE_ID = 1

# Required by Guardian
ANONYMOUS_USER_ID = -1

# For django-wiki customization
WIKI_ACCOUNT_HANDLING = False
WIKI_MAX_REVISIONS = 20

# Required by Userena
AUTH_PROFILE_MODULE = 'accounts.GamerProfile'
USERENA_SIGNIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATNUTS_CLIENT_ID = 'aLUoUeBI9Zuj7?JfC0t9U=P3mycANITG@0hvaQlZ'
STATNUTS_SECRET = 'GsHk=.o2kTu9WkU!a:n1kqkQogZ4lXWitDGn2bZff=?YcdbI-;6h_Grusn@q56@;ttN9OMa9.dWcuBq4lJ8vu7;I9n_f:kJrZ5RUSNkAan088KLyv..7q_.Me94MB?Dy'
STATNUTS_URL = 'https://statnuts-kcup.rhcloud.com'


WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}