from django.test import TestCase
from django.urls import resolve
from lists.models import Item

from lists.views import home_page

class ItemModel(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
        
        
class HomePageTest(TestCase):
    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
    
    def test_root_url_page(self):
        root = resolve('/')
        self.assertEqual(root.func, home_page)
        
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
    def test_can_save_a_post_request(self):
        txt = 'A new list item'
        self.client.post('/', data={'item_text': txt})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, txt)
        
    def test_redirect_after_post(self):
        txt = 'A new list item'
        response = self.client.post('/', data={'item_text': txt})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
    
    def test_display_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        
        response = self.client.get('/')
        
        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
        