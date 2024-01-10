"""
Django settings for cms project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
# import os/
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+ht(2i)#k7mw1nvdw$7qcfyw@02&zd#*^k28spr1-!2t#!f@jj'

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
    'cmsapp',
    'ckeditor',
    'django_extensions',
    'dashboard',
    'crispy_forms',
    "debug_toolbar"
]
CKEDITOR_UPLOAD_PATH = 'uploads/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'cms.urls'


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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

WSGI_APPLICATION = 'cms.wsgi.application'

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
}
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'NAME': str(BASE_DIR / "db.sqlite3"),
    }
}
AUTH_USER_MODEL = "cmsapp.User" 
SITE_URL = 'https://127.0.0.1:8000'
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",

]
STATIC_ROOT ='/static/'

CKEDITOR_IMAGE_BACKEND = 'pillow'
MEDIA_URL = '/media/'
MEDIA_ROOT= BASE_DIR/'media'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'piinnovations1@gmail.com'
EMAIL_HOST_PASSWORD = 'amrbaqgxlnwsdgtx'   
# CKEDITOR_CONFIGS = {
#     'default': {
#         'skin': 'moono',
#         'toolbar_MyCustomToolbar': [
#             {'name': 'basic', 'items': [
#                 'Source',
#                 '-',
#                 'Bold',
#                 'Italic',
#                 'CodeSnippet' ,
#                 'Image',
#                 'Media'
#                 # 'image' # add the codesnippet button name
#             ]}
#         ],

#         'codeSnippet_theme': 'monokai',
        
#         # uncomment to restrict only those languages
#         'codeSnippet_languages': {
#             'python': 'Python',
            
            
            
#         },
#         'toolbar': 'MyCustomToolbar',
#         'extraPlugins': ','.join(
#             [
#                 # add the follow plugins
#                 'codesnippet',
#                 'widget',
#                 'dialog',
#                 'image'
#             ]),
#     }
# }
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_MyCustomToolbar': [
            {'name': 'basic', 'items': [
                'Source',
                '-',
                'Bold',
                'Italic',
                'CodeSnippet' ,
                'FontSize',  # Added FontSize here
                'Image',
                'Media',
            ]}
        ],

        'codeSnippet_theme': 'monokai',

        # uncomment to restrict only those languages
        'codeSnippet_languages': {
            'python': 'Python',
        },
        'toolbar': 'MyCustomToolbar',
        'extraPlugins': ','.join(
            [
                # add the follow plugins
                'codesnippet',
                'widget',
                'dialog',
                'image'
            ]),
    }
}

