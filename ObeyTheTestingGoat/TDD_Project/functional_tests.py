"""
http://stackoverflow.com/questions/8255929/running-webdriver-chrome-with-selenium
https://sites.google.com/a/chromium.org/chromedriver/getting-started
"""

from selenium import webdriver
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
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test')

    def test

if __name__ == '__main__':
    unittest.main()
