
import datetime
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
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
import time
import os, inspect, sys
import re
import glob
from PIL import Image
import ocr_capcha
import shutil

# path_folder_input = glob.glob(os.path.abspath(CurDir +"\\input") + "\\*\\")

# for folder in path_folder_input:
    
#     path_file_input = glob.glob(os.path.abspath(folder) + "\\*.xlsx")

#     for file in path_file_input:

#         df_input = pd.read_excel(file, engine="openpyxl", dtype=object)
#         print(df_input)
# ---------------------------------------------------------------------------------------------------


CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

path_img = os.path.abspath(CurDir +"\\capcha")
path_chrome = os.path.abspath(CurDir +"\\chromedriver.exe")



url_links = "https://canhan.gdt.gov.vn/ICanhan/Request?&dse_sessionId=FL0nfXSCuBQ84-Vvo3MKhSr&dse_applicationId=-1&dse_pageId=3&dse_operationName=retailUserLoginProc&dse_errorPage=error_page.jsp&dse_processorState=initial&dse_nextEventName=start"

import logging
global LOG_INFO
name_Organization = "vpo"
name_Robot = "P.I.T"
name_Version = "1.1.6"
name_Config = "config_pj-vpo_robot.json"
name_Logs = "logs_pj-vpo_robot.txt"


# --- HÀM HỖ TRỢ ---
def readJson(str_Path):
    #!/usr/bin/env python
    import chardet # $ pip install chardet
    import json
    # detect file encoding
    with open(str_Path, 'rb') as data_file:
        raw = data_file.read(32) # at most 32 bytes are returned
        encoding = chardet.detect(raw)['encoding']
    with open(str_Path, encoding=encoding) as data_file:
        data = json.loads(data_file.read())
    return data

data_config = readJson(CurDir+"\\conf\\"+name_Config)

path_Input = data_config["thu_muc_input"]
path_Move_input = data_config["thu_muc_move_input"]
path_Output = data_config["thu_muc_output"]
path_File_import = data_config["thu_muc_import"]



logging.basicConfig(format='------------------ %(asctime)s >>>  %(message)s  <<<------------------', datefmt='%d/%m/%Y %H:%M:%S')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s",datefmt='%d/%m/%Y %H:%M:%S')
LOG_INFO = logging.warning
LOG_ERROR = logging.error
FileHandler = logging.FileHandler(CurDir+"\\"+ name_Logs, 'a+', 'utf-8')
FileHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(FileHandler)


# --------------------------------------- #
def path_input():
    "Check folder input" 
    path_folder_input = glob.glob(os.path.abspath(path_Input) + "\\*\\")
    # print(path_folder_input)
    return path_folder_input

def path_move_input():
     
    path_folder_move_input = glob.glob(os.path.abspath(path_Move_input) + "\\*\\")
    
    return path_folder_move_input

def convert_datetime_string(data_input,format_input='%Y-%m-%d',format_output='%d/%m/%Y'):
    import datetime
    data_date = datetime.datetime.strptime(data_input, format_input)
    data_date = data_date.strftime(format_output)
    return data_date

def open_driver():

    chrome_options = Options()
    prefs = {"credentials_enable_service": False,  
    "profile.password_manager_enabled": False }  # tắt arlert save password chrome
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--ignore-ssl-errors=yes")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument('ignore-certificate-errors') ## fixx ssl
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    # chrome_options.add_argument("--allow-running-insecure-content")
    # chrome_options.add_argument("--headless") #chạy ngầm browwser
    driver = webdriver.Chrome(executable_path= path_chrome, chrome_options=chrome_options)

    return driver


