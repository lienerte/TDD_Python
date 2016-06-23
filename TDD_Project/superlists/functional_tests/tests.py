"""
http://stackoverflow.com/questions/8255929/running-webdriver-chrome-with-selenium
https://sites.google.com/a/chromium.org/chromedriver/getting-started
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.http import HttpRequest
from django.test import LiveServerTestCase

import time
import unittest



class NewVisitorTest(LiveServerTestCase):
    #User enters the main site
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    #Browser then closes
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    #Asked to enter a To-Do list; enter various items and save them
    def test_start_list_and_retrieve(self):
        self.browser.get(self.live_server_url)
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
        first_list_url = self.browser.current_url
        self.assertRegexpMatches(first_list_url, '/lists/.+')
        self.check_for_row_in_list_table("1: Milk and cheese")
        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys("Vegetables")
        inputBox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Milk and cheese', [row.text for row in rows])
        self.assertIn('2: Vegetables', [row.text for row in rows])
            #Option to add to another text box
            #Page updates and shows both on list

        #new user comes
        self.browser.quit()
        self.browser = webdriver.Chrome()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Milk and cheese', page_text)
        self.assertNotIn('2: Vegetables', page_text)

        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys("Lawn Mower")
        inputBox.send_keys(Keys.ENTER)

        second_list_url = self.browser.current_url
        self.assertRegexpMatches(second_list_url, '/lists/.+')
        self.assertNotEqual(second_list_url, first_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Vegetables", page_text)
        self.assertIn("Lawn Mower", page_text)
        self.fail('Finish the test')

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        inputBox = self.browser.find_element_by_id('id_new_item')
        inputBox.send_keys('testing\n')
        self.assertAlmostEqual(
            inputBox.location['x'] + inputBox.size['width'] / 2,
            512,
            delta = 5
        )

if __name__ == '__main__':
    unittest.main()
