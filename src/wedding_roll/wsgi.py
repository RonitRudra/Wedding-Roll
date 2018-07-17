"""
WSGI config for wedding_roll project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# use "gunicorn --bind 0.0.0.0:8000 wedding_roll.wsgi" to run server via gunicorn
# Gunicorn should always be used to deploy production servers.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wedding_roll.settings.production")

application = get_wsgi_application()