def screen_capcha(driver, Curdir, xpath_capcha, count_k, bl_a = False):

    if bl_a == True:
        # get location captcha 2
        driver.save_screenshot(Curdir +"\\screen_shot\\" + str(count_k)+".png")
        driver.switch_to.default_content()

        ele_iframe = driver.find_element_by_xpath('//*[@id="tranFrame"]')
        location = ele_iframe.location
        size = ele_iframe.size
        x_iframe = location['x'] #488
        y_iframe = location['y']  #234
        w_iframe = size['width']  #928
        h_iframe = size['height']  #2100
        height_iframe = y_iframe + h_iframe
        width_iframe = x_iframe + w_iframe

        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tranFrame"]'))

        ele_capcha = driver.find_element_by_xpath(xpath_capcha)
        location = ele_capcha.location
        size = ele_capcha.size
        
        x = location['x']  #397 +488
        y = location['y']  #226
        w = size['width']   #58 
        h = size['height']  #19 
        height = y + h
        width = x + w

        # crop img 
        im = Image.open(CurDir+"\\screen_shot\\" +str(count_k) +".png")
        im = im.crop((int(x + x_iframe), int(y), int(width + x_iframe), int(height))).convert("RGB")
        im.save(path_img+ "\\" + str(count_k)+".jpg")
        str_ocr = ocr_capcha.Get_Captcha1(CurDir, path_img+ "\\" + str(count_k)+".jpg")

    else:
        driver.save_screenshot(Curdir +"\\screen_shot\\" + str(count_k)+".png")
        ele_capcha = driver.find_element_by_xpath(xpath_capcha)
        location = ele_capcha.location
        size = ele_capcha.size
        
        x = location['x']  #397 +488
        y = location['y']  #226
        w = size['width']   #58 
        h = size['height']  #19 
        height = y + h
        width = x + w

        # crop img 
        im = Image.open(CurDir+"\\screen_shot\\" +str(count_k) +".png")
        im = im.crop((int(x), int(y), int(width), int(height))).convert("RGB")
        im.save(path_img+ "\\" + str(count_k)+".jpg")
        str_ocr = ocr_capcha.Get_Captcha1(CurDir, path_img+ "\\" + str(count_k)+".jpg")

    return str_ocr


def check_element(driver, xpath, int_Timeout=60):
    int_Count = 0
    while True:
        try:
            driver.find_element_by_xpath(xpath)
            return True
        except:
            if int_Count == int_Timeout:
                return False
            int_Count+=1
            time.sleep(1)

def select_xpath_options_khongdau(driver, xpath_select, xpath_options, input_option, timeout = 1):
    from unidecode import unidecode

    driver.find_element_by_xpath(xpath_select).click()
    time.sleep(timeout)
    for option_khongdau in driver.find_elements_by_xpath(xpath_options):
        if unidecode(input_option.lower().strip()) in unidecode(str(option_khongdau.text).lower().strip()) :
            option_khongdau.click()
            break


def select_xpath_options(driver, xpath_select, xpath_options, input_option, timeout = 1):

    driver.find_element_by_xpath(xpath_select).click()
    time.sleep(timeout)

    for i, j in enumerate(driver.find_elements_by_xpath(xpath_options)):
        # print(j.text)
        #  or str(j.text).strip() in input option
        if str(j.text).strip() == input_option:
            j.click()
            break

def login(driver, inputMST, str_password ,k):

    try:
        driver.get(url_links)
        while True:
            # user
            time.sleep(2)
            element_MST = driver.find_element_by_xpath('//*[@id="_userName"]')
            element_MST.click()
            element_MST.clear()
            element_MST.send_keys(str(inputMST))

            # element capcha
            xpath_capcha = '//*[@id="safecode"]'
            str_ocr = screen_capcha(driver, CurDir, xpath_capcha, k)

            # ocr capcha
            element_OCRcapcha = driver.find_element_by_xpath('//*[@id="capcha"]')
            element_OCRcapcha.click()
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                # driver.switch_to.default_content()
                alert = driver.switch_to_alert()
                if alert.text == "Mã số thuế không đúng, hãy nhập lại":
                    alert.accept()
                    LOG_INFO("MA SO THUE KHONG CHINH XAC, ID: "+inputMST)
                    return False
            except:
                element_OCRcapcha.send_keys(str_ocr)
                btn_login = driver.find_element_by_xpath('//*[@id="dangnhap"]')
                btn_login.click()
                time.sleep(2)

                # check error messgase captcha
                if check_element(driver, '//*[@id="loginForm"]/table/tbody/tr[4]/td/label', 5) == True:
                    # LOG_INFO(driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[4]/td/label').text)
                    driver.find_element_by_xpath('//*[@id="divCapcha"]/td/a').click()
                    time.sleep(2)
                else:
                    LOG_INFO("CAPTCHA IS CORRECT")
                    break

        while True:
            element_password = driver.find_element_by_xpath('//*[@id="_password"]')
            element_password.send_keys(str_password)
            btn_Dangnhap = driver.find_element_by_xpath('//*[@class="frm_login_content"]/form/table/tbody/tr[3]/td[2]/input')
            btn_Dangnhap.click()

            if check_element(driver,'//*[@class="frm_login_content"]/form/table/tbody/tr[5]/td', 5) == True:
                LOG_INFO("ID: " +inputMST+ " Mật khẩu không đúng, xin vui lòng thử lại !")
                time.sleep(2)
                return False
            else:
                LOG_INFO("DANG NHAP THANH CONG")
                return True
    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
        
    
