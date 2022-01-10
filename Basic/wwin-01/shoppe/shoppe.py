
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import by
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
import os, inspect
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
    driver = webdriver.Chrome(executable_path= r"D:\Win\Train Python\wwin-01\selenium03\chromedriver.exe",chrome_options=chrome_options)
    return driver

def input():
    df_input = pd.read_excel(path+"\\SP.xlsx", sheet_name= "Sheet1",engine="openpyxl")
    #print(df_input)
    return df_input

def Main_func():
    df_input = input()
    df_output = df_input
    driver = open_driver()
    driver.implicitly_wait(5)
    lst_giaBan= []
    lst_giaGoc = []
    lst_KM = []
    lst_SP = []
    lst_tenShop = []
    lst_daBan = []
    for idx_input, row_input in df_input.iterrows():
        driver.get("https://shopee.vn/")
        sleep(2)
        main_page = driver.current_window_handle
        
        wait = WebDriverWait(driver, 5)
        button_close = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@class="shopee-popup__close-btn"]')))
        driver.execute_script("arguments[0].click()", button_close)

        sreach_fiel = driver.find_element_by_xpath('//*[@class="shopee-searchbar-input"]/input')
        sreach_fiel.clear()
        sreach_fiel.send_keys(row_input[0])
        
        butn_search = driver.find_element_by_xpath('//*[@class="btn btn-solid-primary btn--s btn--inline"]')
        butn_search.click()
        
        driver.execute_script("window.scrollTo(0,1800)")
        sleep(5)
      
        lst_tenSP = driver.find_elements_by_xpath('//*[@class="PFM7lj"]/div')
        
        for idx_tenSP, i_tenSP in enumerate(lst_tenSP):
            if (i_tenSP.text) == row_input[1]:
                i_tenSP.click()
                break
        sleep(2)
       
        element_giaBan = driver.find_element_by_xpath("//*[@class='flex items-center']/div/div/div[1]")
        lst_giaBan.append(element_giaBan.text)
        sleep(2)                                       
        element_SP = driver.find_element_by_xpath('//*[@class="flex items-center _90fTvx"]/div/div[2]')
        lst_SP.append((element_SP.text).split()[0])
        element_tenShop = driver.find_element_by_xpath('//*[@class="_2V1E4_"]/div[1]')
        lst_tenShop.append(element_tenShop.text)
        element_daBan = driver.find_element_by_xpath('//*[@class="flex _210dTF"]/div[1]')
        lst_daBan.append(element_daBan.text)
        try: 
            element_giaKM = driver.find_element_by_xpath("//*[@class='flex items-center']/div/div[1]")
            element_KM = driver.find_element_by_xpath("//*[@class='flex items-center']/div[1]/div[2]/div[2]") 
            lst_giaGoc.append(element_giaKM.text)
            lst_KM.append((element_KM.text).split()[0])
        except NoSuchElementException:
            print('NoSuchElementException: Sản phẩm không có KM')
            lst_giaGoc.append("Không có KM")
            lst_KM.append("Không có KM")
        
        sleep(2)
        driver.switch_to.window(main_page)
    
    df_output["Số lượng"]= lst_SP
    df_output["Giá bán"] = lst_giaBan
    df_output["Giá gốc"] = lst_giaGoc
    df_output["%KM"] = lst_KM
    df_output["Tên shop"] = lst_tenShop
    df_output["Đã bán"] = lst_daBan
    writer = pd.ExcelWriter(os.path.abspath(CurDir+'\\Output\\')+"\\Out_out.xlsx",engine="openpyxl")
    df_output.to_excel(writer,sheet_name="Sheet1", index= False,engine="openpyxl")
    writer.save()
    driver.quit()

if __name__ == "__main__":
    Main_func()
