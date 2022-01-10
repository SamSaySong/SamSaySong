
import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pandas as pd
from time import sleep
from datetime import datetime
import os, inspect
import requests
import glob
import threading
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path =  os.path.abspath(CurDir+'\\Store160\\')
path_img = os.path.abspath(CurDir +"\\Image")
file_img = glob.glob(path_img + "\\*.jpg")

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

def Main_func(j):

    lst_Title = []
    lst_Price = []
    lst_Description = []
    lst_Phanloai = []

    #list sp 1 trang
    driver_1 = open_driver()
    driver_1.implicitly_wait(5)
    sleep(3)
    driver_1.get(j.get_attribute("href"))
    sleep(3)
    # for toàn bộ url 1 page
    element_tensp = driver_1.find_element_by_xpath("//*[@class='pro-name']/a")
    if str(element_tensp.text).find("Áo",0) != -1 or str(element_tensp.text).find("Quần",0) != -1:
        element_Title = driver_1.find_element_by_xpath("//*[@class='product-title']/h1")
        element_Price = driver_1.find_element_by_xpath("//*[@class='pro-price']")
        element_Description = driver_1.find_element_by_xpath("//*[@class='description-productdetail']/div/div")
                
        lst_Title.append(element_Title.text)
        lst_Phanloai.append((element_Title.text).split()[0])
        lst_Price.append(element_Price.text)
        lst_Description.append(element_Description.text)
        sleep(3)
        element_pict = driver_1.find_elements_by_xpath('//*[@id="product"]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]/img') 
        for x, y_src in enumerate(element_pict): 
            driver_2 = open_driver()
            driver_2.get(y_src.get_attribute("src"))
            sleep(2)
            img_data = requests.get(driver_2.current_url).content
            with open(path_img+"\\" +datetime.now().strftime("%H-%M-%S")+"-"+str(element_Title.text)+'.jpg', "wb") as crop:
                crop.write(img_data)
                crop.close() 
            driver_2.close()  
    else:
        print("Sản phẩm không đúng loại")
        sleep(1)
    driver_1.close()
    sleep(1)
        
    lst_Pict = []
    for img in file_img:
        lst_Pict.append(img)
    data = {
        "Tên Sản Phẩm": lst_Title,
        "Giá Sản Phẩm": lst_Price,
        "Loại": lst_Phanloai,
        "Thông tin Sản phẩm": lst_Description,    
        "Hình ảnh sản phẩm":lst_Pict,
    }
    
    df_data = pd.DataFrame.from_dict(data)
    print(df_data)
    sleep(1)        

    writer = pd.ExcelWriter(path +r"Sản_phẩm.xlsx" ,engine="openpyxl")
    df_data.to_excel(writer,sheet_name="Sản phẩm",index= False,engine="openpyxl")
    writer.save()
    
def chia_mang(step_threads):
    driver = open_driver()
    driver.implicitly_wait(5)
    driver.get("https://www.160store.com/")
    sleep(2)
    ele_SP = driver.find_element_by_xpath('//*[@id="nav"]/nav/ul/li[3]/a')
    ele_SP = driver.execute_script("arguments[0].click()", ele_SP)
    sleep(3)   
    lst_Urlsp = driver.find_elements_by_xpath("//*[@class='product-img']/a")
    #print(lst_Urlsp)
    url_now = driver.current_url  #lấy url trang hiện tại
    for i in range(1,2):
        driver.get(url_now+"?page="+str(i))
        sleep(3)
        for j in range(step_threads, len(lst_Urlsp), 2):
            Main_func(lst_Urlsp[j])
    driver.quit()

if __name__ == "__main__":
  
    lst_thread = []
    for i in range(1):
        new_thread = threading.Thread(target=chia_mang, args=(i,))
        lst_thread.append(new_thread)
        new_thread.start()
        sleep(5)
    for i in lst_thread:
        i.join()
        