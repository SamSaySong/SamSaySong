from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import os, sys, inspect
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_chrome = os.path.abspath(CurDir +"\\chromedriver.exe")
desired_caps = dict(
    platformName='Android',
    platformVersion='10',
    automationName='uiautomator2',
    deviceName='Android Emulator',
    app=path_chrome('../../../apps/selendroid-test-app.apk')
)
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
el = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='item')
el.click()