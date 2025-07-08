from .base import *

DEBUG = False
ALLOWED_HOSTS = ['testserver']

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_USE_TLS = False

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(minutes=1)
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(minutes=5)

RATELIMIT_ENABLE = False

LOGGING['root']['level'] = 'CRITICAL'
