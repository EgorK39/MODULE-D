from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm
from django.core.mail import EmailMultiAlternatives
from project.settings import DEFAULT_FROM_EMAIL, SITE_URL
from django.template.loader import render_to_string
from News_Portal.models import *


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        authors = Group.objects.get(name='authors')
        user.groups.add(authors)

        html_content = render_to_string(
            'reg_post.html',
            {
                'Link': f'{SITE_URL}/news/',
            }
        )

        msg = EmailMultiAlternatives(
            subject='Вы успешно зарегистрированы',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        return user
