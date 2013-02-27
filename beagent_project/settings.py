# coding: utf-8

from local import *

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru-RU'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '8uk5r5nb7kvpo@b_vkw$zdk2s%)_jgwj9c_kctb!_gmf_35zuw'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'beagent_project.urls'

WSGI_APPLICATION = 'beagent_project.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'beagent',
    'easy_thumbnails',
    'beagent.templatetags',
)

AUTH_USER_MODEL = 'beagent.User'

AUTHENTICATION_BACKENDS = (
    'beagent.backends.Auth',
)

LOCAL = True
if LOCAL:
    SITE_URL = 'http://127.0.0.1:8000/'