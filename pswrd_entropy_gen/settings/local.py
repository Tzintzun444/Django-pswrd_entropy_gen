from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = ['127.0.0.1']

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"

SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(hours=12)
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(days=7)

LOGGING['root']['level'] = 'DEBUG'

RATELIMIT_ENABLE = False

SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
