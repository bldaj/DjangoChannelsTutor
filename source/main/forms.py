from django import forms
from django.core.mail import send_mail
import logging

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
