
from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
from PIL import Image

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_chrome = os.path.abspath(CurDir +"\\chromedriver.exe")

url_links = r"https://dichvucong.baohiemxahoi.gov.vn/#/index?login=1&url=%2Fke-khai%2Fke-khai-don-vi&queryUrl="

def open_driver():

    chrome_options = Options()
    prefs = {"credentials_enable_service": False,    
    "profile.password_manager_enabled": False,}   #tắt arlert save password chrome 
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument("--ignore-ssl-errors=yes")
    # chrome_options.add_argument("--allow-insecure-localhost")
    # chrome_options.add_argument('ignore-certificate-errors') ## fixx ssl
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    # chrome_options.add_argument("--allow-running-insecure-content")
    # chrome_options.add_argument("--headless") #chạy ngầm browwser

    driver = webdriver.Chrome(executable_path= path_chrome, chrome_options= chrome_options)
    return driver


def select_xpath_options(driver, xpath_select, xpath_options, input_option, timeout = 1):

    driver.find_element_by_xpath(xpath_select).click()
    sleep(timeout)

    for i, j in enumerate(driver.find_elements_by_xpath(xpath_options)):
        # print(j.text)
        #  or str(j.text).strip() in input option
        if str(j.text).strip() == input_option:
            j.click()
            break

def select_options_thutuc(driver, kekhai_thang, kekhai_nam, dot_kekhai):

    input_Kykekhai_thang = driver.find_element_by_xpath('//*[@class="col-md-3 col-3 col-xl-3"]/mat-form-field/div/div/div/input')
    input_Kykekhai_thang.clear()
    input_Kykekhai_thang.send_keys(kekhai_thang)

    input_Kykekhai_nam = driver.find_element_by_xpath('//*[@class="col-md-3 col-3 col-xl-3 namkh"]/mat-form-field/div/div/div/input')
    input_Kykekhai_nam.clear()
    input_Kykekhai_nam.send_keys(kekhai_nam)

    input_Dotkekhai = driver.find_element_by_xpath('//*[@placeholder="Nhập đợt kê khai" and @formcontrolname="dot"]')
    # options Ma thu tuc
    select_xpath_options(driver, '//*[@placeholder="Chọn mã thủ tục" and @aria-label="Chọn mã thủ tục"]', "/html[1]/body[1]/div[1]/div[2]/div[1]/div[1]/div[1]/mat-option[*]", input_option= dot_kekhai)

    # Sreach
    btn_Sreach = driver.find_element_by_xpath('/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[6]/button')
    btn_Sreach.click()
    sleep(3)

def ma_Coquan(driver):

    driver.find_element_by_xpath('//*[@class="ng-star-inserted"]/div[2]/button').click()
    sleep(1)
    input_Macoquan = driver.find_element_by_xpath('//*[@class="col-md-12"]/div[4]/div/mat-form-field/div/div/div/input')

    return input_Macoquan

def main():
    "quy trình 630"

    driver = open_driver()
    driver.get(url_links)
    #  ----- LOGIN -------------------------

    # checkbox_Tochuc
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
    sleep(4)
    # -----------------------------------------------------------
    
    str_Macoquan =  ma_Coquan(driver).get_attribute('value').strip()
    # print(str_Macoquan.get_property('value'))

    driver.get("https://dichvucong.baohiemxahoi.gov.vn/#/ke-khai/thu-tuc-don-vi/lich-su-ke-khai")
    # menu_Lichsukekhai = driver.find_element_by_xpath('/html/body/app-root/ke-khai-layout/div/app-siderbar/div/div/ul/li[3]/a')
    # driver.execute_script("arguments[0].click();", menu_Lichsukekhai)
    sleep(3)
    # for list ho so--
    try:
        claim_Kykekhai_thang = "3"
        claim_Kykekhai_nam = "2021"
        claim_Mathutuc = "630a"

        select_options_thutuc(driver, claim_Kykekhai_thang, claim_Kykekhai_nam, claim_Mathutuc)

        dict_Trangthai ={
                        "Đã lưu tạm":"0",
                        "Đã nộp":"1",
                        }
        list_Trangthai = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[7]")
        list_Dotkekhai = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[4]")
        list_Kykekhai = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[5]")
        list_Mathutuc = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[2]")

        
        for idx_Kykekhai, intput_Kykekhai in enumerate(list_Kykekhai):
            
            intput_Kykekhai = str(intput_Kykekhai.text).strip().replace("/", "-")
            input_Dotkekhai = str(list_Dotkekhai[idx_Kykekhai].text).strip()
            input_Trangthai = str(list_Trangthai[idx_Kykekhai].text).strip()
            
           
            # Switch to tab the new window
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            # get page thông tin hồ sơ từng NV
            driver.get("https://dichvucong.baohiemxahoi.gov.vn/#/ke-khai/thu-tuc-don-vi/" +str(claim_Mathutuc)+ "/ke-khai/"+str(str_Macoquan)+"/"+ intput_Kykekhai+ "/" +input_Dotkekhai+ "?clone=0&view="+ dict_Trangthai[input_Trangthai]) 
            sleep(4)
                            
            social_insurance_number = "7936762274"
            claim_bh_tu_ngay = "09/01/2021"
                                    
            list_SOBHXH = driver.find_elements_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr[*]/td[3]/p')

            for idx_BHXH, i_BHXH in enumerate(list_SOBHXH):

                list_Ngaynghi_batdau = driver.find_elements_by_xpath('//*[@id="cdk-accordion-child-0"]/div/div/table/tbody/tr[*]/td[8]/p')
                list_CMND = driver.find_elements_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr[*]/td[4]/p')
                
                if str(i_BHXH.text).strip() == social_insurance_number and (list_Ngaynghi_batdau[idx_BHXH].text).strip() == claim_bh_tu_ngay:
                    print("đúng số HS")
                    driver.execute_script("window.close('');")   # Close tab
                    driver.switch_to.window(driver.window_handles[0])

                    # check trạng thái HS
                    if input_Trangthai != "Đã lưu tạm":
                        button_Nop = driver.find_element(By.XPATH,"/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr["+str(idx_Kykekhai+1)+"]/td[8]/button")
                        driver.execute_script("arguments[0].click();", button_Nop)
                        sleep(2)

                        dct_cacbuocxuli = quatrinhnop_HS(driver)
                        print("Update trạng thái "+ input_Trangthai +"\n"+str(dct_cacbuocxuli))
                    else:
                        print("Trạng thái chưa cập nhật")
                    break

                else:
                    driver.execute_script("window.close('');")   # Close tab
                    driver.switch_to.window(driver.window_handles[0]) 
                    print("số BHXH hoặc ngày nghỉ không chính xác")
                    break
            sleep(3)      
    except Exception as e:    
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)                     
    driver.quit()  

