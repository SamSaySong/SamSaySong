from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import requests
from bs4 import BeautifulSoup
from time import sleep
import os, inspect

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path = os.path.abspath(CurDir + "\\input\\")
def open_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    # prefs = {"credentials_enable_service": False,               #tắt arlert save password chrome
    #     "profile.password_manager_enabled": False,
    #     "profile.managed_default_content_settings.images": 2}    # tắt image web 
    # chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument("--headless") #chạy ngầm browwser
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path= r"D:\Win\Train Python\wwin-01\selenium03\chromedriver.exe",chrome_options=chrome_options)
    return driver

def input():
    df_input = pd.read_excel(path+"\\Input.xlsx", sheet_name= "Sheet1",engine="openpyxl")
  
    return df_input

def main_function():
    df_input_1 = input()
    driver = open_driver()
    driver.get("https://thongtindoanhnghiep.co/")
    main_page = driver.current_window_handle
    
    lst_Tencty = []
    lst_MST = []
    lst_Ngaythanhlap = []
    lst_TP = []
    lst_Nganhnghe = []
    lst_Diachi = []
    for idx, row in df_input_1.iterrows():
        element_TP = driver.find_element_by_id("TinhThanhIDValue")
        lst_option_1 = element_TP.find_elements_by_tag_name("option")
        for option in lst_option_1:
            if option.text == "Đà Nẵng":
                option.click()
                break
        sleep(3)
        element_Quan = driver.find_element_by_id("QuanHuyenIDValue")
        lst_option_2 = element_Quan.find_elements_by_tag_name("option")
        for option_2 in lst_option_2:
            if option_2.text == row[1]:
                option_2.click()
                break
        sleep(3)
       
        btn_submit = driver.find_element_by_xpath('//*[@id="fulltextSearch"]/div/section[4]/button')
        btn_submit = driver.execute_script("arguments[0].click()", btn_submit)
        sleep(3)
       
        url_now = driver.current_url
        for i in range(1,3):
            request = requests.get(url_now+"&p={}".format(i))
            soup = BeautifulSoup(request.content,"html.parser")
            
            lst_items = soup.find_all("div",{"class":"news-v3"})

            # lst_items[0].find("div").find("h2").find("a").get_text() #ten cty

            # lst_items[0].find("div").find("div",{"class":"row"}).find("div",{"class":"col-md-4"}).find("h3").find("strong").find("a").get_text() # MST

            # lst_items[0].find("div").find("div",{"class":"row"}).find("div",{"class":"col-md-4"}).find("p").find("a").get_text() # Thanh pho

            # lst_items[0].find("div").find("div",{"class":"row"}).find("div",{"class":"col-md-4"}).find("p").get_text().replace("Ngày thành lập: ","") # ngay thanh lap
            
            # lst_items[0].find("div").find("ul",{"class":"list-inline posted-info"}).find("li").find("a").find("strong").get_text() # nganh nghe chinh
            
            # lst_items[0].find("div").find("p").find("strong").get_text() #diachi

            for results in lst_items:
                lst_Tencty.append(results.find("div").find("h2").find("a").get_text())
                lst_MST.append(results.find("div").find("div",{"class":"row"}).find("div",{"class":"col-md-4"}).find("h3").find("strong").find("a").get_text())
            
                lst_Ngaythanhlap.append(results.find("div").find("div",{"class":"row"}).find_all("div",{"class":"col-md-4"})[2].find("p").get_text().replace("Ngày thành lập: ",""))
                
                lst_TP.append(results.find("div").find("div",{"class":"row"}).find_all("div",{"class":"col-md-4"})[1].find("p").find("a").get_text())
                
                lst_Nganhnghe.append(results.find("div").find("ul",{"class":"list-inline posted-info"}).find("li").find("a").find("strong").get_text())
            element_DC = driver.find_elements_by_xpath('//*[@class="news-v3 bg-color-white"]/div/p/strong')
            for i in range(len(element_DC)):
                lst_Diachi.append(element_DC[i].text)
                
            
        driver.switch_to.window(main_page)

    data = {"Tên công ty": lst_Tencty,
            "Mã số thuế": lst_MST,
            "Ngành nghề chính": lst_Nganhnghe,
            "Thành phố":lst_TP,
            "Ngày thành lập": lst_Ngaythanhlap,
            "Địa chỉ": lst_Diachi
            }
    
    df_output = pd.DataFrame(data)
    
    lst_STT = []
    for idx, i_row in df_output.iterrows():
        lst_STT.append(idx)
    df_output.insert(loc=0, column="STT", value=lst_STT)  

    
    writer = pd.ExcelWriter(CurDir+"\\Output_bs4.xlsx", sheet_name ="Sheet1",engine='openpyxl')
    df_output.to_excel(writer,"Sheet1",index=False,engine="openpyxl")
    writer.save()   
    driver.close()  


if __name__ == "__main__":
    print("bat dau")   
    main_function()



