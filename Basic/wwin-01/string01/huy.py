# # import re
# file_Open = open("D:\Win\Train Python\Texx_string.txt", "rt")

# doc_file = file_Open.readlines()
# # # lst_new = []

# # # chuoi_cuaem = re.findall(r"\d{1,2}[./-]?[0-9]{0,9}", str(doc_file))

# # # i = 1
# # # while i <= len(chuoi_cuaem):
# # #     lst_new.append(str(i) + "-" + chuoi_cuaem[i-1])
# # #     i += 1

# # # file_moi = open("D:\Win\Train Python\Test_1.txt", "w+", encoding= "utf-8")
# # # file_moi.writelines("\n".join(lst_new))

# # # file_moi.close()


# # str_sdt = """
# # +84-345-123-4567
# # +84 333 123 4567
# # +84 300 123 4567
# # +84 321 123-4567
# # 0 345-540 5883
# # 0321-1234*56

# # +84 123-456-7890
# # (123) 456-7890
# # 123 456 7890
# # 123.456.7890
# # +91 (123) 456-7890

# # """
# # #[\+84|0]?.*[.\- ]?[0-9][.\- ]?[0-9][.\- ]?[0-9]
# # lst_sdt = re.findall("((\+\d{1,2}|0)[\s-])?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}", str_sdt)


# # print(lst_sdt)

# import regex
# import re

# str_A = '''
# lnffdggdfgdfgdflkl168543413434.
# 43533465145 354313154355,
# f41646464
# 316353613615631
# '''

# print(regex.findall('(?<=\w+)\d{1,}(?=\.)',str_A))
# str_1 = ['Thôn Quang Châu, Xã Hoà Châu, Huyện Hoà Vang, Thành phố Đà Nẵng', 'Huyện Hoà Vang, Thành phố Đà Nẵng'] 

# for x in str_1:
#     x.replace

# from unidecode import unidecode

# print(unidecode("Việt Nam Đất Nước Con Người"))
# print(unidecode("Welcome to Vietnam !"))
# print(unidecode("VIỆT NAM ĐẤT NƯỚC CON NGƯỜI"))
# print(df_loc_1)
# print(df_loc_2)
# str_input = str(12749)
# str_output = str_input[::-1] #94712
# list_output = list(str_output)

# maxx_lst = max(list_output)
# maxx_2 = []

# for i in range (len(list_output)):  
#     if list_output[i] < maxx_lst:
#         maxx_2.append(list_output[i])        
# print(max(maxx_2))

# import pandas as pd


# #//*[@class="news-v3 bg-color-white"]/div/div/div/h3/strong
# df_input_2 = pd.read_excel(r"D:\Win\Train Python\wwin-01\selenium02\Output_1.xlsx", "Sheet1", engine="openpyxl")
# df_out = df_input_2[0:0]
# lst_1 = ["1","2","3"]
  
# df_out["Đường dẫn"] = lst_1
# print(df_out)
# if "900.000 đ/tháng" <= "3 triệu/tháng":
#     print("yes")
# else:
#     print("no")
# import re
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import pandas as pd
# import time
# def open_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized") 
#     chrome_options.add_argument("--no-sandbox") 
#     chrome_options.add_argument("--disable-dev-shm-usage") 
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     driver = webdriver.Chrome(executable_path= r"D:\Win\Train Python\wwin-01\selenium03\chromedriver.exe",chrome_options=chrome_options)
#     #driver.implicitly_wait(5)
#     return driver




# def Main():
#     driver = open_driver()
#     str_input = input("Tinh thanh:")
     
#     driver.get("https://www.chotot.com/")
#     time.sleep(5)

#     ele_bds = driver.find_element_by_xpath('//*[@id="__next"]/main/main/div[3]/div[1]/div/div/li[1]/a/span')
#     ele_bds = driver.execute_script("arguments[0].click()", ele_bds)
#     #ele_bds.click()
#     time.sleep(3)

#     ele_chothue = driver.find_element_by_xpath('//*[@id="__next"]/main/div[2]/div[1]/div/li[2]/div/a[5]')
#     ele_chothue = driver.execute_script("arguments[0].click()", ele_chothue)
#     #ele_phongtro.click()
#     time.sleep(5)
#     ele_option = driver.find_element_by_xpath("//body/div[@id='__next']/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/span[2]")
#     ele_option = driver.execute_script("arguments[0].click()", ele_option)

#     #ele_option.click()
#     time.sleep(5)
#     lst_option = driver.find_elements_by_xpath('//*[@class="modal-body___23JBz undefined"]/div/div/ul/li/a')


#     for i, j in enumerate(lst_option):
#         if str(j.text) == str_input:
#             j.click()           
#             time.sleep(2)
#             break
#     time.sleep(5)
#     ele_all = driver.find_element_by_xpath('//body/div[7]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[1]/a[1]')
#     ele_all.click()  #driver.execute_script("arguments[0].click()", ele_all)
#     time.sleep(3)

    

