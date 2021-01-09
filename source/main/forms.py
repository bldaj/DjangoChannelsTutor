import logging

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    UserCreationForm as DjangoUserCreationForm,
    UsernameField,
)
from django.core.mail import send_mail

from main import models

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    message = forms.CharField(max_length=600, widget=forms.Textarea)

    def send_email(self):
        logger.info('Sending email to customer service')
        
        message = f"From {self.cleaned_data['name']}\n{self.cleaned_data['message']}"
        send_mail(
            'Site message',
            message,
            'example@example.com',
            ['jovarec891@iopmail.com'],
            fail_silently=False
        )


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = models.User
        fields = ('email',)
        field_classes = {'email': UsernameField}

    def send_email(self):
        logger.info(f"Sending signup email for email={self.cleaned_data['email']}")

        message = f"Welcome {self.cleaned_data['email']}"
        send_mail(
            'Welcome to BookTime',
            message,
            'example@example.com',
            [self.cleaned_data['email']],
            fail_silently=True,
        )


class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        strip=False, widget=forms.PasswordInput
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user = authenticate(
                self.request, email=email, password=password
            )
            if self.user is None:
                raise forms.ValidationError(
                    'Invalid email/password combination.'
                )
            logger.info(
                f'Authentication successful for email {email}'
            )

        return self.cleaned_data

    def get_user(self):
        return self.user
