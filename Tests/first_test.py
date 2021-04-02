from selenium import webdriver
from unittest import main, TestCase

class Test_tdd(TestCase):
    def setUp(self) -> None:
        self.dr = webdriver.Chrome()
    
    def test_title(self) -> None:
        'HISTORIA DO USUARIO'
        
        self.dr.get('http://localhost:8000')
        self.assertIn('Django', self.dr.title)
        
    def tearDown(self) -> None:
        self.dr.quit()