def thu_tuc():

    LOG_INFO("BẮT ĐẦU QUY TRÌNH KÊ KHAI")

    try:
        list_Port = path_input()
        # ----- Duyet Folder Port -----
        for path_Port in list_Port:
            name_Port = path_Port.split("\\")[-2]
            path_company = glob.glob(os.path.abspath(path_Port+"\\*\\"))
            # print(name_Port)
            LOG_INFO("BAT DAU KE KHAI FOLDER_PORT: "+ name_Port)

            # ---- Duyet Folder Company -----
            for folder_company in path_company:

                folder_name = folder_company.split("\\")[-1]
                path_file = glob.glob(os.path.abspath(folder_company+"\\*.xlsx"))
                # print(folder_name)
                LOG_INFO("BAT DAU KE KHAI FOLDER_NAME: "+ folder_name)

                # ----- Duyet file .xlsx  -----
                for file in path_file:
                    file_name = file.split("\\")[-1].split(".xlsx")[0]
                    # print(file_name)

                    LOG_INFO("BAT DAU KE KHAI FILE_NAME: "+ file_name)
                    df_input_1 = pd.read_excel(file, engine="openpyxl", dtype= object)
                    for idx, row in df_input_1.iterrows():
                        df_input =  df_input_1.dropna(how='all')

                        if str(row).find("CT01") != -1:
                            continue
                        if str(row).find("Tình trạng") != -1:
                            continue
                        if len(str(row[0])) < 9:
                            continue
                        if str(row[0])== "NOTED:" or str(row).find("Giống MST") != -1 or str(row).find("Nếu có lỗi, nêu rõ thông tin lỗi") != -1 or str(row).find("Chỉ tiêu") != -1:
                            continue
                        if str(row).find("trên hệ thống tự động có") != -1:
                            continue

                        str_MST = df_input.iloc[idx,0]
                        str_Password = df_input.iloc[idx,1]
                        str_Status = df_input.iloc[idx,2]
                        str_Kykekhai = df_input.iloc[idx,3]
                        str_Nam =  df_input.iloc[idx,4]
                        str_Tuthang = df_input.iloc[idx,5]
                        str_Denthang =  df_input.iloc[idx,6]

                        driver = open_driver()  
                        if login(driver, str_MST,str_Password ,idx) == False:
                            LOG_INFO("MST: "+str_MST+ " DANG NHAP KHONG THANH CONG")
                            driver.close()
                            continue
                        # -------------------------------------------------------------------------------- 
                        
                        btn_Kekhaithue = driver.find_element_by_xpath('//*[@class="menu basictab"]/ul/li[3]/a')
                        btn_Kekhaithue.click()
                        time.sleep(1)

                        element_Thueluongcong = driver.find_element_by_xpath('//*[@class="submenuEpay"]/div/div[3]/ul/li[3]/a')
                        element_Thueluongcong.click()
                        time.sleep(1)

                        # move iframe Form khai thue tien luong cong
                        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tranFrame"]'))
                        
                        # Select to khai thue tien luong cong
                        element_Select_chontokhai= driver.find_element_by_xpath('//*[@id="mauTKhai"]')
                        element_Select_chontokhai.click()

                        element_Option_tokhai = driver.find_elements_by_xpath('//*[@id="mauTKhai"]/option')

                        for i, j in enumerate(element_Option_tokhai):
                            if "02/KK-TNCN" in (j.text).strip():
                                # driver.execute_script("arguments[0].click();", i)
                                j.click()
                                break

                        btn_Tieptuc = driver.find_element_by_xpath('//*[@id="declarationForm"]/div[2]/table/tbody/tr[2]/td[2]/input')
                        btn_Tieptuc.click()
                        
                        # Form Chọn thông tin tờ khai

                        element_Select_Loaitokhai = '//*[@id="loaiTKhai"]'
                        element_Option_Loaitokhai = '//*[@id="loaiTKhai"]/option'
                        select_xpath_options(driver, '//*[@id="loaiTKhai"]', '//*[@id="loaiTKhai"]/option', input_option='Tờ khai chính thức')

                        element_Select_Quykekhai = '//*[@id="quyKKhai"]'
                        element_Option_Quykekhai = '//*[@id="quyKKhai"]/option'
                        select_xpath_options(driver, '//*[@id="quyKKhai"]', '//*[@id="quyKKhai"]/option', input_option = str_Kykekhai)

                        element_Nam_kekhai = driver.find_element_by_xpath('//*[@id="namKKhaiQuy"]')
                        element_Nam_kekhai.click()
                        element_Nam_kekhai.clear()
                        try:
                            alert = Alert(driver)
                            LOG_INFO('ACCEPT: '+alert.text)  # accept Aler năm kê khai
                            alert.accept() 
                        except:
                            LOG_INFO("KHONG TIM THAY ALERT")

                        # năm kê khai
                        driver.execute_script("arguments[0].value=arguments[1];", element_Nam_kekhai, str_Nam)     
                        time.sleep(2)
                        try:
                            
                            ele_Tuthang =  WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tuThang"]')))
                            driver.execute_script("arguments[0].click();", ele_Tuthang)
                            time.sleep(2)
                            driver.execute_script("document.getElementById('tuThang').value = ''")
                            driver.execute_script("arguments[0].value=arguments[1];", ele_Tuthang, str_Tuthang)     

                        
                            ele_Denthang = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="denThang"]')))
                            driver.execute_script("arguments[0].click();", ele_Denthang)
                            time.sleep(3)
                            driver.execute_script("document.getElementById('denThang').value = ''")
                            driver.execute_script("arguments[0].value=arguments[1];", ele_Denthang, str_Denthang)     
    
                        except Exception as e:
                            LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
                            continue

                        btn_next_chonthongtintokhai = driver.find_element_by_xpath('//*[@id="submitBtn"]')
                        btn_next_chonthongtintokhai.click()
                        time.sleep(2)
                        
                        # Đã có tờ khai chính thức được chấp nhận. Bạn phải nộp tờ khai bổ sung.
                        ele_txError = '//*[@class="box_common_content"]/label'
                        if check_element(driver, ele_txError, int_Timeout=7) == True:

                            LOG_INFO("Đã có tờ khai chính thức được chấp nhận. Bạn phải nộp tờ khai bổ sung.")
                            LOG_INFO("MA SO THUE: "+ str(str_MST) +" "+ str(driver.find_element_by_xpath(ele_txError).text))
                            driver.close()
                            continue
                    
                        # Form input ke khai thue -----------------
                        check_kekhai = ke_khai(driver, row)
                        if check_kekhai == True: 

                            # Form file dinh kem
                            select_Phuluc = '//*[@id="uploadGiayToDKTForm"]/div/table/tbody/tr/td[2]/select[1]'
                            options_Phuluc = '//*[@id="uploadGiayToDKTForm"]/div/table/tbody/tr/td[2]/select/option'
                            select_xpath_options(driver, select_Phuluc, options_Phuluc, input_option="Các chứng từ khác")
                            time.sleep(3)

                            # Choose file
                            btn_insert_file = driver.find_element_by_xpath('//*[@id="uploadGiayToDKTForm"]/div/table/tbody/tr/td[3]/input[1]')
                            btn_insert_file.send_keys(path_File_import)
                            btn_Next = driver.find_element_by_xpath('//*[@id="uploadGiayToDKTForm"]/div/table[2]/tbody/tr/td/input[4]').click()
                            time.sleep(2)

                            # Pass captcha 2
                            while True:
                                
                                # element capcha
                                xpath_capcha = '//*[@id="safecode"]'
                                str_ocr = screen_capcha(driver, CurDir, xpath_capcha, idx, True)

                                element_captcha_2 = driver.find_element_by_xpath('//*[@id="nopTkhaiForm"]/table/tbody/tr[7]/td[2]/input[1]')
                                element_captcha_2.click()
                                element_captcha_2.send_keys(str_ocr)

                                btn_Next_xacthuctokhai = driver.find_element_by_xpath("//input[@id='submitCapc']")
                                btn_Next_xacthuctokhai.click()
                                time.sleep(3)
                                try:
                                    # check thong bao captcha trong
                                    
                                    alert = Alert(driver)
                                    LOG_INFO("ACCEPT: "+alert.text)
                                    alert.accept()
                                    # refresh captcha
                                    driver.find_element_by_xpath('//*[@id="nopTkhaiForm"]/table/tbody/tr[7]/td[2]/a[1]').click()
                                    time.sleep(2)
                    
                                except:
                                     # check thong bao sai captcha
                                    if check_element(driver, "/html[1]/body[1]/div[1]/div[2]/form[1]/table[1]/tbody[1]/tr[9]/td[2]", 5) == True:
                                        # refresh captcha
                                        # LOG_INFO(driver.find_element_by_xpath('//*[@id="nopTkhaiForm"]/table/tbody/tr[9]/td[2]').text)
                                        driver.find_element_by_xpath('//*[@id="nopTkhaiForm"]/table/tbody/tr[7]/td[2]/a[1]').click()
                                        time.sleep(2)
                                    else:
                                        LOG_INFO("CAPTCHA IS CORRECT")
                                        break
                            time.sleep(5)

                            # -----------OTP------
                            ele_OTP = '//*[@class="box_common_content"]/form/table/tbody/tr[4]/td[2]/input[1]'
                            btn_GuilaiOTP = '//*[@class="box_common_content"]/form/table/tbody/tr[4]/td[2]/input[2]'

                            response_opt = wait_OTP(driver, ele_OTP, btn_GuilaiOTP, name_Port)
                            if response_opt == False:
                                LOG_INFO("KHONG TIM THAY OTP")
                                driver.close()
                                continue

                            day_time = response_opt[0]
                            str_OTP = response_opt[1]
                        
                            btn_next_OTP = driver.find_element_by_xpath('//*[@class="box_common_content"]/form/table/tbody/tr[6]/td[2]/input[2]').click()
                            time.sleep(5)

                            #Form kê khai thành công
                            
                            if check_element(driver,'//*[@id="form_content"]/div[2]/table/tbody/tr[2]/td/h3[1]') == True:

                                ele_Noptokhaithanhcong = driver.find_element_by_xpath('//*[@id="form_content"]/div[2]/table/tbody/tr[2]/td/h3[1]')
                                LOG_INFO(ele_Noptokhaithanhcong.text)

                                btn_Next_Noptokhaithanhcong= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form_content"]/div[3]/input[1]')))
                                btn_Next_Noptokhaithanhcong.click()
                                time.sleep(3)

                        # ------ logout ----------------
                        driver.switch_to.default_content()

                        try:
                            btn_Dangxuat = driver.find_element_by_xpath('//*[@class="banner"]/div[3]/span[2]/strong/a').click()
                            
                            alert = Alert(driver)
                            LOG_INFO("ACCEPT: " +alert.text)
                            alert.accept()
                            time.sleep(3)
                        except NoAlertPresentException:
                            LOG_INFO("KHONG TIM THAY ALERT")

                        time.sleep(3)
                        # check
                        ele_Dangxuat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="dangnhap"]/span[2]/strong/a')))

                        if str(ele_Dangxuat.text).strip() == "Đăng nhập":
                            LOG_INFO("DANG XUAT THANH CONG")
                        driver.close()
                    LOG_INFO("HOAN THANH KE KHAI HO SO: "+ file_name)
                
                LOG_INFO("HOAN THANH KE KHAI FOLDER_NAME: " + folder_name)
                # move folder input
                shutil.move(folder_company,  path_Move_input+"\\"+name_Port)  

            LOG_INFO("HOAN THANH KE KHAI PORT_NAME: " + name_Port)  
        driver.quit()
    except Exception as e:     
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))


