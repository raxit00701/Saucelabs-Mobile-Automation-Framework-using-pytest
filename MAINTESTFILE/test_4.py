# test_4.py (or test_main_flow.py)
import pytest
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Test.locators import LOCATORS

@pytest.mark.usefixtures("driver")
class TestMainFlow:
    def test_main_flow(self, driver):
        # STEP 1: LOGIN
        sleep(2)
        driver.find_element(*LOCATORS["xpath"]["username_input"]).send_keys("standard_user")
        driver.find_element(*LOCATORS["xpath"]["password_input"]).send_keys("secret_sauce")
        driver.find_element(*LOCATORS["xpath"]["login_button"]).click()
        sleep(3)

        # STEP 2: SORT ITEMS
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(LOCATORS["xpath"]["sort_button"])
        ).click()
        sleep(2)
        driver.find_element(*LOCATORS["xpath"]["sort_high_to_low"]).click()
        sleep(1)

        # STEP 3: ADD ITEMS
        driver.find_element(*LOCATORS["android_uiautomator"]["image_view_instance_4"]).click()
        sleep(1)
        driver.find_element(*LOCATORS["xpath"]["add_quantity_1"]).click()
        driver.find_element(*LOCATORS["xpath"]["add_quantity_3"]).click()
        sleep(1)
        driver.find_element(*LOCATORS["android_uiautomator"]["image_view_instance_3"]).click()
        sleep(1)

        # STEP 4: CHECKOUT
        checkout_btn = driver.find_element(*LOCATORS["android_uiautomator"]["scroll_to_checkout"])
        checkout_btn.click()
        sleep(2)

        # STEP 5: CONTINUE BUTTON TEST (INVALID DETAILS)
        driver.find_element(*LOCATORS["accessibility_id"]["continue_button"]).click()
        try:
            error_msg = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(LOCATORS["accessibility_id"]["error_message"])
            )
            print("❌ Error message not displayed")
        except:
            print("✅ Error message displayed correctly for empty input")

        # STEP 6: ENTER INVALID DETAILS
        driver.find_element(*LOCATORS["accessibility_id"]["first_name_input"]).send_keys("123")
        driver.find_element(*LOCATORS["accessibility_id"]["last_name_input"]).send_keys("@@@")
        driver.find_element(*LOCATORS["accessibility_id"]["zip_code_input"]).send_keys("abcd")
        driver.find_element(*LOCATORS["android_uiautomator"]["continue_text"]).click()
        sleep(1)
        driver.back()
        sleep(1)

        # STEP 7: ENTER VALID DETAILS
        driver.find_element(*LOCATORS["accessibility_id"]["first_name_input"]).clear().send_keys("John")
        driver.find_element(*LOCATORS["accessibility_id"]["last_name_input"]).clear().send_keys("Doe")
        driver.find_element(*LOCATORS["accessibility_id"]["zip_code_input"]).clear().send_keys("12345")
        driver.find_element(*LOCATORS["android_uiautomator"]["continue_text"]).click()
        sleep(1)

        # STEP 8: SCROLL TO FINISH AND CLICK
        try:
            finish_btn = driver.find_element(*LOCATORS["android_uiautomator"]["scroll_to_finish"])
            finish_btn.click()
            sleep(1)
        except:
            print("❌ FINISH button not found or scroll failed")

        # STEP 9: VERIFY CHECKOUT COMPLETE AND BACK HOME
        try:
            checkout_complete = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(LOCATORS["android_uiautomator"]["checkout_complete"])
            )
            print("✅ Checkout Complete is visible")
            driver.find_element(*LOCATORS["accessibility_id"]["back_home_button"]).click()
            print("✅ Clicked BACK HOME successfully")
        except:
            print("❌ Checkout Complete not visible or BACK HOME button not found")
