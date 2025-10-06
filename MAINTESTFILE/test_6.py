import pytest
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from POM.locators import LOCATORS

@pytest.mark.usefixtures("driver")
class TestAboutBookDemo:
    def test_book_demo_in_webview(self):
        driver = self.driver
        print(driver.page_source)

        driver.find_element(*LOCATORS["login.username"]).send_keys("standard_user")
        driver.find_element(*LOCATORS["login.password"]).send_keys("secret_sauce")
        driver.find_element(*LOCATORS["login.button"]).click()

        sleep(3)

        driver.find_element(*LOCATORS["menu.icon"]).click()
        sleep(3)
        driver.find_element(*LOCATORS["menu.about"]).click()

        print("Available contexts:", driver.contexts)
        WebDriverWait(driver, 20).until(lambda d: len(d.contexts) > 1)
        contexts = driver.contexts
        print("Available contexts:", contexts)
        webview_context = [c for c in contexts if 'WEBVIEW' in c][0]
        driver.switch_to.context(webview_context)

        WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
        print("Webview page source:", driver.page_source)

        book_demo_btn = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(LOCATORS["about.book_demo"]))
        assert book_demo_btn.is_displayed(), "Book a demo button is not displayed"
        book_demo_btn.click()