def ke_khai(driver, str_input):
    "From ke khai"
    try:
        str_MST = str_input[0]
        str_CT22 = str_input[9]
        str_CT23 = str_input[10]
        str_CT24 = str_input[11]
        str_CT25 = str_input[12]
        str_CT26 = str_input[13]
        str_CT27 = str_input[14]
        str_CT28 = str_input[15]
        str_CT29 = str_input[16]
        str_CT30 = str_input[17]
        str_CT31 = str_input[18]
        str_CT32 = str_input[19]
        str_CT33 = str_input[20]
        str_CT34 = str_input[21]
        str_CT35 = str_input[22]
        str_CT37 = str_input[24]

        machitieu_21 = False
        if machitieu_21 == True:
            checkbox_Machitieu_21 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[2]/td[4]/input')
            checkbox_Machitieu_21.click()

        
        input_Machitieu_22 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[3]/td[4]/input')
        input_Machitieu_22.click()
        input_Machitieu_22.clear()
        input_Machitieu_22.send_keys(str_CT22)
  
        
        input_Machitieu_23 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[4]/td[4]/input')
        input_Machitieu_23.click()
        input_Machitieu_23.clear()
        input_Machitieu_23.send_keys(str_CT23)

        ele_Machitieu_24 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[5]/td[4]/input[1]')
        if ele_Machitieu_24.get_property('value').strip().replace(".","") != str(str_CT24):
            # print(ele_Machitieu_24.get_property('value').strip().replace(".",""))
            # print(ele_Machitieu_24.get_attribute('value').strip().replace(".",""))

            LOG_INFO("MST: "+str_MST+ " Tổng giảm trừ - CT24 không đúng")
            return False
            
        ele_Machitieu_25 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[6]/td[4]/input[1]')
        if  ele_Machitieu_25.get_attribute('value').strip().replace(".","") != str(str_CT25):
            ele_Machitieu_25.click()
            ele_Machitieu_25.clear()
            ele_Machitieu_25.send_keys(str_CT25)

        input_Machitieu_26 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[7]/td[4]/input')
        input_Machitieu_26.click()
        input_Machitieu_26.clear()
        input_Machitieu_26.send_keys(str_CT26)

        
        input_Machitieu_27 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[8]/td[4]/input')
        input_Machitieu_27.click()
        input_Machitieu_27.clear()
        input_Machitieu_27.send_keys(str_CT27)

        
        input_Machitieu_28 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[9]/td[4]/input')
        input_Machitieu_28.click()
        input_Machitieu_28.clear()
        input_Machitieu_28.send_keys(str_CT28)

        
        input_Machitieu_29 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[10]/td[4]/input')
        input_Machitieu_29.click()
        input_Machitieu_29.clear()
        input_Machitieu_29.send_keys(str_CT29)

        # *-----
        ele_Machitieu_30 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[11]/td[4]/input[1]')
        if ele_Machitieu_30.get_attribute('value').strip().replace(".","") != str(str_CT30):

            # print(ele_Machitieu_30.get_attribute('value').strip().replace(".",""))
            LOG_INFO("MST: "+str_MST+" Tổng giảm trừ - CT30 không đúng")
            return False
            
        ele_Machitieu_31 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[12]/td[4]/input[1]')
        if ele_Machitieu_31.get_attribute('value').strip().replace(".","") != str(str_CT31):
            LOG_INFO("MST: "+str_MST+" Tổng giảm trừ - CT31 không đúng")
            return False


        ele_Machitieu_33 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[14]/td[4]/input[1]')
        if ele_Machitieu_33.get_attribute('value').strip().replace(".","") != str(str_CT33):
            LOG_INFO("MST: "+str_MST+" Tổng giảm trừ - CT33 không đúng")
            return False
        
        ele_Machitieu_34 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[15]/td[4]/input[1]')
        if ele_Machitieu_34.get_attribute('value').strip().replace(".","") != str(str_CT34):
       
            LOG_INFO("MST: "+str_MST+" Tổng giảm trừ - CT34 không đúng")
            return False

        
        input_Machitieu_35 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[17]/td[4]/input')
        input_Machitieu_35.click()
        input_Machitieu_35.clear()
        input_Machitieu_35.send_keys(str_CT35)

        # machitieu_36 = False
        # if machitieu_36 == True:
        #     input_Machitieu_36 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[18]/td[4]/input')
        #     input_Machitieu_36.click()
        #     input_Machitieu_36.clear()
        #     input_Machitieu_36.send_keys("")

        ele_Machitieu_37 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[19]/td[4]/input')
        if ele_Machitieu_37.get_attribute('value').strip().replace(".","") != str(str_CT37):
            
            LOG_INFO("MST: "+str_MST+" Tổng giảm trừ - CT37 không đúng")

            return False

        time.sleep(2)

        btn_Luubannhap = driver.find_element_by_xpath('//*[@id="bnhapBT"]').click()
        time.sleep(5)
        
        # Alert lưu bản nháp
        try:
            alert = Alert(driver)
            alert.text
            alert.accept()
            LOG_INFO("ACCEPT "+alert.text)
        except:
            LOG_INFO("KHONG TIM THAY ALERT")
        time.sleep(5)

        btn_Hoanthanhkekhai = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/form/div[2]/input[3]')))
        btn_Hoanthanhkekhai.click()
        time.sleep(5)

        btn_Noptokhai = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="btnNext" and @value="Nộp tờ khai"]')))
        btn_Noptokhai.click()
        time.sleep(5)
        
    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
        return False
    return True


