# coding: utf-8

import os

def local_path(path):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), path))

PRODUCTION = False

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Roman Dynin', 'deromanok@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'beagent',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '',
        'PORT': '',
    }
}

MEDIA_URL = '/media/'

MEDIA_ROOT = local_path('media')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    local_path('static'),
)

TEMPLATE_DIRS = (
    local_path('templates'),
)