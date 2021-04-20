from time import sleep, time
from unittest import TestCase
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class Test_tdd(LiveServerTestCase):
    def setUp(self) -> None:
        self.dr = webdriver.Chrome()
        
    def test_can_start_a_list_for_one_user(self):
        self.dr.get(self.live_server_url)
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers to make a fly')
    
    def test_mutiple_users_can_start_listers_at_different_url(self):
        self.dr.get(self.live_server_url)
        inputbox = self.dr.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys('\n')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
        edith_list_url = self.dr.current_url
        self.assertRegex(edith_list_url, '/list/.+')
        self.dr.quit()
        
        self.dr = webdriver.Chrome()
        self.dr.get(self.live_server_url)
        page_text = self.dr.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        
        inputbox = self.dr.find_element_by_id('id_new_item')
        inputbox.send_keys('By milk')
        inputbox.send_keys('\n')
        self.wait_for_row_in_list_table('1: Buy milk')
        
        francs_list_url = self.dr.current_url
        self.assertRegex(francs_list_url, '/list/.+')
        self.assertNotEqual(francs_list_url, edith_list_url)
        
        page_text = self.dr.fin_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        
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
        self.wait_for_row_in_list_table(txt)
        self.check_for_row_in_list_table(txt)

        # self.fail('Finish tests')
  
    def tearDown(self) -> None:
        self.dr.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time()
        c = 0
        while True:
            try:
                print(f'TENTANDO ENCONTRAR ELEMENTO {c} "{row_text}"')
                c += 1
                table = self.dr.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn("1: " + row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time() - start_time > MAX_WAIT: raise e
                sleep(.5)