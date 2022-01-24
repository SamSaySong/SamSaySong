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
from selenium.webdriver.remote.webdriver import WebDriver

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
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation",'enable-logging']) # tắt popup của face
    chrome_options.add_argument("user-data-dir="+CurDir+"\\exxtenstion")
    chrome_options.add_extension(r"D:\Tai lieu\Tool\eSignerChrome_1.0.8_0.crx")
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
  
    
    driver = webdriver.Chrome(executable_path= path_chrome, options=chrome_options)
     
    return driver

urls = "https://www.google.com.vn/?hl=vi"

def test_remote(urls):
  
    driver = open_driver()
    
    driver.get(urls)

    user_name =  '0109411417-QL'
    pass_word = "123456aA@"
    login(driver,user_name,pass_word)

    # while True:
    #     executor_url = driver.command_executor._url
    #     session_id = driver.session_id
    #     time.sleep(1)
    #     with open(CurDir+"\\"+"log_session.txt", mode= "w+",encoding="utf-8") as file:
    #         file.write(executor_url+"\n"+session_id)
    #         file.close()


url_Thuedoanhnghiep = 'https://thuedientu.gdt.gov.vn/etaxnnt/Request?&dse_sessionId=opLE55FV2bAnltX5V-tNM3S&dse_applicationId=-1&dse_pageId=1&dse_operationName=corpIndexProc&dse_errorPage=error_page.jsp&dse_processorState=initial&dse_nextEventName=start'

def check_element(driver, xpath, int_Timeout=60):
    int_Count = 0
    while True:
        try:
            driver.find_element_by_xpath(xpath)
            return True
        except:
            if int_Count == int_Timeout:
                return False
            int_Count+=1
            time.sleep(1)

def select_xpath_options(driver, xpath_select, xpath_options, input_option, timeout = 1):
    
    driver.find_element_by_xpath(xpath_select).click()
    time.sleep(timeout)

    for i, j in enumerate(driver.find_elements_by_xpath(xpath_options)):
        if  input_option in str(j.text).strip() :
            j.click()
            break


def login(driver, user_name, pass_word):

    try:
        driver.get(url_Thuedoanhnghiep)
        try:
            if check_element(driver, '//*[@class="banner"]/div[3]/span/strong/a',5) == True:
                btn_Dangxuat = driver.find_element_by_xpath('//*[@class="banner"]/div[3]/span/strong/a')
                btn_Dangxuat.click()
                alert = Alert(driver)
                # Check alert logout
                if (alert.text).strip() == 'Quý khách có muốn đăng xuất khỏi dịch vụ?':
                    alert.accept()
                    ele_Dangxuat = driver.find_element_by_xpath('//*[@class="dangnhap"]/span/strong/a')
                    ele_Dangxuat.click()
        except:
            pass

        # Screen Thue Dien Tu
        btn_Doanhnghiep = driver.find_element_by_xpath("//*[@class='khungbaolongin']/div[2]/div/div[2]").click()
        time.sleep(2)

        # Screen Login form
        btn_Login_form = driver.find_element_by_xpath("//*[@class='banner']/div[3]/span[2]/button").click()
        time.sleep(2)

        while True:
            try:
                input_User = driver.find_element_by_xpath('//*[@id="_userName"]')
                input_User.click()
                input_User.clear()
                input_User.send_keys(user_name)
                time.sleep(2)
                    
                input_Password = driver.find_element_by_xpath('//*[@id="password"]')
                input_Password.click()
                input_Password.clear()
                input_Password.send_keys(pass_word)
                time.sleep(2)

                element_select_Doituong = '//*[@id="login_type"]'
                element_options_Doituong = '//*[@id="login_type"]/option'
                select_xpath_options(driver, element_select_Doituong, element_options_Doituong, input_option='Người nộp thuế')
                time.sleep(30)
            except:
                pass
     

    except Exception as e:      
       print(e)
     
    
if __name__ == "__main__":   
    test_remote(urls)    
    # 456456456546