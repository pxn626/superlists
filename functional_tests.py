from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # open index  
        self.browser.get('http://localhost:8000')
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
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy Fish' for row in rows),
            f"New ti-do item did not appear in table. Contents were:\n{table.text}"
        )
        # in text input "Buy rice"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy rice')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # ENTER
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy Fish', [row.text for row in rows])
        self.assertIn('2: Buy rice', [row.text for row in rows])
        
        # in text output "2: Buy rice"
        self.fail('Finish the test')
        # output the only URL


if __name__ == '__main__':
    unittest.main()
