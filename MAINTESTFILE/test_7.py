import pytest
from Test.BaseTest import BaseTest
import time
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from POM.locators import LOCATORS


@pytest.mark.usefixtures("driver")
class TestGeoLocation1:
    def test_geo_location_readings(self):
        driver = self.driver
        print(driver.page_source)

        driver.find_element(*LOCATORS["login.username"]).send_keys("standard_user")
        driver.find_element(*LOCATORS["login.password"]).send_keys("secret_sauce")
        driver.find_element(*LOCATORS["login.button"]).click()

        sleep(4)

        driver.find_element(*LOCATORS["menu.icon"]).click()
        sleep(2)
        driver.find_element(*LOCATORS["menu.geo_location"]).click()

        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located(LOCATORS["geo.allow_once"])).click()

        for _ in range(5):
            lat = wait.until(EC.presence_of_element_located(LOCATORS["geo.latitude"])).text
            lng = wait.until(EC.presence_of_element_located(LOCATORS["geo.longitude"])).text
            print("Latitude:", lat, "| Longitude:", lng)
            time.sleep(1)
