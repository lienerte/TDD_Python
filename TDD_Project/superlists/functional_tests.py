"""
http://stackoverflow.com/questions/8255929/running-webdriver-chrome-with-selenium
https://sites.google.com/a/chromium.org/chromedriver/getting-started
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.http import HttpRequest

import time
import unittest



class NewVisitorTest(unittest.TestCase):
    #User enters the main site
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    #Browser then closes
    def tearDown(self):
        self.browser.quit()

    #Asked to enter a To-Do list; enter various items and save them
    def test_start_list_and_retrieve(self):
        self.browser.get('http://localhost:8000')
            #Header says To-Do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

            #To-Do list ready to be added to
        inputBox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputBox.get_attribute('placeholder'),
            'Enter a to-do item',
        )
            #Input is added to the text box
        inputBox.send_keys("Milk and cheese")
        #time.sleep(10)
        inputBox.send_keys(Keys.ENTER)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Milk and cheese', [row.text for row in rows])
        self.assertIn('2: Vegetables', [row.text for row in rows])
            #Option to add to another text box
            #Page updates and shows both on list
        self.fail('Finish the test')

if __name__ == '__main__':
    unittest.main()
