from django.views.generic import FormView

from main import forms


class ContactUsView(FormView):
    template_name = 'contact_form.html'
    form_class = forms.ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
