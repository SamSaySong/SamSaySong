from types import prepare_class
from typing import KeysView
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

def select_xpath_options_split(driver, xpath_select, xpath_options, input_option, timeout = 1):
    "sreach options Chọn phương án"

    input_chonphuongan= driver.find_element_by_xpath(xpath_select)
    input_chonphuongan.click()
    input_chonphuongan.send_keys(input_option)    # Search option
    sleep(5)
    # xpath_scroll = driver.find_element_by_xpath('//*[@class="cdk-overlay-pane"]/div/mat-option[10]')
    # driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", xpath_scroll)
    for i, j in enumerate(driver.find_elements_by_xpath(xpath_options)):
        # str(j.text).split("-").strip()[0]

        #  or str(j.text).strip() in input option
        if str(j.text).split("-")[0].strip() in input_option:
            j.click()
            sleep(timeout)
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

    # data test
    list_TT = [
                {
                    "Name": "Phan Nguyễn Đăng Khoa",
                    "Số BHXH":"7936762274",
                    "Phân loai":"Tăng lao động",
                    "Options":"TM",
                },
                {
                    "Name": "Phạm Nguyễn Tường Vy",
                    "Số BHXH":"7916436045",
                    "Phân loai":"Tăng lao động",
                    "Options":"TL",

                },
                {
                    "Name": "Huỳnh Văn Anh Tuấn",
                    "Số BHXH":"7910119655",
                    "Phân loai":"Tăng lao động",
                    "Options":"TH",

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
        sleep(1)

        # Check select Phan Loai
        check_element(driver,'//*[@class="col-md-3"]/mat-form-field/div/div//div/mat-select', 10)

        # select options Phan Loai
        select_xpath_options(driver, '//*[@class="col-md-3"]/mat-form-field/div/div//div/mat-select', '//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option/span', input_option= tt["Phân loai"])

        btn_Apdung = driver.find_element_by_xpath('//*[@id="footer-dialog"]/button[1]')
        driver.execute_script("arguments[0].click();", btn_Apdung)     
        sleep(2)

        # element_TT_BHXH = driver.find_elements_by_xpath('//*[@class="table-box table-height"]/div/div/table/tbody/tr/td[4]/p')
        check_element(driver,'//*[@class="table-box table-height"]/div/div/table/tbody/tr/td[4]/p')
        
        maso_BHXH(driver, '//*[@class="table-box table-height"]/div/div/table/tbody/tr/td[4]/p', tt["Số BHXH"])
        # check mã số BHXH => kê khai
        ke_khai(driver, tt)

    # Lưu kê khai
    btn_Luu = driver.find_element_by_xpath('//body/app-root[1]/ke-khai-layout[1]/div[1]/div[1]/app-thutuc-donvi[1]/div[1]/div[1]/form[1]/div[1]/div[1]/button[1]')
    sleep(15)

    # driver.execute_script("arguments[0].click();", btn_Luu)

    # Submit kê khai
    # btn_Kekhai = driver.find_element_by_xpath('/html/body/app-root/ke-khai-layout/div/div/app-thutuc-donvi/div/div/form/div/div/button[2]').click()
    driver.quit()

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

def ke_khai(driver, data_claim):
    "Form kê khai thông tin"

    try:
        check_element(driver, '//*[@class="cl-B ng-star-inserted"]/bhxh-input/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div/div/input')
       
        select_xpath_options_split(driver,'//*[@class="cl-B ng-star-inserted"]/bhxh-input/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div/div/input', '//*[@class="cdk-overlay-pane"]/div/mat-option', input_option=data_claim["Options"])
        sleep(2)

        claim_CMND = "1"
        if claim_CMND != "":
            input_CMND = driver.find_element_by_xpath('//*[@class="cl-5 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_CMND)
            input_CMND.send_keys(claim_CMND)

        #  Cấp bậc, chức vụ, chức danh nghề, nơi làm việc ---
        claim_Noilamviec = "1"
        if claim_Noilamviec != "":
            input_Noilamviec = driver.find_element_by_xpath('//*[@class="cl-7 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/textarea')
            driver.execute_script("arguments[0].click();", input_Noilamviec)
            input_Noilamviec.send_keys(claim_Noilamviec)

        claim_Phongban = "1"
        if claim_Phongban != "":
            input_Phongban = driver.find_element_by_xpath('//*[@class="cl-8 ng-star-inserted"]/bhxh-input/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_Phongban)
            input_Phongban.send_keys(claim_Phongban)

        claim_Nhaquanli_TuNgay = "21/10/2021"
        claim_CMKTcao_TuNgay = ""
        claim_CMKTtrung_TuNgay = ""
        claim_Khac_TuNgay = ""

        # Vị trí việc làm ---

        if claim_Nhaquanli_TuNgay != "":
            # Nhà quản lý
            input_Nhaquanli_TuNgay = driver.find_element_by_xpath('//*[@class="cl-9 ng-star-inserted"]/div/bhxh-input[1]/div/div/div/mat-form-field/div/div/div[1]/input')
            driver.execute_script("arguments[0].click();", input_Nhaquanli_TuNgay)
            input_Nhaquanli_TuNgay.send_keys(claim_Nhaquanli_TuNgay)
            
            input_Nhaquanli_DenNgay = driver.find_element_by_xpath('//*[@class="cl-9 ng-star-inserted"]/div/bhxh-input[2]/div/div/div/mat-form-field/div/div/div[1]/input')
            driver.execute_script("arguments[0].click();", input_Nhaquanli_DenNgay)
            claim_Nhaquanli_DenNgay="22/10/2021"
            input_Nhaquanli_DenNgay.send_keys(claim_Nhaquanli_DenNgay)

        elif claim_CMKTcao_TuNgay != "":
            # Chuyên môn kĩ thuật bậc cao	
            input_CMKTcao_TuNgay = driver.find_element_by_xpath('//*[@class="cl-10 ng-star-inserted"]/div/bhxh-input[1]/div/div/div/mat-form-field/div/div/div[1]/input')
            driver.execute_script("arguments[0].click();", input_CMKTcao_TuNgay)
            input_CMKTcao_TuNgay.send_keys(claim_CMKTcao_TuNgay)
            
            input_CMKTcao_DenNgay = driver.find_element_by_xpath('//*[@class="cl-10 ng-star-inserted"]/div/bhxh-input[2]/div/div/div/mat-form-field/div/div/div[1]/input')
            driver.execute_script("arguments[0].click();", input_CMKTcao_DenNgay)
            claim_CMKTcao_DenNgay="22/10/2021"
            input_CMKTcao_DenNgay.send_keys(claim_CMKTcao_DenNgay)

        elif claim_CMKTtrung_TuNgay != "":
            # Chuyên môn kĩ thuật bậc trung	
            input_CMKTtrung_TuNgay = driver.find_element_by_xpath('//*[@class="cl-11 ng-star-inserted"]/div/bhxh-input[1]/div/div/div/mat-form-field/div/div/div[1]/input')
            driver.execute_script("arguments[0].click();", input_CMKTtrung_TuNgay)
            input_CMKTtrung_TuNgay.send_keys(claim_CMKTtrung_TuNgay)
            
            input_CMKTtrung_DenNgay = driver.find_element_by_xpath('//*[@class="cl-11 ng-star-inserted"]/div/bhxh-input[2]/div/div/div/mat-form-field/div/div/div[1]/input')
            driver.execute_script("arguments[0].click();", input_CMKTtrung_DenNgay)
            claim_CMKTtrung_DenNgay = ""
            input_CMKTtrung_DenNgay.send_keys(claim_CMKTtrung_DenNgay)

        elif claim_Khac_TuNgay != "":
            # Khác
            input_Khac_TuNgay = driver.find_element_by_xpath('//*[@class="cl-12 ng-star-inserted"]/div/bhxh-input[1]/div/div/div/mat-form-field/div/div/div[1]/input')
            driver.execute_script("arguments[0].click();", input_Khac_TuNgay)
            input_Khac_TuNgay.send_keys("21/10/2021")
            
            input_Khac_DenNgay = driver.find_element_by_xpath('//*[@class="cl-12 ng-star-inserted"]/div/bhxh-input[2]/div/div/div/mat-form-field/div/div/div[1]/input')
            driver.execute_script("arguments[0].click();", input_Khac_DenNgay)
            claim_Khac_DenNgay = ""
            input_Khac_DenNgay.send_keys(claim_Khac_DenNgay)
        sleep(1)

        # checkbox Có giảm chết ---
        input_Cogiamchet = False
        if input_Cogiamchet == True:

            checkbox_Cogiamchet = driver.find_element_by_xpath('//*[@class="cl-14 ng-star-inserted"]/bhxh-input/div/div/div/div/mat-checkbox/label/div/input')
            driver.execute_script("arguments[0].click();", checkbox_Cogiamchet)

            input_Ngaychet = driver.find_element_by_xpath('//*[@class="cl-15 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_Ngaychet)
            input_Khac_DenNgay.send_keys("22/10/2021")
        sleep(1)

        # Tiền lương -- Phụ cấp
        claim_Phucapluong = ""
        if claim_Phucapluong != "":
            input_Phucapluong = driver.find_element_by_xpath('//*[@class="cl-23 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_Phucapluong)
            input_Phucapluong.clear()
            input_Phucapluong.send_keys(claim_Phucapluong)
        
        claim_Cackhoanbosung = ""
        if claim_Cackhoanbosung != "":
            input_Cackhoanbosung = driver.find_element_by_xpath('//*[@class="cl-24 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_Cackhoanbosung)
            input_Cackhoanbosung.clear()
            input_Cackhoanbosung.send_keys(claim_Cackhoanbosung)

        # Ngành/nghề nặng nhọc, độc hại ---
        claim_Nganhnghe_Ngaybatdau = ""
        if claim_Nganhnghe_Ngaybatdau != "":
            input_Nganhnghe_Ngaybatdau = driver.find_element_by_xpath('//*[@class="cl-25 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_Nganhnghe_Ngaybatdau)
            input_Nganhnghe_Ngaybatdau.send_keys("21/10/2021")
            
            input_Nganhnghe_Ngayketthuc = driver.find_element_by_xpath('//*[@class="cl-26 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_Nganhnghe_Ngayketthuc)
            input_Nganhnghe_Ngayketthuc.send_keys("22/10/2021")
            sleep(1)

        # Loại và hiệu lực hợp đồng lao động ----
        claim_HDLD_khongthoihan_Ngaybatdau = "21/10/2021"
        claim_HDLD_thoihan_Ngaybatdau = ""
        claim_HDLD_khac_Ngaybatdau = ""

        if claim_HDLD_khongthoihan_Ngaybatdau != "":
            # HĐLĐ Không xác định thời hạn
            input_HDLD_khongthoihan_Ngaybatdau = driver.find_element_by_xpath('//*[@class="cl-27 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_HDLD_khongthoihan_Ngaybatdau)
            input_HDLD_khongthoihan_Ngaybatdau.send_keys(claim_HDLD_khongthoihan_Ngaybatdau)

        elif claim_HDLD_thoihan_Ngaybatdau !="":
            # HĐLĐ Xác định thời hạn
            input_HDLD_thoihan_Ngaybatdau = driver.find_element_by_xpath('//*[@class="cl-28 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_HDLD_thoihan_Ngaybatdau)
            input_HDLD_thoihan_Ngaybatdau.send_keys(claim_HDLD_thoihan_Ngaybatdau)
            
            input_HDLD_thoihan_Ngayketthuc = driver.find_element_by_xpath('//*[@class="cl-29 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_HDLD_thoihan_Ngayketthuc)
            input_HDLD_thoihan_Ngayketthuc.send_keys(claim_HDLD_thoihan_Ngayketthuc = "22/10/2021")

        elif claim_HDLD_khac_Ngaybatdau !="":
            # Hiệu lực HĐLĐ Khác
            input_HDLD_khac_Ngaybatdau = driver.find_element_by_xpath('//*[@class="cl-30 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_HDLD_khac_Ngaybatdau)
            input_HDLD_khac_Ngaybatdau.send_keys("21/10/2021")
            
            input_HDLD_khac_Ngayketthuc = driver.find_element_by_xpath('//*[@class="cl-31 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_HDLD_khac_Ngayketthuc)
            input_HDLD_khac_Ngayketthuc.send_keys(claim_HDLD_khac_Ngayketthuc ="")
        sleep(1)

        # Tỷ lệ đóng
        claim_Tyledong = ""
        if claim_Tyledong != "":
            input_Tyledong = driver.find_element_by_xpath('//*[@class="cl-34 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
            driver.execute_script("arguments[0].click();", input_Tyledong)
            input_Tyledong.send_keys(claim_Tyledong)

        # Tính lãi
        input_Tinhlai = False
        if input_Tinhlai == True:
            checkbox_Tinhlai = driver.find_element_by_xpath('//*[@class="cl-35 ng-star-inserted"]/bhxh-input/div/div/div/div/mat-checkbox/label/div/input')
            driver.execute_script("arguments[0].click();", checkbox_Tinhlai)
            
        # Ghi chú
        claim_Ghichu = "123"
        if claim_Ghichu != "":
            input_Ghichu = driver.find_element_by_xpath('//*[@class="cl-36 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/textarea')
            driver.execute_script("arguments[0].click();", input_Ghichu)
            input_Ghichu.clear()
            input_Ghichu.send_keys(claim_Ghichu)
            sleep(1)
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, e)




                   
if __name__ == "__main__":
    print("Bắt đầu quy trình")   
    main()
    print("Hoàn thành")

