"""
WSGI config for CultoParaFamiliaDjango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from enums import enums
from whitenoise import WhiteNoise 
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{enums.SITE_NAME}.settings')

BASE_DIR = Path(__file__).resolve().parent.parent

application = get_wsgi_application()
application = WhiteNoise(application, root=f"{os.path.join(BASE_DIR, 'templates', 'static')}")
