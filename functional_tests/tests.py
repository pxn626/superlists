# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import os


MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        
    def tearDown(self):
        self.browser.quit()
    
    # 辅助方法
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                # table = self.browser.find_element_by_id('id_nothing')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                # self.assertIn('foo', [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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
        self.wait_for_row_in_list_table('1: Buy Fish')
        # in text input "Buy rice"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy rice')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        # ENTER
        self.wait_for_row_in_list_table('1: Buy Fish')
        self.wait_for_row_in_list_table('2: Buy rice')
        # in text output "2: Buy rice"
        # self.fail('Finish the test')
        # output the only URL

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy ball')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy ball')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # 另一个人来访问本站
        # 先退出之前的
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 打开首页
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Fish', page_text)
        self.assertNotIn('Buy rice', page_text)

        # 输入自己的带帮事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # 获取惟一的URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Fish', page_text)
        self.assertIn('Buy milk', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
