import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def open_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path= r"D:\Win\Train Python\wwin-01\selenium03\chromedriver.exe",chrome_options=chrome_options)
    #driver.implicitly_wait(5)
    return driver
def open_input():
    df_input = pd.read_excel(r"D:\Win\Train Python\wwin-01\selenium03\output\Output.xlsx", "Sheet", engine="openpyxl")
    return df_input
def Main():
    driver = open_driver()
    str_input = input("Tinh thanh:")
    df_input = open_input()
    df_output = df_input[0:0] 
    driver.get("https://www.chotot.com/")
    time.sleep(5)
    
    ele_bds = driver.find_element_by_xpath('//*[@id="__next"]/main/main/div[3]/div[1]/div/div/li[1]/a/span')
    ele_bds = driver.execute_script("arguments[0].click()", ele_bds)
    #ele_bds.click()
    time.sleep(3)
   
    ele_chothue = driver.find_element_by_xpath('//*[@id="__next"]/main/div[2]/div[1]/div/li[2]/div/a[5]')
    ele_chothue = driver.execute_script("arguments[0].click()", ele_chothue)
    #ele_phongtro.click()
    time.sleep(5)
    ele_option = driver.find_element_by_xpath("//body/div[@id='__next']/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/span[2]")
    ele_option = driver.execute_script("arguments[0].click()", ele_option)

    #ele_option.click()
    time.sleep(5)
    lst_option = driver.find_elements_by_xpath('//*[@class="modal-body___23JBz undefined"]/div/div/ul/li/a')
    
    
    for i, j in enumerate(lst_option):
        if str(j.text) == str_input:
            j.click()           
            break
    time.sleep(5)
    
    ele_all = driver.find_element_by_xpath('//body/div[7]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/a[1]')
    ele_all = driver.execute_script("arguments[0].click()", ele_all)
    #ele_all.click()  
    time.sleep(5)                                
    
    lst_url = driver.find_elements_by_xpath('//*[@class="ListAds___3Mp16"]/ul/div/li/a')   
    lst_title = []
    lst_DT = []  #Diện tích
    lst_giaP = []  #Giá phòng (tháng)
    lst_Dc = []   #Địa chỉ BĐS
    lst_TT = []  #Thông tin thêm
    # Tin Tuc
    i = 1
    while i <= 2:  
        for i, k in enumerate(lst_url):        
            driver_1 = open_driver()
            driver_1.get(k.get_attribute("href"))
            time.sleep(5)
            lst_price = driver_1.find_element_by_xpath('//*[@id="__next"]/div[3]/div[1]/div/div[4]/div[2]/div[1]/div[1]/span/div/span/span/span[1]')
            lst_d = str(lst_price.text).split()
            if lst_price.text <= "3 triệu/tháng" or lst_d[1] == "đ/tháng":                              
                
                lst_DT.append((driver_1.find_element_by_xpath('//*[@id="__next"]/div[3]/div[1]/div/div[4]/div[2]/div[1]/div[1]/span/div/span/span/span[1]/span[*]')).text)
                # lst_title.append((driver_1.find_element_by_xpath('//*[@id="__next"]/div[3]/div[1]/div/div[4]/div[2]/h1')).text) 
                # lst_Dc.append((driver_1.find_element_by_xpath('//*[@id="__next"]/div[3]/div[1]/div/div[4]/div[2]/div[4]/div/div/div[2]/span')).text)
                # lst_giaP.append((driver_1.find_element_by_xpath('//*[@id="__next"]/div[3]/div[1]/div/div[4]/div[2]/div[1]/div[1]/span/div/span/span/span[1]')).text)               
                # lst_TT.append((driver_1.find_element_by_xpath('//*[@id="__next"]/div[3]/div[1]/div/div[4]/div[2]/p')).text)
                     
            driver_1.close()
        time.sleep(3)
        btn_next = driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div[2]/main/div[2]/div[3]/div/div[10]')
        btn_next = driver.execute_script("arguments[0].click()", btn_next)
        time.sleep(3)
        i+=1
    # df_output["Thông tin thêm"] = lst_TT
    # df_output["Giá phòng (tháng)"] = lst_giaP
    # df_output["Tin tức"] = lst_title
    #df_output["Diện tích"] = lst_DT
    # df_output["Địa chỉ BĐS"] = lst_Dc
    # writer = pd.ExcelWriter(r"D:\Win\Train Python\wwin-01\selenium03\output\Output_1.xlsx", sheet_name ="Sheet",engine='openpyxl')
    # df_output.to_excel(writer,"Sheet1",index=False,engine="openpyxl")      
    # writer.save()  
    print(lst_DT)
    driver.quit()
if __name__ == "__main__":
    print("bat dau")   
    Main()
    print("hoan thanh")