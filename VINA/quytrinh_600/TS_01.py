
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import pandas as pd
from time import sleep
from datetime import datetime   
import os, inspect, sys
import re
import glob
from pandas import ExcelWriter

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_img = os.path.abspath(CurDir +"\\capcha")
path_chrome = os.path.abspath(CurDir +"\\chromedriver.exe")

url_links = r"https://dichvucong.baohiemxahoi.gov.vn/#/index?login=1&url=%2Fke-khai%2Fke-khai-don-vi&queryUrl="


def open_driver():

    chrome_options = Options()
    prefs = {"credentials_enable_service": False,
            "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) # tắt popup của face
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    # chrome_options.add_argument("--ignore-ssl-errors=yes")
    # chrome_options.add_argument("--allow-insecure-localhost")
    # chrome_options.add_argument('ignore-certificate-errors') ## fixx ssl
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    # chrome_options.add_argument('--disable-gpu') 
    # chrome_options.add_argument("--allow-running-insecure-content")
    
    driver = webdriver.Chrome(executable_path= path_chrome, chrome_options=chrome_options)
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
            sleep(1)

def check_selector(driver, selector, int_Timeout=60):
    
    int_Count = 0
    while True:
        try:
            driver.find_element_by_css_selector(selector)
            return True
        except:
            if int_Count == int_Timeout:
                return False
            int_Count+=1
            sleep(1)

def select_xpath_options(driver, xpath_select, xpath_options, input_option, timeout = 1):

    driver.find_element_by_xpath(xpath_select).click()
    sleep(timeout)
    for i, j in enumerate(driver.find_elements_by_xpath(xpath_options)):
        # print(j.text)
        #  or str(j.text).strip() in input option
       
        if str(j.text).strip() == input_option:
            j.click()
            break
def main():

    driver = open_driver()
    driver.get(url_links)

    # Form login
    checkbox_Tochuc = driver.find_element_by_css_selector("#mat-checkbox-2-input")
    driver.execute_script("arguments[0].click();", checkbox_Tochuc)

    element_ID_MasoBHXH = driver.find_element_by_css_selector('#mat-input-0')
    element_ID_MasoBHXH.click()
    element_ID_MasoBHXH.send_keys("0314607162")

    element_Matkhau = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[2]/div[1]/mat-dialog-container[1]/app-dialog-login[1]/form[1]/div[1]/div[2]/mat-form-field[2]/div[1]/div[1]/div[2]/input[1]')
    element_Matkhau.click()
    element_Matkhau.send_keys("0314607162")

    input_captcha = driver.find_element_by_xpath('//*[@id="mat-input-2"]')
    input_captcha.click()
    input_captcha.send_keys(input("Nhap capcha:"))

    btn_login = driver.find_element_by_xpath('//*[@class="modal-footer"]/button[2]')
    btn_login.click()

    # check login thành công
    element_DSthutuc = check_element(driver, '//*[@class="active ng-star-inserted"]/a')
    if element_DSthutuc == True:
        print("Login thanh cong")
    sleep(3)

    check_element(driver,'//tbody/tr[1]/td[2]/button[1]')
    btn_600 = driver.find_element_by_xpath('//tbody/tr[1]/td[2]/button[1]')
    btn_600.click()
    sleep(3)

    # Form Chọn kỳ kê khai------
    check_element(driver,'//*[@id="footer-dialog"]/button[1]')
    btn_Xacnhan = driver.find_element_by_xpath('//*[@id="footer-dialog"]/button[1]')
    driver.execute_script("arguments[0].click();", btn_Xacnhan)
    sleep(3)

    # element_BV = driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]/div/div/div/mat-option/span/span/span')
    # data test
    list_TT = [
                {
                    "Name": "Phan Nguyễn Đăng Khoa",
                    "Số BHXH":"7936762274",
                    "Phân loai":"Tăng lao động",
                    "Options":"TM",
                }

            ]
    #  Lấy thông tin từng nhân viên
    for tt in list_TT:

        # Form kê khai---------------------------
        btn_Chonlaodong = driver.find_element_by_xpath('//*[@class="ke-khai"]/div/button')
        driver.execute_script("arguments[0].click();", btn_Chonlaodong)
        sleep(5)

        # Tìm kiếm lao động kê khai-------
        
        input_Hoten = driver.find_element_by_xpath('//*[@class="col-md-8 col-lg-8 col-xl-8 col-8"]/mat-form-field/div/div/div/input')
        # input_Hoten.click()
        driver.execute_script("arguments[0].click();", input_Hoten)
        input_Hoten.send_keys(tt["Name"])
        sleep(2)

        # btn_timkiem = wait.until(EC.presence_of_element_located(By.XPATH,'//*[@id="body-dialog"]/form/div/div[5]/button'))
        btn_timkiem = driver.find_element_by_xpath('//*[@id="body-dialog"]/form/div/div[5]/button')
        driver.execute_script("arguments[0].click();", btn_timkiem)
        sleep(2)

        # Form danh sách lao động

        # check mã số BHXH form danh sách lao động == mã số BHXH HS nhân viên
        danhsach_Nhanvien = driver.find_elements_by_xpath('//*[@id="body-dialog"]/div/table/tbody/tr[*]/td[3]')
        
        for i in range(len(danhsach_Nhanvien)):

            element_MS_BHXH = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="body-dialog"]/div/table/tbody/tr['+str(i+1)+']/td[7]')))
            
            select_Checkbox_NV = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="body-dialog"]/div/table/tbody/tr['+str(i+1)+']/td[2]/mat-checkbox/label/div/input')))
        
            if str(element_MS_BHXH.text).strip() == tt["Số BHXH"].strip():
                # select_Checkbox_NV.click()
                driver.execute_script("arguments[0].click();", select_Checkbox_NV)
                break


         # Check select Phan Loai
        check_element(driver,'//*[@class="col-md-3"]/mat-form-field/div/div//div/mat-select', 10)

        # select options Phan Loai
        select_xpath_options(driver, '//*[@class="col-md-3"]/mat-form-field/div/div//div/mat-select', '//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option/span', input_option= tt["Phân loai"])

        btn_Apdung = driver.find_element_by_xpath('//*[@id="footer-dialog"]/button[1]')
        driver.execute_script("arguments[0].click();", btn_Apdung)     
        sleep(2)

        check_element(driver,'//*[@class="table-box table-height"]/div/div/table/tbody/tr/td[4]/p')


        ke_khai(driver, tt)


