from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os, sys, inspect
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_FireFox = os.path.abspath(CurDir +"\\geckodriver.exe")


options = webdriver.FirefoxOptions()
options.add_argument("--start-maximized") 
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-infobars')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-extensions')
service = Service(path_FireFox)
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(options = options, service=service)

driver.get("https://www.geeksforgeeks.org/python-calendar-module/")
wait = WebDriverWait(driver, 10)
driver.refresh()
ele_calendar = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="post-254800"]/div[2]/figure[1]/table/tbody/tr[3]/th[1]/a')))
# ele_calendar = driver.find_element(By.XPATH,"//strong[normalize-space()='setfirstweekday()']")
driver.get(ele_calendar.get_attribute('href'))
time.sleep(1)

# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# driver.execute_script("window.scrollTo(0, Y)") 
for i in range(1,5000,100):
    driver.execute_script("window.scrollTo(0, {})".format(i))
    time.sleep(1)
try:
    element_X = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[10]/div[3]/div/div[1]/span')))
    element_X.click()
except:
    pass
time.sleep(1)
