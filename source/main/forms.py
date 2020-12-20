import logging

from django import forms
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
