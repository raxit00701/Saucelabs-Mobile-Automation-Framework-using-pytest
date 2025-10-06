# base.py
from appium import webdriver
from appium.options.android import UiAutomator2Options


class BaseTest:
    def __init__(self):
        options = UiAutomator2Options()
        options.set_capability("platformName", "Android")
        options.set_capability("deviceName", "Pixel_8")
        options.set_capability("automationName", "UiAutomator2")
        options.set_capability("app", r"C:\Users\raxit\PycharmProjects\AppiumTesting\.venv\Lib\test.apk")
        options.set_capability("appPackage", "com.swaglabsmobileapp")
        options.set_capability("appActivity", "com.swaglabsmobileapp.SplashActivity")
        options.set_capability("appWaitActivity", "*")
        options.set_capability("appWaitDuration", 60000)
        options.set_capability("adbExecTimeout", 60000)
        options.set_capability("newCommandTimeout", 300)
        options.set_capability("noReset", False)
        options.set_capability("fullReset", True)
        options.set_capability("chromedriverExecutable", r"C:\chromedriver.exe")
        options.set_capability("unicodeKeyboard", True)
        options.set_capability("resetKeyboard", True)

        # Start driver
        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    def quit_driver(self):
        self.driver.quit()