#     driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

#     btn_next = driver.find_element_by_xpath('//*[@id="__next"]/div[3]/div/div[2]/main/div[2]/div[3]/div/div[10]')
#     btn_next = driver.execute_script("arguments[0].click()", btn_next)
#     time.sleep(3)
    
# if __name__ == "__main__":
#     print("bat dau")   
#     Main()
#     print("hoan thanh")

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# import pandas as pd
# import time

# def Open_Browser():
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized") 
#     chrome_options.add_argument("--no-sandbox") 
#     chrome_options.add_argument("--disable-dev-shm-usage") 
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     driver = webdriver.Chrome(executable_path= r"D:\Win\Train Python\wwin-01\selenium01\chromedriver.exe",chrome_options=chrome_options)   
#     return driver

# def Open_input():
#     df_input = pd.read_excel(r"D:\Win\Train Python\wwin-01\selenium01\Exercise_01 (Tai lieu)\Input.xlsx", "Sheet1",engine="openpyxl")
#     return df_input

# def Main():
#     df_Input = Open_input()
#     driver = Open_Browser()
#     for idx_input, row_input in df_Input.iterrows():
#         driver.get("https://thongtindoanhnghiep.co/")
       
#         element_1 = driver.find_element_by_id("TinhThanhIDValue")
#         lst_option_1 = element_1.find_elements_by_tag_name("option")
#         for option in lst_option_1:
            
#             print(option.text)


# if __name__ == "__main__":
#     print("bat dau")   
#     Main()
#     print("hoan thanh")


# #data_df_1 = pd.read_excel(r'D:\Win\Train Python\wwin-01\input\ISMS_DangKyLamViecTuXa.xlsx', sheet_name='Sheet 1',skiprows=3,skipfooter=10, header=1,engine="openpyxl")
# # list_header = data_df_1.columns.values

# for idx, row in data_df_2.iterrows():
#     # for idx_header ,i_header in enumerate(list_header): 
#     #     pass

# #     print(row['TCs'])
# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common import touch_actions 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.touch_actions import TouchActions
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import Select
# def Open_Browser():
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized") 
#     chrome_options.add_argument("--no-sandbox") 
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     #chrome_options.add_argument("--headless")
#     chrome_options.add_experimental_option('w3c', False)
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#     driver = webdriver.Chrome(executable_path= r"D:\Win\Train Python\wwin-01\selenium01\chromedriver.exe",chrome_options=chrome_options)   
#     return driver

    
# def Main():
#     driver = Open_Browser()
    # driver.get('https://thongtindoanhnghiep.co/')
    
    # wait = WebDriverWait(driver, 5)

    # elemet_TP = wait.until(EC.presence_of_element_located((By.ID,"TinhThanhIDValue")))
    # elemet_TP.click()
    # select_TP = Select(driver.find_element_by_id("TinhThanhIDValue"))
    # select_TP.select_by_value("/da-nang")
   
    # elemet_Q = wait.until(EC.presence_of_element_located((By.ID,"QuanHuyenIDValue")))
    # elemet_Q.click()
    # select_Quan = Select(driver.find_element_by_id("QuanHuyenIDValue"))
    # select_Quan.select_by_value("/da-nang/quan-hai-chau")
    
    # driver.find_element_by_xpath("//button[@class='btn-u btn-block']/i").click()
    # driver.forward()     
    # time.sleep(5)    
      
   
    # get geeksforgeeks.org
#     driver.get("https://www.geeksforgeeks.org/")
    
#     # get element 
#     element = driver.find_element_by_link_text("Courses")
    
#     # create action chain object
#     action = ActionChains(driver)
    
#     # click the item
#     action.click(on_element = element)
    
#     # perform the operation
#     action.perform()

#     driver.quit()
# if __name__ == "__main__":
#     print("bat dau")   
#     Main()
#     print("hoan thanh")
# data_df_2 = pd.read_excel(r'D:\Win\Train Python\wwin-01\BT_EXecl\File-1.xlsx',skiprows=2,engine="openpyxl")
# list_header = data_df_2.columns.values
# print(list_header) 
# lst_sdt = []
# for idx_input, row_input in data_df_2.iterrows():
                      
#     if "SỐ ĐIỆN THOẠI" in list_header[7]:
#         lst_sdt.append(re.findall(r"(?<=[SDĐ\s-])\d.+",str(row_input["SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)"])))  
# print(lst_sdt)
        
# import requests
# import os, inspect
# import base64
# from pandas import ExcelWriter
# import pandas as pd
# import glob
# import time
# CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# path =  os.path.abspath(CurDir+'\\hinhnen\\')

