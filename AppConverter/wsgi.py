"""WSGI config for AppConverter."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AppConverter.settings")
application = get_wsgi_application()
