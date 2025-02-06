from .base import *  # noqa
from .base import env
from decouple import config

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
# DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="8OmLatOrLmWP8ujI6JiuIxGhfjGB87ULLpWxwzvY03Jr50bMs9wjEdgyKTNDlVJV",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "django", "it245151.uni-graz.at"]
# ALLOWED_HOSTS = ["167.99.251.188"]
# ALLOWED_HOSTS = ["cc-explorer.com", "api.cc-explorer.com", "167.99.251.188", "django"]


CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8080",
    "http://localhost:81",
    "http://frontend:81",
    "http://167.99.251.188:81",
    "http://167.99.251.188",
    "https://cc-explorer.com",
    "https://api.cc-explorer.com",
    "https://ml.cc-explorer.com",
    "https://it245151.uni-graz.at"
    ]
# CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = ['https://it245151.uni-graz.at']

# Important for running behind a proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
# EMAIL_PORT = 587
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = "CC-Explorer ccexplorerdemo@gmail.com"
EMAIL_HOST_PASSWORD=config("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER=config("EMAIL_HOST_USER")
DOMAIN=config("DOMAIN")


# ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# DOMAIN = "localhost:8080"
# DOMAIN = "cc-explorer.com"
# DOMAIN = "it245151.uni-graz.at"


DJOSER = {
    'SEND_ACTIVATION_EMAIL' : True,
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    "SERIALIZERS": {
        "current_user" : "biocrust_app.users.serializers.UserSerializer"
    }
}

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa: F405


# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

if not DEBUG and env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa: F405

# Your stuff...
# ------------------------------------------------------------------------------
