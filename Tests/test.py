from time import sleep
from unittest import TestCase
from selenium import webdriver
from django.test import LiveServerTestCase

class Test_tdd(LiveServerTestCase):
    def setUp(self) -> None:
        self.dr = webdriver.Chrome()
        
    def check_for_row_in_list_table(self, raw_text):
        table = self.dr.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(raw_text, [row.text.split(':')[-1].strip() for row in rows])
    
    def test_title(self) -> None:
        'HISTORIA DO USUARIO'
        
        self.dr.get(self.live_server_url)
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
        self.check_for_row_in_list_table(txt)

        # self.fail('Finish tests')
  
    def tearDown(self) -> None:
        self.dr.quit()
