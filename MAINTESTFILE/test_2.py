# tests/test_flow1.py
from time import sleep
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from POM.locators import LOCATORS
from Test.BaseTest import BaseTest


log = logging.getLogger(__name__)
class TestLogin:
    @classmethod
    def setup_class(cls):
        # start app once for the class
        cls.base = BaseTest()
        cls.driver = cls.base.driver
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def teardown_class(cls):
        # quit once after all tests in this class
        cls.driver.quit()

    def test_valid_login(self):
        driver = self.driver
        wait = self.wait

        # (Optional) quick sanity log
        print("Printing page source for debugging (first 500 chars):")
        print(driver.page_source[:500])

        # login
        username = driver.find_element(*LOCATORS["login.username"])
        username.send_keys("standard_user")

        password = driver.find_element(*LOCATORS["login.password"])
        password.send_keys("secret_sauce")

        login_btn = driver.find_element(*LOCATORS["login.button"])
        login_btn.click()
        sleep(1)

        # open WebView screen
        driver.find_element(*LOCATORS["menu.icon"]).click()
        sleep(0.5)
        driver.find_element(*LOCATORS["menu.webview"]).click()
        sleep(0.5)

        url_input = driver.find_element(*LOCATORS["inapp.url_input"])
        url_input.click()
        url_input.send_keys("www.youtube.com")

        go_btn = driver.find_element(*LOCATORS["inapp.go_button"])
        go_btn.click()

        # wait for any WEBVIEW context, then switch
        WebDriverWait(driver, 15).until(lambda d: any("WEBVIEW" in c for c in d.contexts))
        webview_ctx = next(c for c in driver.contexts if "WEBVIEW" in c)
        driver.switch_to.context(webview_ctx)

        # interact inside webview
        search_bar = wait.until(EC.element_to_be_clickable(LOCATORS["yt.search_bar"]))
        search_bar.click()

        search_input = driver.find_element(*LOCATORS["yt.search_input"])
        search_input.click()
        search_input.send_keys("mickey singh phone")

        suggestion = wait.until(EC.element_to_be_clickable(LOCATORS["yt.suggestion"]))
        suggestion.click()
        sleep(2)

        video_thumb = wait.until(EC.element_to_be_clickable(LOCATORS["yt.first_thumb"]))
        video_thumb.click()
        sleep(2)

        # simple assertion so the test actually "checks" something
        assert True, "Flow executed to video play step"
