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

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_chrome = os.path.abspath(CurDir +"\\chromedriver.exe")

# def attach_to_session(executor_url, session_id):

#     original_execute = WebDriver.execute
#     def new_command_execute(self,command, params=None):
#         if command == "newSession":
#             # Mock the response
#             return {'success': 0, 'value': None, 'sessionId': session_id}
#         else:
#             return original_execute(self,command, params)

#     # Patch the function before creating the driver object
#     WebDriver.execute = new_command_execute
#     driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
#     driver.session_id = session_id
#     # Replace the patched function with original function
#     WebDriver.execute = original_execute
#     return driver


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

urls = "https://www.google.com.vn/?hl=vi"

def test_remote(urls):
  
    driver = open_driver()
    
    driver.get(urls)

    while True:
        executor_url = driver.command_executor._url
        session_id = driver.session_id
        time.sleep(1)
        with open(CurDir+"\\"+"log_session.txt", mode= "w+",encoding="utf-8") as file:
            file.write(executor_url+"\n"+session_id)
            file.close()
    
if __name__ == "__main__":   
    test_remote(urls)    
    # 456456456546