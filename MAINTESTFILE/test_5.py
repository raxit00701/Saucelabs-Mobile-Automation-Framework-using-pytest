import pytest
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from POM.locators import LOCATORS
from Test.BaseTest import BaseTest

@pytest.fixture(scope="class")
def driver(request):
    base = BaseTest()
    request.cls.driver = base.driver
    yield
    base.driver.quit()

@pytest.mark.usefixtures("driver")
class TestDrawing:
    def test_valid_login_and_draw(self):
        driver = self.driver

        # Debug: print UI XML to check elements
        print(driver.page_source)

        # --- Login ---
        driver.find_element(*LOCATORS["login.username"]).send_keys("standard_user")
        driver.find_element(*LOCATORS["login.password"]).send_keys("secret_sauce")
        driver.find_element(*LOCATORS["login.button"]).click()
        sleep(3)

        # Step 1: Click on ImageView (menu icon); try instance(1) behavior via index
        print("Step 1: Clicking on ImageView instance 1")
        image_views = driver.find_elements_by_class_name("android.widget.ImageView") \
                      if hasattr(driver, "find_elements_by_class_name") \
                      else driver.find_elements(*LOCATORS["menu.icon"]) or driver.find_elements("class name", "android.widget.ImageView")
        try:
            if isinstance(image_views, list) and len(image_views) > 1:
                image_views[1].click()
            else:
                driver.find_element(*LOCATORS["menu.icon"]).click()
        except Exception as e:
            print(f"Fallback clicking menu icon due to: {e}")
            driver.find_element(*LOCATORS["menu.icon"]).click()

        sleep(2)

        # Step 2: Open DRAWING
        print("Step 2: Clicking on test-DRAWING")
        driver.find_element(*LOCATORS["menu.drawing"]).click()
        sleep(2)

        # Step 3: Draw the pattern using W3C pointer actions (Appium 2.x)
        print("Step 3: Drawing the pattern")
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")

        def draw_line(x1, y1, x2, y2, hold=0.8):
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=finger)
            actions.w3c_actions.pointer_action.move_to_location(x1, y1)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(hold)
            actions.w3c_actions.pointer_action.move_to_location(x2, y2)
            actions.w3c_actions.pointer_action.pointer_up()
            actions.perform()
            sleep(0.2)

        # Pattern 1: Vertical
        print("Drawing pattern 1: Vertical line down")
        draw_line(162, 611, 162, 1436)

        # Pattern 2: Horizontal
        print("Drawing pattern 2: Horizontal line right")
        draw_line(162, 611, 911, 620)

        # Pattern 3: Diagonal down-left
        print("Drawing pattern 3: Diagonal line down-left")
        draw_line(911, 620, 162, 1063)

        # Pattern 4: Diagonal down-right
        print("Drawing pattern 4: Diagonal line down-right")
        draw_line(162, 1063, 852, 1439)

        print("Completed drawing all pattern segments")
        sleep(1)

        # Step 4: SAVE
        print("Step 4: Clicking on SAVE button")
        driver.find_element(*LOCATORS["drawing.save"]).click()

        # Step 5: Permission popup (handle variants)
        print("Step 5: Waiting for permission popup")
        wait = WebDriverWait(driver, 10)
        try:
            try:
                wait.until(EC.element_to_be_clickable(LOCATORS["perm.allow"])).click()
                print("Permission 'Allow' clicked")
            except TimeoutException:
                wait.until(EC.element_to_be_clickable(LOCATORS["perm.allow_once"])).click()
                print("Permission 'Allow once' clicked")
        except TimeoutException:
            print("Permission popup did not appear within timeout")

        # Step 6: Wait 5s and click Android dialog OK (button1)
        print("Step 6: Waiting 5 seconds and clicking on dialog button")
        sleep(5)
        try:
            driver.find_element(*LOCATORS["android.dialog.ok"]).click()
            print("Dialog button clicked successfully")
        except Exception as e:
            print(f"Error clicking dialog button: {e}")

        print("Test completed successfully!")

