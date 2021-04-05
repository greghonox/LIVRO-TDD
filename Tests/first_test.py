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
        
        txt = 'Buy peacock feathers'
        
        inputbox = self.dr.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')
        inputbox.send_keys(txt)
        inputbox.send_keys('\n')
        
        print('ESPERANDO PARA SEGUIR O TESTE')
        sleep(5)
        
        table = self.dr.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: ' + txt, [row.text for row in rows])
        # self.fail('Finish tests')
  
    def tearDown(self) -> None:
        self.dr.quit()
