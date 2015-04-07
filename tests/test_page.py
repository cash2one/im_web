# -*- coding: utf-8 -*-
import unittest
import multiprocessing
import time
import os
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from gevent.wsgi import WSGIServer

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_PATH)

from www import app
from config import SESSION_COOKIE_DOMAIN

HOST = SESSION_COOKIE_DOMAIN


class TestPage(unittest.TestCase):
    _process = None
    port = 5000
    app = None
    driver = None
    share = dict()

    def test_00_server_is_up_and_running(self):
        response = requests.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)

    @staticmethod
    def serve(application, port):
        http_server = WSGIServer(('', port), application)
        http_server.serve_forever()

    @classmethod
    def setUpClass(cls):
        cls._process = None

        # Get the app
        cls.app = cls.create_app()

        cls.port = 5000  # Default
        if 'LIVESERVER_PORT' in cls.app.config:
            cls.port = cls.app.config['LIVESERVER_PORT']

        cls._process = multiprocessing.Process(
            target=cls.serve, args=(cls.app, cls.port)
        )

        cls._process.start()

        # we must wait the server start listening
        time.sleep(1)

        cls.driver = webdriver.Firefox()
        # https://sites.google.com/a/chromium.org/chromedriver/getting-started
        # driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls._process.terminate()

    @classmethod
    def get_server_url(cls, path=''):
        """
        Return the url of the test server
        """
        return 'http://%s:%s%s' % (HOST if HOST else 'localhost', cls.port, '/' + path if path else '')

    @classmethod
    def create_app(cls):
        app.config['DEBUG'] = False
        app.config['TESTING'] = True
        # app.config['APP_MODE'] = 'Development'
        # Default port is 5000
        app.config['LIVESERVER_PORT'] = 8943
        return app

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
        email.send_keys('biohfj@gmail.com')
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

    def test_05_im_add(self):
        driver = self.driver
        # Opening the link we want to test
        driver.get(self.get_server_url('im/game/add?offset=0'))

        # find the form element
        name = driver.find_element_by_id('name')
        android = driver.find_element_by_class_name('android')
        android_identity = driver.find_element_by_name('android_identity')

        ios = driver.find_element_by_class_name('ios')
        ios_identity = driver.find_element_by_name('ios_identity')

        sandbox_key = driver.find_element_by_id('develop_apns')
        sandbox_key_secret = driver.find_element_by_id('sandbox_key_secret')

        production_key = driver.find_element_by_id('production_apns')
        production_key_secret = driver.find_element_by_id('production_key_secret')

        submit = driver.find_element_by_class_name('btn-info')

        # Fill the form with data
        now = str(int(time.time()))
        name.send_keys(u'测试' + now)
        android.click()
        android_identity.send_keys('test.' + now)

        ios.click()
        ios_identity.send_keys('test.' + now)
        sandbox_key.send_keys(os.path.abspath('test.p12'))
        sandbox_key_secret.send_keys('')

        production_key.send_keys(os.path.abspath('prod_123.p12'))
        production_key_secret.send_keys('123')

        # submitting the form
        submit.send_keys(Keys.RETURN)

        # check the returned result
        wait = WebDriverWait(driver, 10)
        wait.until(expected_conditions.title_is(u'gobelieve即时通讯'))
        self.assertIn(self.get_server_url('im/game/complete/'), driver.current_url)
        TestPage.share['item_id'] = driver.current_url.replace(self.get_server_url('im/game/complete/'), '')

    def test_06_im_complete(self):
        driver = self.driver
        # Opening the link we want to test
        driver.get(self.get_server_url('im/game/complete/' + TestPage.share['item_id']))
        self.assertIn(u"接入信息如下", driver.page_source)

    def test_07_im_edit(self):
        driver = self.driver
        # Opening the link we want to test
        driver.get(self.get_server_url('im/game/' + TestPage.share['item_id']))

        # find the form element
        name = driver.find_element_by_id('name')
        submit = driver.find_element_by_class_name('btn-info')
        # Fill the form with data
        now = str(int(time.time()))
        name_value = u'测试' + now
        name.send_keys(name_value)
        # submitting the form
        submit.send_keys(Keys.RETURN)

        # check the returned result
        wait = WebDriverWait(driver, 10)
        wait.until(expected_conditions.title_is(u'gobelieve即时通讯'))
        self.assertIn(self.get_server_url('im/game/detail'), driver.current_url)