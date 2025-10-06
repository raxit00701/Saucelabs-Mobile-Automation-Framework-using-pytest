# POM/locators.py
from appium.webdriver.common.appiumby import AppiumBy

# Central factory: keys -> (by, value)
LOCATORS = {
    # --- Login ---
    "login.username": (AppiumBy.XPATH, '//android.widget.EditText[@content-desc="test-Username"]'),
    "login.password": (AppiumBy.XPATH, '//android.widget.EditText[@content-desc="test-Password"]'),
    "login.button":   (AppiumBy.XPATH, '//android.widget.TextView[@text="LOGIN"]'),

    # --- Menu / common entries ---
    "menu.icon":            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(1)'),
    "menu.geo_location":    (AppiumBy.ACCESSIBILITY_ID, 'test-GEO LOCATION'),
    "menu.drawing":         (AppiumBy.ACCESSIBILITY_ID, 'test-DRAWING'),
    "menu.webview":         (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("WEBVIEW")'),
    "menu.about":           (AppiumBy.ACCESSIBILITY_ID, 'test-ABOUT'),

    # --- In-app WebView launcher (native) ---
    "inapp.url_input":      (AppiumBy.ACCESSIBILITY_ID, 'test-enter a https url here...'),
    "inapp.go_button":      (AppiumBy.XPATH, '//android.widget.TextView[@text="GO TO SITE"]'),

    # --- Geo Location page ---
    "geo.allow_once":       (AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_one_time_button"]'),
    "geo.latitude":         (AppiumBy.ACCESSIBILITY_ID, "test-latitude"),
    "geo.longitude":        (AppiumBy.ACCESSIBILITY_ID, "test-longitude"),
    "drawing.save": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SAVE")'),
    # --- About (WEBVIEW) ---
    "about.book_demo":      (AppiumBy.XPATH, "//button[contains(@class,'MuiButton-root') and contains(normalize-space(),'Book a demo')]"),

    # --- YouTube (inside WEBVIEW) ---
    "yt.search_bar":        (AppiumBy.XPATH, "//div[@aria-label='Search YouTube']"),
    "yt.search_input":      (AppiumBy.XPATH, "//input[@id='search' or @name='search_query']"),
    "yt.suggestion":        (AppiumBy.XPATH, "//div[contains(@class,'ytSuggestionComponentSuggestion') and @role='presentation']"),
    "yt.first_thumb":       (AppiumBy.CSS_SELECTOR, "ytm-thumbnail-cover.video-thumbnail-container-large img.video-thumbnail-img"),

    # --- PERMISSIONS ---
    "perm.allow": (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
    "perm.allow_once": (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_one_time_button"),

    # generic Android dialog positive button
    "android.dialog.ok":  (AppiumBy.ID, "android:id/button1"),
}
