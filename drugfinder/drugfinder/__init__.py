from .celery import app as celery_app

__all__ = ['celery_app']

# This will make sure our Celery app is important every time Django starts.
