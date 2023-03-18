from tixvana.settings import *

DEBUG = True

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: update this when you have the production host
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(
    BASE_DIR / 'media'
)


EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_USE_SSL = True
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')