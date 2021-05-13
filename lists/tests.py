from django.test import TestCase
from django.urls import resolve
from lists.models import Item, List

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
        
        
class NewListTest(TestCase):
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
        self.client.post('/lists/new', data={'item_text': txt})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, txt)
        
    def test_redirect_after_post(self):
        txt = 'A new list item'
        response = self.client.post('/lists/new', data={'item_text': txt})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
    

class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()
        
        saved_item = List.objects.first()
        self.assertEqual(saved_item, list_)
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.list, list_)
        

class ListViewTest(TestCase):
    def test_users_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
        
    def test_display_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
    
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        
        response = self.client.get(f'/lists/{correct_list.id}/')
        
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
        
    def test_can_save_a_post_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        text = 'A new item for an existing list'
        self.client.post(
            f'/lists/{correct_list.id}/add_item', 
            data={'item_text', text}
        )
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, text)
        self.assertEqual(new_item.list, correct_list)
        
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            f'/lists/{correct_list.id}/add_item', 
            data={'item_text': 'A new item for an existing list'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
        
        