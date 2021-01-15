from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# open index  
		self.browser.get('http://localhost:8000')
		
		self.assertIn('To-Do', self.browser.title)
		self.fail("Finish the test!")
		
		# in text input "Buy Fish"
		# ENTER
		# IN text output "1: Buy Fish"
		# in text input "Buy rice"
		# ENTER
		# in text output "2: Buy rice"
		
		# output the only URL


if __name__ == '__main__':
	unittest.main()
