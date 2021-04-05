from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class HomePageTest(TestCase):
    def test_root_url_page(self):
        root = resolve('/')
        self.assertEqual(root.func, home_page)
        
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
    def test_can_save_a_post_request(self):
        txt = 'A new list item'
        response = self.client.get('/', data={'item': txt})
        self.assertIn(txt, response.content.decode())
        self.assertTemplateUsed(response, 'home.html')