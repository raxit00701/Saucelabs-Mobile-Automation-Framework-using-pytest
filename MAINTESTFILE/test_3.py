import pytest
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Test.locators import LOCATORS

@pytest.mark.usefixtures("driver")
class TestLoginFlow:
    # --- helpers ------------------------------------------------------------
    def _ensure_login_screen(self, driver):
        """If already logged in, bring app back to login screen."""
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located(LOCATORS["xpath"]["username_input"])
            )
            return  # already on login
        except TimeoutException:
            pass

        # Not on login → reset/relaunch app (adjust package if different)
        try:
            driver.terminate_app("com.swaglabsmobileapp")
            driver.activate_app("com.swaglabsmobileapp")
        except Exception:
            # Fallback for drivers without terminate/activate
            driver.reset()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(LOCATORS["xpath"]["username_input"])
        )

    def _login(self, driver, user="standard_user", pwd="secret_sauce"):
        self._ensure_login_screen(driver)
        driver.find_element(*LOCATORS["xpath"]["username_input"]).send_keys(user)
        driver.find_element(*LOCATORS["xpath"]["password_input"]).send_keys(pwd)
        driver.find_element(*LOCATORS["xpath"]["login_button"]).click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(LOCATORS["android_uiautomator"]["first_item"])
        )

    # --- tests --------------------------------------------------------------
    def test_valid_login(self, driver):
        print(driver.page_source)
        self._login(driver)
        print("✅ Login executed successfully")

    def test_complete_flow(self, driver):
        """Full flow without calling another test."""
        self._login(driver)

        # Step 1: first item → add to cart
        print("Step 1: Selecting first item and adding to cart...")
        driver.find_element(*LOCATORS["android_uiautomator"]["first_item"]).click()
        sleep(2)

        driver.swipe(540, 1500, 540, 600, 1000)  # scroll down
        sleep(1)
        driver.find_element(*LOCATORS["xpath"]["add_to_cart"]).click()
        sleep(2)
        print("✅ Step 1 completed: Added first item to cart")

        # Step 2: back to products
        print("Step 2: Going back to products...")
        driver.swipe(540, 600, 540, 1500, 1000)  # scroll up
        sleep(1)
        driver.find_element(*LOCATORS["xpath"]["back_to_products"]).click()
        sleep(2)
        print("✅ Step 2 completed: Back to products page")

        # Step 3: select fourth item
        print("Step 3: Selecting fourth item...")
        driver.swipe(540, 1500, 540, 600, 1000)  # scroll down
        sleep(1)
        driver.find_element(*LOCATORS["xpath"]["fourth_item"]).click()
        sleep(2)
        print("✅ Step 3 completed: Selected fourth item")

        # Step 4: add fourth item
        print("Step 4: Adding fourth item to cart...")
        driver.swipe(540, 1500, 540, 600, 1000)
        sleep(1)
        driver.find_element(*LOCATORS["xpath"]["add_to_cart_fourth"]).click()
        sleep(2)
        print("✅ Step 4 completed: Added fourth item to cart")

        print("🎉 All test steps completed successfully!")
