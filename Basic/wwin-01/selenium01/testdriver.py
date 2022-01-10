from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

def Open_Browser():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path= r"D:\Win\Train Python\wwin-01\selenium01\chromedriver.exe",chrome_options=chrome_options)   
    return driver

def Open_input():
    df_input = pd.read_excel(r"D:\Win\Train Python\wwin-01\selenium01\Exercise_01 (Tai lieu)\Input.xlsx", "Sheet1",engine="openpyxl")
    return df_input

def Main():
    df_Input = Open_input()
    driver = Open_Browser()
    for idx_input, row_input in df_Input.iterrows():
        driver.get("https://thongtindoanhnghiep.co/")
       
        element_1 = driver.find_element_by_id("TinhThanhIDValue")
        lst_option_1 = element_1.find_elements_by_tag_name("option")
        for option in lst_option_1:
            if option.text == "Đà Nẵng":
                option.click()
                break
        time.sleep(5)
        element_2 = driver.find_element_by_id("QuanHuyenIDValue")
        lst_option_2 = element_2.find_elements_by_tag_name("option")
        for option in lst_option_2:
            if (option.text) == row_input[1]:
                option.click()
                break
        

        btn_sub = driver.find_element_by_xpath('//*[@id="fulltextSearch"]/div/section[4]/button')
        btn_sub.click()                          
        lst_URLs = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/div[4]/div[1]/div[*]/div/h2/a")
        for j_dx, j_url in enumerate(lst_URLs):
            driver_1 = Open_Browser()
            driver_1.get(j_url.get_attribute("href"))
            driver_1.save_screenshot("D:\\Win\\Train Python\\wwin-01\\selenium01\\src_shot\\"+str(j_dx)+"_scr_shot.png")
            driver_1.close()

    driver.quit()


if __name__ == "__main__":
    print("bat dau")   
    Main()
    print("hoan thanh")