def ke_khai(driver, data_claim):
    ele_TK1TS = '//*[@class="ke-khai"]/form/mat-tab-group/mat-tab-header/div[2]/div/div/div[2]'

    check_element(driver, ele_TK1TS)
    driver.find_element_by_xpath(ele_TK1TS).click()
    time.sleep(2)

    ele_KCB_bandau = driver.find_element_by_xpath('//*[@class="table-box table-height"]/div/div/div/table/tbody/tr/td[15]/p')
    ele_KCB_bandau.click()
    time.sleep(2)

    ele_TT_KCB = driver.find_element_by_xpath('//*[@class="table-holder table-height"]/table/tbody/tr/td[15]/bhxh-input/div/div/div/div/dia-chi-kcb/div/mat-form-field[1]/div/div/div/input')
    ele_TT_KCB.click()
    time.sleep(2)
    lst_TT_BV = []
    lst_Tinhthanh = driver.find_elements_by_xpath('//*[@class="cdk-overlay-container"]/div/div/div/mat-option/span/span/span')
    writer = pd.ExcelWriter('D:\\HuyNP\\VINA\\quytrinh_600\\output\\thongtin.xlsx', engine="xlsxwriter")

    for i_tinhthanh in range(len(lst_Tinhthanh)):
        lst_Tinhthanh = driver.find_elements_by_xpath('//*[@class="cdk-overlay-container"]/div/div/div/mat-option/span/span/span')

        str_tinhthanh = str(lst_Tinhthanh[i_tinhthanh].text).split("-")[1].strip()
        
        lst_Tinhthanh[i_tinhthanh].click()
        time.sleep(1)

        ele_BV_KCB = driver.find_element_by_xpath('//*[@class="table-holder table-height"]/table/tbody/tr/td[15]/bhxh-input/div/div/div/div/dia-chi-kcb/div/mat-form-field[2]/div/div/div/input')
        ele_BV_KCB.click()
        time.sleep(2)

        lst_BV = driver.find_elements_by_xpath('//*[@class="cdk-overlay-container"]/div/div/div/mat-option/span/span/span')

        for idx_bv, i_bv in enumerate(lst_BV):
            lst_TT_BV.append(i_bv.text)
        time.sleep(1)

        dct_data = { str_tinhthanh:lst_TT_BV,

                    }

        df_output = pd.DataFrame(dct_data)
        df_output.to_excel(writer, sheet_name=str(str_tinhthanh), index= False)
        lst_TT_BV=[]

        ele_TT_KCB = driver.find_element_by_xpath('//*[@class="table-holder table-height"]/table/tbody/tr/td[15]/bhxh-input/div/div/div/div/dia-chi-kcb/div/mat-form-field[1]/div/div/div/input')
        ele_TT_KCB.click()
        ele_TT_KCB.clear()
        time.sleep(1)

        button_X = driver.find_element_by_xpath('//*[@class="ng-star-inserted"]/dia-chi-kcb/div/mat-form-field[1]/div/div/div[2]/button')
        button_X.click()
        time.sleep(1)
    writer.save()
    

def maso_BHXH(driver, xpath, input_option, time_out=2):
    "check mã số BHXH form kê khai thông tin == mã số BHXH HS nhân viên"

    element_TT_BHXH = driver.find_elements_by_xpath(xpath)
    sleep(time_out)

    for idx_element, ele_BHXH in enumerate(element_TT_BHXH):
        if str(ele_BHXH.text).strip() == input_option.strip():
            # ele_BHXH.click()
            driver.execute_script("arguments[0].click();", ele_BHXH)
            sleep(time_out)
            break

if __name__ == "__main__":
  
    main()
    