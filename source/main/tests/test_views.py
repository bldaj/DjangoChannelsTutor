from unittest.mock import patch

from django.contrib import auth
from django.test import TestCase
from django.urls import reverse

from main import forms
from main import models


class TestPage(TestCase):

    def test_home_page_works(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'BookTime')

    def test_about_us_page_works(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_us.html')
        self.assertContains(response, 'BookTime')

    def test_contact_us_page_works(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_form.html')
        self.assertContains(response, 'BookTime')
        self.assertIsInstance(response.context['form'], forms.ContactForm)

    def test_user_signup_page_loads_correctly(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertContains(response, 'BookTime')
        self.assertIsInstance(response.context['form'], forms.UserCreationForm)

    def test_user_signup_submission_works(self):
        post_data = {
            'email': 'user@domain.com',
            'password1': 'abcabcabc',
            'password2': 'abcabcabc'
        }

        with patch.object(forms.UserCreationForm, 'send_email') as mocked_send:
            response = self.client.post(
                reverse('signup'), post_data
            )
            self.assertEqual(response.status_code, 302)
            self.assertTrue(
                models.User.objects.filter(
                    email=post_data['email']
                ).exists()
            )
            self.assertTrue(
                auth.get_user(self.client).is_authenticated
            )
            mocked_send.assert_called_once()
