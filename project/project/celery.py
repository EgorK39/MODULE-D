import os
from celery import Celery
from celery.schedules import crontab

# from News_Portal.tasks import printer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'News_Portal.tasks.printer',
#         'schedule': 5,
#         'args': (5,),
#     },
# }
app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'News_Portal.tasks.sendsend',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        'args': ['preview', 'pk', 'title', 'subscribers'],
    },
}
