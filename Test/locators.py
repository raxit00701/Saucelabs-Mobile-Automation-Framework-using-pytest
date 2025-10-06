
# locators.py
# Consolidated locators for Appium tests, grouped by strategy for clarity and minimal space.

from appium.webdriver.common.appiumby import AppiumBy

LOCATORS = {
    "xpath": {
        "username_input": (AppiumBy.XPATH, '//android.widget.EditText[@content-desc="test-Username"]'),  # Username field
        "password_input": (AppiumBy.XPATH, '//android.widget.EditText[@content-desc="test-Password"]'),  # Password field
        "login_button": (AppiumBy.XPATH, '//android.widget.TextView[@text="LOGIN"]'),  # Login button
        "sort_button": (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Modal Selector Button"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView'),  # Sort modal
        "sort_high_to_low": (AppiumBy.XPATH, '//android.widget.TextView[@text="Price (high to low)"]'),  # Sort: Price high to low
        "add_quantity_1": (AppiumBy.XPATH, '(//android.widget.TextView[@text="+"])[1]'),  # First add quantity
        "add_quantity_3": (AppiumBy.XPATH, '(//android.widget.TextView[@text="+"])[3]'),  # Third add quantity
        "add_to_cart": (AppiumBy.XPATH, '//android.widget.TextView[@text="ADD TO CART"]'),  # Add to cart
        "back_to_products": (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-BACK TO PRODUCTS"]/android.widget.ImageView'),  # Back to products
        "fourth_item": (AppiumBy.XPATH, '(//android.view.ViewGroup[@content-desc="test-Item"])[4]'),  # Fourth item
        "add_to_cart_fourth": (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-ADD TO CART"]'),  # Add to cart (fourth item)
        "go_to_site_button": (AppiumBy.XPATH, '//android.widget.TextView[@text="GO TO SITE"]'),  # Webview go to site
        "youtube_search_bar": (AppiumBy.XPATH, "//div[@aria-label='Search YouTube']"),  # YouTube search bar
        "youtube_search_input": (AppiumBy.XPATH, "//input[@id='search' or @name='search_query']"),  # YouTube search input
        "youtube_suggestion": (AppiumBy.XPATH, "//div[contains(@class, 'ytSuggestionComponentSuggestion') and @role='presentation']"),  # YouTube suggestion
        "permission_allow_one_time": (AppiumBy.XPATH, '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_one_time_button"]'),  # Permission one-time
    },
    "accessibility_id": {
        "continue_button": (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE"),  # Checkout continue
        "error_message": (AppiumBy.ACCESSIBILITY_ID, "test-Error message is displayed"),  # Error message
        "first_name_input": (AppiumBy.ACCESSIBILITY_ID, "test-First Name"),  # First name
        "last_name_input": (AppiumBy.ACCESSIBILITY_ID, "test-Last Name"),  # Last name
        "zip_code_input": (AppiumBy.ACCESSIBILITY_ID, "test-Zip/Postal Code"),  # Zip code
        "back_home_button": (AppiumBy.ACCESSIBILITY_ID, "test-BACK HOME"),  # Back home
        "url_input": (AppiumBy.ACCESSIBILITY_ID, "test-enter a https url here..."),  # Webview URL
        "geo_location": (AppiumBy.ACCESSIBILITY_ID, "test-GEO LOCATION"),  # Geo location
        "latitude_display": (AppiumBy.ACCESSIBILITY_ID, "test-latitude"),  # Latitude
        "longitude_display": (AppiumBy.ACCESSIBILITY_ID, "test-longitude"),  # Longitude
        "drawing_option": (AppiumBy.ACCESSIBILITY_ID, "test-DRAWING"),  # Drawing option
    },
    "android_uiautomator": {
        "image_view_instance_4": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(4)'),  # ImageView 4
        "image_view_instance_3": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(3)'),  # ImageView 3
        "scroll_to_checkout": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("CHECKOUT")'),  # Scroll to checkout
        "continue_text": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CONTINUE")'),  # Continue by text
        "scroll_to_finish": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("FINISH")'),  # Scroll to finish
        "checkout_complete": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CHECKOUT: COMPLETE!")'),  # Checkout complete
        "first_item": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("test-Item").instance(0)'),  # First item
        "menu_image_view_instance_1": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(1)'),  # Menu ImageView 1
        "webview_option": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("WEBVIEW")'),  # Webview option
        "save_button": (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SAVE")'),  # Save button
    },
    "css_selector": {
        "youtube_video_thumbnail": (AppiumBy.CSS_SELECTOR, "ytm-thumbnail-cover.video-thumbnail-container-large img.video-thumbnail-img"),  # YouTube thumbnail
    },
    "id": {
        "permission_allow": (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),  # Permission allow
        "dialog_button": (AppiumBy.ID, "android:id/button1"),  # Dialog button
    },
    "class_name": {
        "image_view": (AppiumBy.CLASS_NAME, "android.widget.ImageView"),  # Generic ImageView
    }
}
