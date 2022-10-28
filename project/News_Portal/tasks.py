from celery import shared_task
import time
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from project.settings import SITE_URL
from django.conf import settings
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import *

#
#
# @shared_task
# def send_mail():
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': Post.preview,
#             'Link': f'{SITE_URL}/news/{pk}',
#         }
#     )
#     msg = EmailMultiAlternatives(
#         subject=Post.objects.titel_name,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers,
#     )
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()


# @receiver(post_save, sender=PostCategory)
@shared_task
def notify_new_post(sender, instance, created, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for cat in categories:
            subscribers += cat.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_mail(instance.preview(), instance.pk, instance.titel_name, subscribers)


post_save.connect(notify_new_post, sender=PostCategory)



@shared_task
def sendsend(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'Link': f'{SITE_URL}/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