def tracuu_Tokhai():
    "Form tra cuu to khai"

    LOG_INFO("BẮT ĐẦU QUY TRÌNH TRA CỨU")
    try:

        list_Port = path_move_input()
        # duyet sl ho so -----
        for path_Port in list_Port:
            name_Port = path_Port.split("\\")[-2]
            path_company = glob.glob(os.path.abspath(path_Port+"\\*\\"))
            # print(name_Port)
            LOG_INFO("BAT DAU TRA CUU FOLDER_PORT: "+ name_Port)

            # ---- Duyet Folder Company -----
            for folder_company in path_company:
                folder_name = folder_company.split("\\")[-1]
                path_file = glob.glob(os.path.abspath(folder_company+"\\*.xlsx"))
                # print(folder_name)
                LOG_INFO("BAT DAU TRA CUU FOLDER_NAME: "+ folder_name)

                # ----- Duyet file .xlsx  -----
                for file in path_file:
                    file_name = file.split("\\")[-1].split(".xlsx")[0]
                    # print(file_name)

                    writer = pd.ExcelWriter(path_Output+ '\\' +name_Port+"\\"+str(file_name)+ '_'+ datetime.datetime.now().strftime("%d%m%Y")+ '.xlsx')
                    df_input = pd.read_excel(file, engine="openpyxl", dtype= object)

                    df_output = df_input
                    for idx, row in df_input.iterrows():

                        df_input_1 =  df_input.dropna(how='all')
                        df_output = df_input_1

                        if str(row).find("CT01") != -1:
                            continue
                        if str(row).find("Tình trạng") != -1:
                            continue
                        if len(str(row[0])) < 9:
                            continue
                        if str(row[0])== "NOTED:" or str(row).find("Giống MST") != -1 or str(row).find("Nếu có lỗi, nêu rõ thông tin lỗi") != -1 or str(row).find("Chỉ tiêu") != -1:
                            continue
                        if str(row).find("trên hệ thống tự động có") != -1:
                            continue

                        str_MST = df_input_1.iloc[idx,0]
                        str_Password = df_input_1.iloc[idx,1]
                        str_Status = df_input_1.iloc[idx,2]
                        str_Kykekhai = df_input_1.iloc[idx,3]
                        str_Nam =  df_input_1.iloc[idx,4]

                        str_Tuthang = df_input_1.iloc[idx,5]
                        str_Denthang =  df_input_1.iloc[idx,6]

                        driver = open_driver()  
                        if login(driver, str_MST,str_Password ,idx) == False:
                            LOG_INFO("MST: "+str_MST+ " DANG NHAP KHONG THANH CONG")
                            driver.close()
                            continue

                        driver.switch_to.default_content()
                        btn_Kekhaithue = driver.find_element_by_xpath('//*[@class="menu basictab"]/ul/li[3]/a')
                        btn_Kekhaithue.click()
                        time.sleep(2)
                    
                        btn_Tracuutokhai = driver.find_element_by_xpath('//*[@class="submenuEpay"]/div/div[3]/ul/li[6]/a')
                        btn_Tracuutokhai.click()
                        time.sleep(2)
                        # -----
                        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tranFrame"]'))

                        select_Luachon_tracuutokhai = driver.find_element_by_xpath('//*[@class="form"]/form/table/tbody/tr[2]/td[2]/select')
                        list_options_tracuutokhai = driver.find_elements_by_xpath('//*[@class="form"]/form/table/tbody/tr[2]/td[2]/select/option')
                        input_Mahopdong = driver.find_element_by_xpath('//*[@class="form"]/form/table/tbody/tr[3]/td[2]/input[1]')

                        #  Sreach------------------------------------
                        input_Tungay = driver.find_element_by_xpath('//*[@class="form"]/form/table/tbody/tr[4]/td[2]/input[1]')
                        input_Tungay.click()
                        input_Tungay.clear()
                        input_Tungay.send_keys('01/'+str_Tuthang)

                        input_Denngay =  driver.find_element_by_xpath('//*[@class="form"]/form/table/tbody/tr[4]/td[2]/input[2]')

                        btn_Tracuu = driver.find_element_by_xpath('//*[@class="form"]/form/table/tbody/tr[5]/td/input[1]').click()
                        time.sleep(2)

                        # check nội dung
                        ele_Dieukientracuu = '//*[@id="khung_noidung"]/div[4]/b/i/span'
                        if check_element(driver, ele_Dieukientracuu, int_Timeout=5) == True:
                            LOG_INFO("LOG_ERROR: "+ driver.find_element_by_xpath(ele_Dieukientracuu))
                            driver.close()
                            continue

                        # ---- Form tra cuu

                        lst_Kytinhthue = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[3]')
                        lst_Ngaynop = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[8]')
                        lst_Trangthai = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[10]')

                        lst_Lannop = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[7]')
                        lst_Lydotuchoi = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[11]')
                        lst_Taive = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[15]/a')

                        str_Kytinhthue = str_Kykekhai +"/" + str(str_Nam)
                        # day_convert = convert_datetime_string(day_time.split(" ")[0])
                        for idx_Kytinhthue, j_Kytinhthue in enumerate(lst_Kytinhthue):
                            str_Ngaynop = str(lst_Ngaynop[idx_Kytinhthue].text).split(" ")[0].strip()

                            # lay KQ moi nhat
                            if j_Kytinhthue.text == str_Kytinhthue:
                                
                                df_output["Status"][idx] = lst_Trangthai[idx_Kytinhthue].text
                                df_output.to_excel(writer, index = False, engine='openpyxl')
                                # print(df_output)
                                LOG_INFO("DA UPDATE HO SO - ID: "+ str_MST + " "+ df_output["Status"][idx] )
                                # break
                        driver.switch_to.default_content()

                        try:
                            btn_Dangxuat = driver.find_element_by_xpath('//*[@class="banner"]/div[3]/span[2]/strong/a').click()
                            time.sleep(3)
                            alert =  Alert(driver)
                            LOG_INFO("ACCEPT: "+ alert.text)
                            alert.accept()
                            time.sleep(3)
                        except NoAlertPresentException:
                            LOG_INFO("KHONG TIM THAY ALERT")

                        time.sleep(3)
                        # check
                        ele_Dangxuat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="dangnhap"]/span[2]/strong/a')))
                        if str(ele_Dangxuat.text).strip() == "Đăng nhập":
                            LOG_INFO("DANG XUAT THANH CONG")
                        driver.close()
                        
                    LOG_INFO("HOAN THANH UPDATE TRANG THAI HO SO: "+ file_name)
                    writer.save()

                LOG_INFO("HOAN THANH TRA CUU FOLDER_NAME: " + folder_name) 
            
            LOG_INFO("HOAN THANH TRA CUU NAME_PORT: " + name_Port) 

        driver.quit()
    except Exception as e:      
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))

