from time import sleep
from unittest import TestCase
from selenium import webdriver
from django.http import HttpResponse


class Test_tdd(TestCase):
    def setUp(self) -> None:
        self.dr = webdriver.Chrome()
    
    def test_title(self) -> None:
        'HISTORIA DO USUARIO'
        
        self.dr.get('http://localhost:8000')
        self.assertIn('To-Do list', self.dr.title)
        
        head_text = self.dr.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', head_text)
        
        inputbox = self.dr.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys('\n')
        sleep(5)
        
        table = self.dr.find_element_by_id('id_list_table')
        self.assertTrue(
            any(x.text == '1: Buy peacock feathers' for x in table)
        )
        self.fail('Finish tests')
    
    def test_home_page_returns_correct_html(self):
        request = HttpResponse()
        response = home_page(request)
        html = response.content.decode('utf-8')
        expected_html = render_to_string('home.html')        
        self.assertEqual(html, expected_html)
        
    def tearDown(self) -> None:
        self.dr.quit()
