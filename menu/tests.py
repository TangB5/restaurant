from django.test import TestCase

from .models import Plat
# Create your tests here.
class PlatTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Plat.objects.create(
            categorie="dessert",
            nom='abrico a la fraise',
            description='rafraichisant et sucree',
            prix=1200,

        )