# -*- coding: utf-8 -*-
import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


HOST = 'developer.gobelieve.io'


class TestPage(unittest.TestCase):
    port = 80
    driver = None
    share = dict()

    def test_00_server_is_up_and_running(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        # https://sites.google.com/a/chromium.org/chromedriver/getting-started
        # driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    @classmethod
    def get_server_url(cls, path=''):
        """
        Return the url of the test server
        """
        return 'http://%s%s%s' % (
            HOST if HOST else 'localhost', ':' + str(cls.port) if cls.port != 80 else '', '/' + path if path else '')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_index(self):
        driver = self.driver
        driver.get(self.get_server_url())
        self.assertEqual(driver.title, '')

    def test_02_login(self):
        driver = self.driver
        # Opening the link we want to test
        driver.get(self.get_server_url('login'))

        # find the form element
        email = driver.find_element_by_id('email')

        password = driver.find_element_by_id('password')

        submit = driver.find_element_by_link_text(u'登录')

        # Fill the form with data
        email.send_keys('demo@gobelieve.io')
        password.send_keys('111111')
        # submitting the form
        submit.send_keys(Keys.RETURN)

        # check the returned result
        wait = WebDriverWait(driver, 10)
        wait.until(expected_conditions.title_is(u'gobelieve即时通讯'))
        self.assertEqual(self.get_server_url('im'), driver.current_url)

    def test_03_im_index(self):
        driver = self.driver
        # Opening the link we want to test
        driver.get(self.get_server_url('im'))
        self.assertIn(u'SDK测试', driver.page_source)

    def test_04_im_detail(self):
        driver = self.driver
        # Opening the link we want to test
        driver.get(self.get_server_url(u'im/game/detail/7?game=7&name=SDK测试'))

        self.assertIn(u"App Key", driver.page_source)
        self.assertIn(u"App Secret", driver.page_source)