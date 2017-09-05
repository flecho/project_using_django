"""
WSGI config for drugfinder project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drugfinder.settings")

application = get_wsgi_application()



'''
	2017/08/21

	WSGI servers obtain the path to the apllication callable from their configuration. 
	Django's built-in server, namely the runserver command, reads it from the WSGI_APPLICATION setting. 
	By default, it's set to <project_name>.wsgi.application, which points to the application callable in <project_name>/wsgi.py

'''
