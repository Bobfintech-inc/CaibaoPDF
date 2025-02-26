
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

print("Celery Configuration:")
for key, value in app.conf.items():
    if key.startswith('CELERY_'):
        print(f"{key}: {value}")