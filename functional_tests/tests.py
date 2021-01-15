from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
    
    # 辅助方法
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # 测试方法
    def test_can_start_a_list_and_retrieve_it_later(self):
        # open index  
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # in text input "Buy Fish"
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'  
        )
        inputbox.send_keys('Buy Fish')
        # ENTER
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # IN text output "1: Buy Fish"
        self.check_for_row_in_list_table('1: Buy Fish')
        # in text input "Buy rice"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy rice')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # ENTER
        self.check_for_row_in_list_table('1: Buy Fish')
        self.check_for_row_in_list_table('2: Buy rice')
        # in text output "2: Buy rice"
        self.fail('Finish the test')
        # output the only URL
