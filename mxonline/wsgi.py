"""
WSGI config for mxonline project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import time
import traceback
import signal
import sys

sys.path.append('/opt/djangostack-1.9.7-0/apps/django/django_projects/mxonline')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/djangostack-1.9.7-0/apps/django/django_projects/mxonline/egg_cache")


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mxonline.settings")





try:
    application = get_wsgi_application()
    print 'WSGI without exception'
except Exception:
    print 'handling WSGI exception'
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)