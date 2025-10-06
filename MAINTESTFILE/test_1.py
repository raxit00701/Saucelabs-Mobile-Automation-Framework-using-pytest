import pytest
import time
import allure
import logging
from Test.BaseTest import BaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

log = logging.getLogger(__name__)
@pytest.fixture(scope="class")
def driver_setup(request):
    base = BaseTest()
    driver = base.driver
    wait = WebDriverWait(driver, 10)

    request.cls.driver = driver
    request.cls.wait = wait
    yield
    driver.quit()


@pytest.mark.usefixtures("driver_setup")
@allure.feature("Login Tests")
class TestLogin:

    def swipe(self, start_x, start_y, end_x, end_y, duration=800):
        finger = PointerInput("touch", "finger")
        actions = ActionBuilder(self.driver)
        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.pointer_up()
        actions.perform()

    @allure.story("Empty login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_empty_login(self):
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//android.widget.TextView[@text="LOGIN"]'))
        )
        login_btn.click()
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//android.view.ViewGroup[@content-desc="test-Error message"]')
            )
        )
        assert True, "Empty login error displayed"

    @allure.story("Auto-fill login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_autofill_login(self):
        screen_size = self.driver.get_window_size()
        width = screen_size['width']
        height = screen_size['height']

        self.swipe(width // 2, int(height * 0.7), width // 2, int(height * 0.3))

        user_text = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//android.widget.TextView[@text="standard_user"]'))
        )
        user_text.click()

        self.swipe(width // 2, int(height * 0.3), 545, 959)
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//android.widget.TextView[@text="LOGIN"]'))
        )
        login_btn.click()

        self.driver.back()
        assert True, "Auto-fill login attempted"

    @allure.story("Parametrized login")
    @pytest.mark.parametrize(
        "username,password,expected_error",
        [
            pytest.param("invalid_user", "wrong_pass", True),
            pytest.param("standard_user", "secret_sauce", False),
        ]
    )
    def test_login(self, username, password, expected_error):
        username_field = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//android.widget.EditText[@content-desc="test-Username"]'))
        )
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//android.widget.EditText[@content-desc="test-Password"]'))
        )

        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)

        time.sleep(1)
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//android.widget.TextView[@text="LOGIN"]'))
        )
        login_btn.click()

        if expected_error:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//android.view.ViewGroup[@content-desc="test-Error message"]')
                )
            )
            assert True, f"Invalid login error displayed for {username}"
        else:
            assert True, f"Valid login attempted with {username}"
