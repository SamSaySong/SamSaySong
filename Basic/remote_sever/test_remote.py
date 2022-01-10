import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import os, inspect, sys

# desired_cap = {
#  'os_version': '7',
#  'resolution': '1280x800',
#  'browser': 'Chrome',
#  'browser_version': '95.0',
#  'os': 'Windows',

# }
# chromeOptionsRemote = webdriver.ChromeOptions()
# chromeOptionsRemote.add_argument("--start-maximized")
# chromeOptionsRemote.add_argument("--disable-session-crashed-bubble")

# initRemoteDriver = webdriver.Remote(options=chromeOptionsRemote, command_executor='http://192.168.1.93:4444/wd/hub', desired_capabilities=desired_cap)



# initRemoteDriver.get("https://www.kenh14.vn/")

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_chrome = os.path.abspath(CurDir +"\\chromedriver.exe")

def open_driver():

    chrome_options = Options()
   
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) # tắt popup của face
    chrome_options.add_argument("user-data-dir="+CurDir+"\\exxtenstion")
    chrome_options.add_extension(r"D:\INFOR\Tool\eSignerChrome_1.0.8_0.crx")
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    chrome_options.add_argument("--profile-directory=Default")
    prefs = {"credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "download.default_directory": 'D:\HuyNP\Project_PIT_Terra\input',}   
    chrome_options.add_experimental_option("prefs",  
                                            {'profile': prefs}) #disable-restore-pages-poup
  
    
    driver = webdriver.Chrome(executable_path= path_chrome, chrome_options=chrome_options)
     
    return driver

driver = open_driver()


# driver.get(r'https://shopee.vn/search?keyword=d%C3%A2y%20chuy%E1%BB%81n')
# Navigate to url
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def geoLocationTest():
    
    Map_coordinates = dict({
        "latitude": 41.8781,
        "longitude": -87.6298,
        "accuracy": 100
        })
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", Map_coordinates)
    driver.get(r'https://shopee.vn/search?keyword=d%C3%A2y%20chuy%E1%BB%81n')
geoLocationTest()
driver.quit()