def quatrinhnop_HS(driver):
    "Get thông tin các bước xử lí Hồ sơ"
    
    # Test dữ liệu
    # dct_All = {"form":[]}

    # dct_table = { "Bước": "",
    #         "Tên cơ quan": "",
    #         "Phòng ban xử lý": "",
    #         "Thời gian gửi":"",
    #         "Trạng thái hồ sơ":"",
    #         "Desc": []         
    #     }
    # dict_con = {
    #             "STT": [],
    #             "Cán bộ xử lý":[],
    #             "Hành động": [],
    #             "Thời gian xử lý":[],
    #             }
    
    
    list_ele_desc = driver.find_elements_by_xpath('//*[@class="modal-body body-fixed scroll-custom"]/div[*]/div[2]/div/table/tbody/tr/td')


    button_arrow = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[1]')
    hd_Buoc = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[2]')
    hd_Tencoquan = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[3]')
    hd_Phongbanxuly = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[4]')
    hd_Thoigiangui = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[5]')
    hd_Trangthaihoso = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[6]')
    lst_Step = ""
    # lst_Desc = []
    # for từng bước 
    for idx_button_arrow, i_button_arrow in enumerate(button_arrow) :
        i_button_arrow.click()
        list_row_step = driver.find_elements_by_xpath('//*[@class="modal-body body-fixed scroll-custom"]/div['+str(idx_button_arrow+2)+']/div[1]/div')
        list_row_desc = driver.find_elements_by_xpath('//*[@class="modal-body body-fixed scroll-custom"]/div/div[2]/div/table/tbody/tr/td')

        for idx_row_step, i_row_step in enumerate(list_row_step):
            lst_Step +=i_row_step.text + "|"
        lst_Step+="\n"
        for idx_desc, i_desc in enumerate(list_row_desc):
            lst_Step += i_desc.text +"|"
        lst_Step+="\n"

        sleep(3)
        sleep(3)
        i_button_arrow.click()
        sleep(1)
    #     dct_table["Bước"] = str(hd_Buoc[idx_button_arrow].text)
    #     dct_table["Tên cơ quan"] = hd_Tencoquan[idx_button_arrow].text
    #     dct_table["Phòng ban xử lý"] = hd_Phongbanxuly[idx_button_arrow].text
    #     dct_table["Thời gian gửi"] = hd_Thoigiangui[idx_button_arrow].text
    #     dct_table["Trạng thái hồ sơ"] = hd_Trangthaihoso[idx_button_arrow].text


        # element_rowTr = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]')
        # element_rowTd = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td')
        # ele_STT = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[1]')
        # ele_Canboxuly = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[2]')
        # ele_Hanhdong = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[3]')
        # ele_Thoigianxuly = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[4]')

        # for STT mỗi bước 
        # for idx, stt in enumerate(ele_STT):
        #     dict_con["STT"].append(stt.text)
        #     dict_con["Cán bộ xử lý"].append(ele_Canboxuly[idx].text)
        #     dict_con[ "Hành động"].append(ele_Hanhdong[idx].text)
        #     dict_con["Thời gian xử lý"].append(ele_Thoigianxuly[idx].text)

        # dct_table["Desc"].append(dict_con)
        # dct_All["form"].append(dct_table)

    
        
        # dict_con = {
        #     "STT": [],
        #     "Cán bộ xử lý":[],
        #     "Hành động": [],
        #     "Thời gian xử lý":[],
        #     }

        # dct_table = { "Bước": "",
        #         "Tên cơ quan": "",
        #         "Phòng ban xử lý": "",
        #         "Thời gian gửi":"",
        #         "Trạng thái hồ sơ":"",
        #         "Desc": [],           
        #     } 
    try:              
        btn_dong = driver.find_element_by_xpath('//*[@class="cdk-overlay-pane"]/mat-dialog-container/app-dialog-qua-trinh-xu-ly/div/div[3]/button')
        btn_dong.click()
        # driver.execute_script("arguments[0].click();", btn_dong)
        sleep(2)
    except Exception as e:
        print("chua co nut dong" + e)
    return lst_Step

if __name__ == "__main__":   
    main()    



