from decimal import Decimal

from  django.test import TestCase

from main import models


class TestModel(TestCase):

    def test_active_manager_works(self):
        models.Product.objects.create(
            name='Test',
            price=Decimal('10'),
        )
        models.Product.objects.create(
            name='Test',
            price=Decimal('10'),
            active=False
        )

        self.assertEqual(
            len(models.Product.objects.active()), 1
        )
