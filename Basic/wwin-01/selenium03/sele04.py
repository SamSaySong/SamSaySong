import re
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from unidecode import unidecode
import os, inspect

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path =  os.path.abspath(CurDir+'\\Test_Thu_Muc\\')

def open_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path= CurDir +"\\chromedriver.exe",chrome_options=chrome_options)
    return driver
def check_element(driver,xpath,int_Timeout=60):
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

def select_xpath_options(driver, xpath_select, xpath_options, input_option, timeout=1):
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(xpath_select))
    time.sleep(timeout)
    for i in driver.find_elements_by_xpath(xpath_options): 
        if str(i.text).strip() == str(input_option).strip():
            driver.execute_script("arguments[0].click();", i)
            break

def str_input():
    str_iinput = input("Tinh thanh:")
    return str_iinput

def Main():
    driver = open_driver()
    str_Input = str_input()
    lst_input = str_Input.lower().split()
    lst_encode = [unidecode(i) for i in lst_input]
    str_lower ="-".join(lst_encode)
    
    driver.get("https://www.chotot.com/")
    time.sleep(2)
    
    ele_bds = driver.find_element_by_xpath('//*[@id="__next"]/main/main/div[3]/div[1]/div/div/li[1]/a/img')
    check_element(driver, ele_bds, 2)
    
    ele_bds = driver.execute_script("arguments[0].click()", ele_bds)
    time.sleep(2)
   
    ele_chothue = driver.find_element_by_xpath('//*[@id="__next"]/main/main/div[2]/div[1]/div/li[2]/div/a[5]')
    ele_chothue = driver.execute_script("arguments[0].click()", ele_chothue)
    
    # selec_Chothue = Select(driver.find_element_by_xpath('//*[@id="__next"]/main/main/div[2]/div[1]/div/li[2]/a/div[2]'))
    # selec_Chothue.deselect_by_visible_text("Phòng trọ")
    time.sleep(3)
    ele_option_All ="//body/div[@id='__next']/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/span[2]"
    #ele_option_All = driver.execute_script("arguments[0].click()", ele_option_All)
    lst_option_TP = '//*[@class="Styles_tagLink__w5_mC "]'
    
    select_xpath_options(driver, ele_option_All, lst_option_TP, str_Input, 2)
    # for i, j in enumerate(lst_option_TP):
    #     if str(j.text) == str_Input:
    #         j.click()           
    #         break
    # time.sleep(5)
    time.sleep(5)
    ele_AllQuan = driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[2]/div/div/ul/li[1]/a")
    ele_AllQuan = driver.execute_script("arguments[0].click()", ele_AllQuan)
    time.sleep(3)
    
    lst_title = []  
    lst_DT = []  #Diện tích
    lst_giaP = []  #Giá phòng (tháng)
    lst_Dc = []   #Địa chỉ BĐS
    lst_TT = []  #Thông tin thêm
    for z in range(1,2):   
        urls = 'https://nha.chotot.com/'+ str_lower + '/thue-phong-tro?page=' + str(z)
        driver.get(urls)
        
        lst_url = driver.find_elements_by_xpath('//*[@id="__next"]/div[3]/div[1]/div[2]/main/div[1]/div[3]/div/div[1]/ul[1]/div[*]/li/a')  
        
        for i, k in enumerate(lst_url):        
            driver_1 = open_driver()
            driver_1.get(k.get_attribute("href"))
            time.sleep(5)
            lst_price = driver_1.find_element_by_xpath('//*[@id="__next"]/div[3]/div[1]/div/div[4]/div[2]/div[1]/div[1]/span/div/span/span/span[1]')
            # nếu 1 url ko tìm thấy element thì xử lí ngoại lệ
            try:    
                if lst_price.text <= "3 triệu/tháng" or str(lst_price.text).find("đ/tháng") != -1 :
                    lst_Dc.append((driver_1.find_element_by_xpath('//*[@class="fz13"]')).text)
                    lst_DT.append(((driver_1.find_element_by_xpath('//*[@id="__next"]/div[3]/div[1]/div/div[4]/div[2]/div[1]/div[1]/span/div/span/span/span[1]/span[*]')).text).split('-')[1].strip())
                    lst_title.append((driver_1.find_element_by_xpath('//*[@id="__next"]/div[3]/div[1]/div/div[4]/div[2]/h1')).text) 
                    lst_giaP.append(((driver_1.find_element_by_xpath("//*[@class='price___2UkjD']/span")).text).split('-')[0].strip())      
                    lst_TT.append((driver_1.find_element_by_xpath('//*[@id="__next"]/div[3]/div[1]/div/div[4]/div[2]/p')).text)
            except NoSuchElementException:
                print("Khong tim thay element") 
                driver_1.close()
                continue
            driver_1.close()       

    data = {
            "Tin tức" : lst_title, 
            "Diện tích" : lst_DT,
            'Giá phòng (tháng)' : lst_giaP,
            'Địa chỉ BĐS' : lst_Dc,
            'Thông tin thêm': lst_TT}
    
    df_data = pd.DataFrame.from_dict(data, orient='index')
    df_data = df_data.transpose()
    lst_STT = []
    for idx, i_row in df_data.iterrows():
        lst_STT.append(idx)
    df_data.insert(loc=0, column="STT", value=lst_STT)
    writer = pd.ExcelWriter(path + r"test.xlsx" ,engine="openpyxl")
    df_data.to_excel(writer, index=False, engine="openpyxl")
    writer.save()
    driver.close()
if __name__ == "__main__":
    print("bat dau")   
    Main()
    print("hoan thanh")    
                   
                    
                    
            
            
            