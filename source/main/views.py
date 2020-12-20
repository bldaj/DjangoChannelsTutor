import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from main import forms
from main import models

logger = logging.getLogger(__name__)


class ContactUsView(FormView):
    template_name = 'contact_form.html'
    form_class = forms.ContactForm
    success_url = '/'

    def form_valid(self, form: forms.ContactForm):
        form.send_email()
        return super().form_valid(form)


class ProductListView(ListView):
    template_name = 'main/product_list.html'
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None

        if tag != 'all':
            self.tag = get_object_or_404(
                models.ProductTag, slug=tag
            )

        if self.tag:
            products = models.Product.objects.active().filter(
                tags=self.tag
            )
        else:
            products = models.Product.objects.active()

        return products


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to = self.request.GET.get('next', '/')
        return redirect_to

    def form_valid(self, form: forms.UserCreationForm):
        response = super().form_valid(form)
        form.save()

        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        logger.info(f'New signup for email={email}')

        user = authenticate(email=email, password=raw_password)
        login(self.request, user)

        form.send_email()

        messages.info(
            self.request, 'You signed up successfully/.'
        )

        return response
