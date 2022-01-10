from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import os
import pandas as pd
from pandas import ExcelWriter
from time import sleep
from selenium.webdriver.chrome.options import Options
path_INPUT = r"D:\Win\Train Python\wwin-01\selenium01\Exercise_01 (Tai lieu)\Input.xlsx"
sheet_INPUT = "Sheet1"

#Xóa những task cũ
def Clear():
    os.system("taskkill /f /im chromedriver.exe")
    os.system("taskkill /f /im chrome.exe")

#Mở excel sử dụng thư viện pandas
def Read_Excel(path,sheet):
    df_INPUT = pd.read_excel(open(path,'rb'), sheet_name = sheet, dtype = object,engine="openpyxl")
    return df_INPUT

#Mở trình duyệt chromedriver sử dụng selenium
def Open_Browser():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path=r"D:\Win\Train Python\wwin-01\selenium01\chromedriver.exe", chrome_options=chrome_options)
    return driver

#Hàm xử lý chính
def Process_Main():
    df_INPUT = Read_Excel(path_INPUT,sheet_INPUT)
    driver = Open_Browser()
    for idx_INPUT, row_INPUT in df_INPUT.iterrows():
        driver.get('https://thongtindoanhnghiep.co/')
        element = driver.find_element_by_xpath("//select[@id='TinhThanhIDValue']")
        list_OPTIONS = element.find_elements_by_tag_name("option")
        for option in list_OPTIONS:
            if str(option.text) == "Đà Nẵng":
                option.click()  
                break
        sleep(5)
        element = driver.find_element_by_xpath("//select[@id='QuanHuyenIDValue']")
        list_OPTIONS = element.find_elements_by_tag_name("option")
        for option in list_OPTIONS:
            if str(option.text).strip() == str(row_INPUT[1]).strip():
                option.click()
                break

        #btn_submit = driver.find_element_by_xpath('//*[@id="fulltextSearch"]/div/section[4]/button').click()
        btn_submit = driver.find_element_by_xpath('//*[@id="fulltextSearch"]/div/section[4]/button')
        btn_submit = driver.execute_script("arguments[0].click()", btn_submit)

        list_URLS = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[3]/div[1]/div[*]/div/h2/a')


        for idx_url, i_url in enumerate(list_URLS):
            driver1 = Open_Browser()
            driver1.get(i_url.get_attribute("href"))
            driver1.save_screenshot("Output\\"+str(idx_url)+"_screenshot.png")
            driver1.quit()
       
    driver.quit()

#Phần thực thi
if __name__ == "__main__":
    print ("Bắt đầu quy trình")
    Clear()
    Process_Main()
    print ("Kết thúc quy trình")



# dfChotot.loc[index,'STT'] = str(index+1)

#     dfChotot.loc[index,'Tin tức'] = driver2.find_element_by_xpath('//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/h1').text

#     dfChotot.loc[index,'Thông tin thêm'] = driver2.find_element_by_xpath('//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/p').text

#     dfChotot.loc[index,'Địa chỉ BĐS'] = driver2.find_element_by_xpath('//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[3]/div/div[2]/div').text

#     dfChotot.loc[index,'Giá phòng (tháng)'] = (driver2.find_element_by_xpath('//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/span[1]/span[1]').text).split(' ')[0]

#     dfChotot.loc[index,'Diện tích'] = (driver2.find_element_by_xpath('//*[@id="app"]/div[2]/main/article/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/span[2]').text).split('-')[1].strip()

#     count+=1

#     if count==20:

#         break