# file = glob.glob("D:\Win\Train Python\wwin-01\Store160\Image\\" + "*.jpg")
# for i in file:
#     print(i)
#str_i = "https://product.hstatic.net/1000253775/product/z2618387788662_0a95bcd3b6b6f46aad24a1e386b46fc3_ccd2d7e7f7cf4da98618a8bd50bae6f4_master.jpg"

# img_data = requests.get(str_i).content
# with open('D:\\Win\\Train Python\\wwin-01\\Store160\\Image\\' +'1_src.jpg', "wb") as crop:
#     crop.write(img_data)
#     crop.close()    



# import requests
# import base64
# # Making a get request
# response = requests.get(str_i)
# base_64 = response.content
# with open(r'D:\Win\Train Python\wwin-01\Youtube\\' + "1"+'_src.png', "wb") as crop:
#     crop.write(base_64)
#     crop.close()..

    
# from selenium.common.exceptions import NoSuchElementException
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# from time import sleep
# import os, inspect

# def main_function():
   
#     request = requests.get(r"https://thongtindoanhnghiep.co/tim-kiem?location=%2Fda-nang%2Fquan-hai-chau&kwd=")
#     soup = BeautifulSoup(request.content,"html.parser")
    
#     lst_items = soup.find_all("div",{"class":"news-v3"})

#     print(len(lst_items))

# if __name__ == "__main__":
    
#     main_function()
# import schedule
# import time
  
# # Functions setup
# def sudo_placement():
#     print("Get ready for Sudo Placement at Geeksforgeeks")
  
# def good_luck():
#     print("Good Luck for Test")
  
# def work():
#     print("Study and work hard")
  
# def bedtime():
#     print("It is bed time go rest")
      
# def geeks():
#     print("Shaurya says Geeksforgeeks")
  
# # Task scheduling
# # After every 10mins geeks() is called. 
# schedule.every(0.1).minutes.do(geeks)
  
# # After every hour geeks() is called.
# schedule.every().hour.do(geeks)
  
# # Every day at 12am or 00:00 time bedtime() is called.
# schedule.every().day.at("00:00").do(bedtime)
  
# # After every 5 to 10mins in between run work()
# schedule.every(5).to(10).minutes.do(work)
  
# # Every monday good_luck() is called
# schedule.every().monday.do(good_luck)
  
# # Every tuesday at 18:00 sudo_placement() is called
# schedule.every().tuesday.at("18:00").do(sudo_placement)
  
# # Loop so that the scheduling task
# # keeps on running all time.
# while True:
  
#     # Checks whether a scheduled task 
#     # is pending to run or not
#     schedule.run_pending()
#     time.sleep(1)

# importing the requests library

# import requests module


# import requests
# import json
 
# # url = "https://httpbin.org/post"
 
# headers = {"Content-Type": "application/json; charset=utf-8"}
 
# data = {
#     "id": 1001,
#     "name": "geek",
#     "passion": "coding",
# }
 
# payload = json.dumps(data)
# # response = requests.post(url, headers=headers, json=payload)
 
# # print("Status Code", response.status_code)
# # print("JSON Response ", response.json())
# import requests
  
# # Making a get request
# response = requests.post('https://httpbin.org/post',data=payload, headers= headers)

# # print response
# print(response.status_code)
  
# # print request object
# print(response.request)


import time
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
import pandas as pd
from time import sleep
from datetime import datetime   
import os, inspect
import requests
import glob
from PIL import Image
import base64


CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_img = os.path.abspath(CurDir +"\\capcha")
path_chrome = os.path.abspath(CurDir +"\\chromedriver.exe")

url_links = "https://canhan.gdt.gov.vn/ICanhan/Request?&dse_sessionId=Ey3gCMEC1wkj2DXU9T_sUOP&dse_applicationId=-1&dse_pageId=3&dse_operationName=retailUserLoginProc&dse_errorPage=error_page.jsp&dse_processorState=initial&dse_nextEventName=start"


def open_driver():

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    #chrome_options.add_argument("--headless") #chạy ngầm browwser
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('ignore-certificate-errors') ## fixx ssl
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--ignore-ssl-errors=yes")
    chrome_options.add_argument("--allow-insecure-localhost")
    driver = webdriver.Chrome(executable_path= path_chrome, chrome_options=chrome_options)

    return driver

def main():
    driver = open_driver()
    driver.get(url_links)

    element_capcha =driver.find_element_by_xpath('//*[@id="safecode"]')

    img_base64 = driver.execute_script("""
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    """, element_capcha)
    
    with open(r"image.jpg", 'wb') as f:
        f.write(base64.b64decode(img_base64))

    driver.quit()
if __name__ == "__main__":
    print("bat dau")   
    main()
    print("hoan thanh")