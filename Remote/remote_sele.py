
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
from selenium.webdriver.remote.webdriver import WebDriver
import time
desired_cap = {
"os" : "Windows",
"os_version" : "7",
"browser" : "IE",
"browser_version" : "8.0",
"browserstack.local" : "false",
}
 
def attach_to_session(executor_url, session_id):

    original_execute = WebDriver.execute
    def new_command_execute(self,command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self,command, params)

    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver


bro = attach_to_session('http://127.0.0.1:54980', 'c8c7f9097fe4dc55308f72e37efed89d')
# element_trans= bro.find_element_by_xpath('//*[@class="current"]/li[8]/a')
# element_trans.click()

time.sleep(3)


