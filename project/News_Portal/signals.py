from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from project.settings import SITE_URL
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import *


def send_mail(preview, pk, title, subscribers):
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


@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for cat in categories:
            subscribers += cat.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_mail(instance.preview(), instance.pk, instance.titel_name, subscribers)
