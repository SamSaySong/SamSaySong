# from appium import webdriver
# from appium.webdriver.common.mobileby import MobileBy
from matplotlib.pyplot import cla
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
import os, inspect, sys
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# path_chrome = CurDir + "\\"+"chromedriver.exe"
# def open_driver():

#     options = Options()
#     prefs = {"credentials_enable_service": False,  
#     "profile.password_manager_enabled": False ,  # tắt arlert save password chrome
#     "profile.default_content_settings.popups": 0,
#     # "download.default_directory": path_Download, # IMPORTANT - ENDING SLASH V IMPORTANT
#     "download.prompt_for_download": False,
#     "directory_upgrade": True,
#     "safebrowsing.enabled": True}
#     options.add_experimental_option('prefs', prefs)
#     options.add_argument('--safebrowsing-disable-download-protection')
#     options.add_argument("--no-sandbox") 
#     options.add_argument("--start-maximized") 
#     options.add_argument("--disable-dev-shm-usage") 
#     options.add_argument("--disable-web-security")
#     options.add_experimental_option("excludeSwitches", ["enable-automation",'enable-logging'])
#     options.add_experimental_option('useAutomationExtension', False)
#     options.add_argument('disable-infobars')
#     options.add_argument("--disable-extensions")
#     options.add_argument("--ignore-ssl-errors=yes")
#     options.add_argument("--allow-insecure-localhost")
#     options.add_argument('ignore-certificate-errors') ## fixx ssl
#     options.add_argument("--disable-blink-features")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
#     # options.add_argument("--allow-running-insecure-content")

#     driver = webdriver.Chrome(executable_path= path_chrome, chrome_options=options)
#     return driver

# driver = open_driver()
# driver.get('http://www.zenq.com')
# time.sleep(5)
class Item:
    pay_rate = 0.8
    def __init__(self, name, price, quantity):
        assert price >=0, f"Nếu price < 0 => lỗi"
        assert quantity >=0, f"Nếu quantity < 0 => lỗi"

        self.name = name
        self.price = price
        self.quantity = quantity

    def calculate_total(self):
        return self.price * self.quantity
    
    def apply_discount(self):
        self.price = self.price * self.pay_rate

    def is_integer(num):

        if isinstance(num, float):
            return num.is_integer()

        elif isinstance(num, int):
            return True

        else:
             return False

class Student:

    def __init__(self, name: str, major: str, gpa: int):

        self.name = name
        self.major = major
        self.gpa = gpa
    def on_honor_roll(self):
        if self.gpa >= 3.5:
            return True
        else:
            return False

class MyChef:
    def make_ga(self):
        print("ga ngon lam")

    def make_rausong(self):
        print('Rau song co sau')

    def make_special_dish(self):
        print("The chek makes bbq ribs")

    def make_comchien(self):
        print('Com chien duong chau')