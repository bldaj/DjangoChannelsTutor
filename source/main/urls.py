from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html')),
    path('about-us/', TemplateView.as_view(template_name='about_us.html')),
]
