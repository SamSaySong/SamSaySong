
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import base64
def Open_Browser():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path= r"D:\Win\Train Python\wwin-01\selenium01\chromedriver.exe",chrome_options=chrome_options)   
    return driver

def Main():
    
    x = 4059
    while x <= 8000: 
        driver = Open_Browser() 
        driver.get("https://dichvucong.baohiemxahoi.gov.vn/#/index")
        btn_BHXH = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/div/div[3]/div/ul/li[2]/a')
        btn_BHXH = driver.execute_script('arguments[0].click()', btn_BHXH)
        time.sleep(3) 
        capcha = driver.find_elements_by_xpath('//body/div[1]/div[2]/div[1]/mat-dialog-container[1]/app-dialog-login[1]/form[1]/div[1]/div[2]/div[1]/div[1]/img[1]')
        time.sleep(5) 
        
        for i, j in enumerate(capcha): 
            #lst_capcha.append(j.get_attribute('src'))
            #driver_1 = Open_Browser()
            #driver_1.get(j.get_attribute("src"))
            #driver_1.save_screenshot('D:\\Win\\Train Python\\wwin-01\\selenium03\\capcha\\image\\' + str(x)+'_src.png')
            img_base64 = str(j.get_attribute("src")).split(",")
            img_crop = img_base64[1].encode()
            time.sleep(3)
           
            with open('D:\\Win\\Train Python\\wwin-01\\selenium03\\capcha\\image\\' + str(x)+'_src.png', "wb") as crop:
                crop.write(base64.decodebytes(img_crop))
            crop.close()
            driver.close()
            
        x+=1
        time.sleep(3)
        
    driver.quit()
if __name__ == "__main__":
    print("bat dau")   
    Main()
    print("hoan thanh")