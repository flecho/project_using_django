import os
from celery import Celery
#from django.conf import settings

'''
	The Celery app we created in the proejct root will collect all tasks defined across all Django apps listed in the INSTALLED_APPS configuration.
'''

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drugfinder.settings')

app = Celery('drugfinder', backend='amqp', broker='amqp://flecho:wnstkd003!@localhost:5672/aitrics_vhost')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

'''
		The broker parameter specifies the URL needed to connect to our broker. In our case, this is the RabbitMQ service that is running on our server. RabbitMQ operates using a protocol called "amqp". If RabbitMQ is operating under its default configuration, celery can connect with no other information other than the amqp:// scheme.
'''