def wait_OTP(driver, xpath_InputOPT, xpath_SendOPT, name_Port ,timeout = 60):
    import main_API
    ip_config = data_config["ip_otp"]
    x = 1
    count_timeout = 3
    while True:
        day_times ,str_OTP = main_API.api_otp(ip_config, name_Port)

        if str_OTP != "":
            driver.find_element_by_xpath(xpath_InputOPT).send_keys(str_OTP)
            return day_times, str_OTP, True

        elif x == timeout:
            # Refresh OPT
            driver.find_element_by_xpath(xpath_SendOPT).click()
            x = 0
            count_timeout +=1
            time.sleep(5)
        x+=1

        if count_timeout == 3:
            return False


if __name__ == "__main__":
    import datetime
    import schedule
    import time
 
    LOG_INFO("BẮT ĐẦU CHẠY")
    # thu_tuc()
    # tracuu_Tokhai()
    if data_config['lien_tuc'] == True:
        while True:
            thu_tuc()
            tracuu_Tokhai()
    else:
        schedule.every().day.at(data_config['che_do_ke_khai']['thoi_gian_co_dinh']).do(thu_tuc)
        schedule.every().day.at(data_config['che_do_quet_ket_qua']['thoi_gian_co_dinh']).do(tracuu_Tokhai)

    while True:
        schedule.run_pending()
        time.sleep(1)
