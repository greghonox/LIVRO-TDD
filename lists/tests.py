from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

class HomePageTest(TestCase):
    def test_root_url_page(self):
        root = resolve('/')
        self.assertEqual(root.func, home_page)