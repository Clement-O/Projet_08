"""
WSGI config for purbeurre project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Third party import
from dotenv import load_dotenv

load_dotenv()

if os.environ.get('ENV') == 'PRODUCTION':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'purbeurre.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'purbeurre.settings')

application = get_wsgi_application()
