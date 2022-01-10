from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
import os, inspect
import threading
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path =  os.path.abspath(CurDir+'\\Input\\')
def open_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    #chrome_options.add_argument("--headless") #chạy ngầm browwser
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path= r"D:\HuyNP\Basic\remote_sever\chromedriver.exe",chrome_options=chrome_options)
    return driver

def Main(x):
    driver = open_driver()
    a = 400
    b = 10
    driver.set_window_rect(a,b,400,600)
    driver.get("https://www.youtube.com/")
    sleep(3)
    wait = WebDriverWait(driver,20)
    actions = ActionChains(driver)

    button_Search= wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/yt-icon-button/button/yt-icon')))
    driver.execute_script("arguments[0].click()",button_Search)
    
    search =wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@id='search']")))
    actions.move_to_element(search)
    actions.click(search)
    actions.send_keys(x)
    actions.perform()
    
    button_search= wait.until(EC.presence_of_element_located((By.XPATH,'//*[@class="style-scope ytd-searchbox"]/yt-icon')))
    driver.execute_script("arguments[0].click()",button_search)
    for j in range(10):
        sleep(1)
        driver.execute_script("window.scrollTo(0,{}00)".format(str(j)))
    sleep(10)
    driver.quit()

def chia_key(step):
    df_key = pd.read_excel(path+"\\keys.xlsx",sheet_name="Sheet1", engine="openpyxl")
    lst_key = [] 
    for idx, row in df_key.iterrows():
        lst_key.append(row[0])
    for x in range(step, len(lst_key), 2):
        Main(lst_key[x])

if __name__ == "__main__":
    lst_thread = []
    for i in range (2):
        new_thread = threading.Thread(target=chia_key,args=(i,))
        lst_thread.append(new_thread)
        new_thread.start()
        sleep(5)
    for j in lst_thread:
        j.join()
