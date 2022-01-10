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
import threading

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
global LOG_ERROR
name_Organization = "vpo"
name_Robot = "P.I.T"
name_Version = "1.1.6"
name_Config = "config_pj-vpo_robot.json"
name_Logs = "logs_pj-vpo_robot.txt"
name_Config_port = "config_pj-vpo_port-name.json"

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
data_config_port = readJson(CurDir+"\\conf\\"+name_Config_port)


path_Input = data_config["thu_muc_input"]
path_Move_input = data_config["thu_muc_move_input"]
path_Output = data_config["thu_muc_output"]
path_File_import = data_config["thu_muc_import"]
path_Download = data_config["thu_muc_download"]
path_Backup = data_config["thu_muc_backup"]


# email cấu hình gửi
id_email_gui =data_config["id_email_gui"]
pass_email_gui =data_config["pass_email_gui"]

# email tb hoàn thành quy trình
email_nhan = data_config["email_nhan"]

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
    path_folder_input = glob.glob(os.path.abspath(path_Input) + "\\*.xlsx")
    # print(path_folder_input)
    return path_folder_input

def path_move_input():
    path_folder_move_input = glob.glob(os.path.abspath(path_Move_input) + "\\*.xlsx")
    
    return path_folder_move_input

def convert_datetime_string(data_input,format_input='%Y-%m-%d',format_output='%d/%m/%Y'):
    import datetime
    data_date = datetime.datetime.strptime(data_input, format_input)
    data_date = data_date.strftime(format_output)
    return data_date

class thread_with_trace(threading.Thread): 
    def __init__(self, *args, **keywords): 
        threading.Thread.__init__(self, *args, **keywords) 
        self.killed = False
    
    def start(self): 
        self.__run_backup = self.run 
        self.run = self.__run       
        threading.Thread.start(self) 
    
    def __run(self): 
        sys.settrace(self.globaltrace) 
        self.__run_backup() 
        self.run = self.__run_backup 
    
    def globaltrace(self, frame, event, arg): 
        if event == 'call': 
            return self.localtrace 
        else: 
            return None
    
    def localtrace(self, frame, event, arg): 
        if self.killed: 
            if event == 'line': 
                raise SystemExit() 
        return self.localtrace 
    
    def kill(self): 
        self.killed = True

def open_driver():

    options = Options()
    prefs = {"credentials_enable_service": False,  
    "profile.password_manager_enabled": False ,  # tắt arlert save password chrome
    "profile.default_content_settings.popups": 0,
    "download.default_directory": path_Download, # IMPORTANT - ENDING SLASH V IMPORTANT
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True}
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--safebrowsing-disable-download-protection')
    options.add_argument("--no-sandbox") 
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--disable-web-security")
    options.add_experimental_option("excludeSwitches", ["enable-automation",'enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument('ignore-certificate-errors') ## fixx ssl
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    # options.add_argument("--allow-running-insecure-content")

    driver = webdriver.Chrome(executable_path= path_chrome, chrome_options=options)

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

def select_xpath_submenu(driver, xpath_submenu, input_option, timeout=60):

    for i, j in enumerate(driver.find_elements_by_xpath(xpath_submenu)):
        if str(j.text).strip() == input_option:
            j.click()
            break


def login(driver, inputMST, str_password ,k):

    try:
        driver.get(url_links)
        time.sleep(3)
        # Login 1
        while True:
            try:
                # user
                element_MST= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="_userName"]')))
                # element_MST = driver.find_element_by_xpath('//*[@id="_userName"]')
                element_MST.click()
                element_MST.clear()
                element_MST.send_keys(str(inputMST))
                time.sleep(1)

                element_OCRcapcha = driver.find_element_by_xpath('//*[@id="capcha"]')
                element_OCRcapcha.click()
                time.sleep(1)

                
                alert = Alert(driver)
                time.sleep(1)
                if str(alert.text).find("Mã số thuế không đúng, hãy nhập lại") != -1:
                    LOG_INFO(alert.text)
                    time.sleep(2)
                    alert.accept()
                    LOG_INFO("MA SO THUE KHONG CHINH XAC, ID: "+inputMST)
                    return False
            except:
                pass
            time.sleep(2)
            
            # element capcha
            xpath_capcha = '//*[@id="safecode"]'
            str_ocr = screen_capcha(driver, CurDir, xpath_capcha, k)

            # ocr capcha
            element_OCRcapcha = driver.find_element_by_xpath('//*[@id="capcha"]')
            element_OCRcapcha.click()
            time.sleep(1)

            if len(str_ocr) == 4:
                element_OCRcapcha.send_keys(str_ocr)
            else:
                # refresh captcha
                driver.find_element_by_xpath('//*[@id="divCapcha"]/td/a').click()
                time.sleep(1)
                continue

            btn_login = driver.find_element_by_xpath('//*[@id="dangnhap"]')
            btn_login.click()
            time.sleep(2)

            # check error messgase captcha
            if check_element(driver, '//*[@id="loginForm"]/table/tbody/tr[4]/td/label', 5) == True:
                
                # refresh captcha
                driver.find_element_by_xpath('//*[@id="divCapcha"]/td/a/img').click()
                time.sleep(1)
            else:
                LOG_INFO("CAPTCHA IS CORRECT")
                break
        
        # Login 2
        while True:
            element_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="_password"]')))

            # element_password = driver.find_element_by_xpath('//*[@id="_password"]')
            element_password.click()
            element_password.send_keys(str_password)
            time.sleep(1)
            
            btn_Dangnhap = driver.find_element_by_xpath('//*[@class="frm_login_content"]/form/table/tbody/tr[3]/td[2]/input')
            btn_Dangnhap.click()
            time.sleep(2)
            if check_element(driver,'//*[@class="frm_login_content"]/form/table/tbody/tr[5]/td', 5) == True:
                LOG_INFO("ID: " +inputMST+ " Mật khẩu không đúng, xin vui lòng thử lại !")
                time.sleep(1)
                return False
            else:
                LOG_INFO("DANG NHAP THANH CONG")
                return True
    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
        return False

#---
flag = False

def start_record(path_record, name_record):
    import pyautogui
    import cv2
    import numpy as np
    
    # Specify resolution
    resolution = (1920, 1080)
    
    # Specify video codec
    codec = cv2.VideoWriter_fourcc(*"XVID")
    
    # Specify name of Output file
    day_time = datetime.datetime.now()
    day_time = day_time.strftime('%Y%m%d')
    filename = path_record+"/"+day_time+'_'+name_record+".avi"
    
    # Specify frames rate. We can choose any 
    # value and experiment with it
    fps = 25.0
    
    # Creating a VideoWriter object
    out = cv2.VideoWriter(filename, codec, fps, resolution)
    
    # Create an Empty window
    # cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    
    # Resize this window
    # cv2.resizeWindow("Live", 480, 270)
    
    while True:
        # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()
    
        # Convert the screenshot to a numpy array
        frame = np.array(img)
    
        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # Write it to the output file
        out.write(frame)
        
        # Optional: Display the recording screen
        # cv2.imshow('Live', frame)
        
        # Stop recording when we press 'q'
        
        # if cv2.waitKey(1) == ord('q'):
        if flag ==True:
            break
    
    # Release the Video writer
    out.release()
    
    # Destroy all windows
    cv2.destroyAllWindows()

def save_record():
    global flag
    flag=True
    print("stop record")
    return flag

def run(path, name_record):
    name_record = name_record.split(".xlsx")[0]
    try:
        th=threading.Thread(target=start_record,args=(path, name_record))
        th.start()
    except:
        print('loi 437')

def thu_tuc():

    LOG_INFO("BẮT ĐẦU QUY TRÌNH KÊ KHAI")

    try:
        list_Input = path_input()
          
        if len(list_Input) >= 1:
            # ----- Duyet file .xlsx  -----
            for file_input in list_Input:

                if str(file_input).find("~$") != -1:
                    continue

                file_name = str(file_input).split("\\")[-1]
                run(path=path_Backup+"/save_record/ke_khai",name_record=file_name)
             
                LOG_INFO("BAT DAU KE KHAI FILE_NAME: "+ file_name)

                df_input_1 = pd.read_excel(file_input, engine="openpyxl", dtype= object)
                df_input =  df_input_1.dropna(how='all')
                time.sleep(2)
                
                # File backup
                backup_File(file_input, path_Backup, file_name)
                LOG_INFO("BACKUP FILE: "+file_name)
                time.sleep(2)

                #  Check nếu file đang mở, move_file trả về False, del file coppy
                if move_file(file_input, path_Move_input, file_name) == False:
                    os.remove(path_Move_input+"\\"+file_name)
                    time.sleep(3)
                    continue

                lst_except = []

                for idx, row in df_input.iterrows():
                    try:

                        str_MST = str(df_input.iloc[idx,0]).strip()
                        str_Password = str(df_input.iloc[idx,1]).strip()
                        str_Phone_number = str(df_input.iloc[idx,2]).strip()
                        str_Email = str(df_input.iloc[idx,3]).strip()
                        str_Status = str(df_input.iloc[idx,4]).strip()
                        str_Tokhaidanop = str(df_input.iloc[idx,5]).strip()
                        str_Thongbao_Cucthue = str(df_input.iloc[idx,6]).strip()
                        str_Kykekhai = str(df_input.iloc[idx,7]).strip()
                        str_Nam =  str(df_input.iloc[idx,8]).strip()
                        str_Tuthang = str(df_input.iloc[idx,9]).strip()
                        str_Denthang =  str(df_input.iloc[idx,10]).strip()

                        if str(row).find("CT01") != -1:
                            continue

                        if str(row).find("Tình trạng") != -1:
                            continue

                        if str_MST == "nan" or str_MST == "":
                            lst_except.append(idx)
                            time.sleep(1)
                            LOG_INFO("MA SO THUE TRONG")
                            send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" mã số thuế trống. Vui lòng kiểm tra!", to_email=str_Email)
                            time.sleep(1)
                            continue
                        

                        if str_Password == "nan" or str_Password == "":
                            lst_except.append(idx)
                            time.sleep(1)
                            LOG_INFO("MA SO THUE - ID: "+str_MST+ " PASSWORD KHONG DUOC DE TRONG")
                            send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" "+str_MST+" mật khẩu trống. Vui lòng kiểm tra!", to_email=str_Email)
                            time.sleep(1)
                            continue
                        
                        if str(row[0])== "NOTED:" or str(row).find("Giống MST") != -1 or str(row).find("Nếu có lỗi, nêu rõ thông tin lỗi") != -1 or str(row).find("Chỉ tiêu") != -1:
                            continue

                        if str(row).find("trên hệ thống tự động có") != -1:
                            continue
                        
                        driver = open_driver()
                      
                        if login(driver, str_MST,str_Password ,idx) == False:
                            lst_except.append(idx)
                            time.sleep(1)
                            LOG_INFO("MST: "+str_MST+ " DANG NHAP KHONG THANH CONG")
                            send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" MST "+str_MST+" mã số thuế hoặc mật khẩu không đúng. Vui lòng kiểm tra!", to_email=str_Email)
                            time.sleep(1)
                            driver.quit()
                            continue
                        time.sleep(2)

                        # -------------------------------------------------------------------------------- 
                        # Check screen "Màn hình đang đăng nhập"
                        if check_element(driver, '//*[@class="succeed_table_content"]/table/tbody/tr/td/input',5) == True:
                            driver.find_element_by_xpath('//*[@class="succeed_table_content"]/table/tbody/tr/td/input').click()
                            time.sleep(1)
                        btn_Kekhaithue = driver.find_element_by_xpath('//*[@class="menu basictab"]/ul/li[3]/a')
                        btn_Kekhaithue.click()
                        time.sleep(2)

                        element_Thueluongcong = '//*[@class="submenuEpay"]/div/div[3]/ul/li/a'
                        select_xpath_submenu(driver, element_Thueluongcong, input_option="Khai thuế tiền lương tiền công")
                        time.sleep(2)
                        

                        # move iframe Form khai thue tien luong cong
                        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tranFrame"]'))
                        
                        # Select to khai thue tien luong cong
                        element_Select_chontokhai= driver.find_element_by_xpath('//*[@id="mauTKhai"]')
                        element_Select_chontokhai.click()
                        time.sleep(2)

                        element_Option_tokhai = driver.find_elements_by_xpath('//*[@id="mauTKhai"]/option')

                        for i, j in enumerate(element_Option_tokhai):
                            if "02/KK-TNCN" in (j.text).strip():
                                # driver.execute_script("arguments[0].click();", i)
                                j.click()
                                break
                        time.sleep(2)
                        
                        btn_Tieptuc = driver.find_element_by_xpath('//*[@id="declarationForm"]/div[2]/table/tbody/tr[2]/td[2]/input')
                        btn_Tieptuc.click()
                        time.sleep(2)
                        
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
                            time.sleep(2) 
                            alert = Alert(driver)
                            LOG_INFO('ACCEPT: '+alert.text)  # accept Aler năm kê khai
                            alert.accept() 
                        except:
                            LOG_INFO("KHONG TIM THAY ALERT")

                        
                        if len(str_Nam) == 4:
                            # năm kê khai
                            driver.execute_script("arguments[0].value=arguments[1];", element_Nam_kekhai, str_Nam)     
                            time.sleep(2) 
                        else:
                            lst_except.append(idx)
                            LOG_INFO("NAM KE KHAI KHONG CHINH XAC")
                            send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" "+str_MST+" năm kê khai không chính xác. Vui lòng kiểm tra!", to_email=str_Email)
                            time.sleep(1)

                            driver.quit()
                            continue
                   
                        try:
                            # ele_Tuthang =  WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="tuThang"]')))
                            # driver.execute_script("arguments[0].click();", ele_Tuthang)
                            # time.sleep(1)
                            # driver.execute_script("document.getElementById('tuThang').value = ''")
                            # time.sleep(1)
                            # driver.execute_script("arguments[0].value=arguments[1];", ele_Tuthang, str_Tuthang)     
                            # time.sleep(1)
                            # actions = ActionChains(driver)
                            ele_tuthang = driver.find_element_by_xpath('//*[@id="tuThang"]')
                            ele_tuthang.click()
                            ele_tuthang.send_keys(Keys.CONTROL+"a")
                            ele_tuthang.send_keys(Keys.BACKSPACE)
                            ele_tuthang.send_keys(str_Tuthang)
                            time.sleep(1)

                            ele_Denthang = driver.find_element_by_xpath('//*[@id="denThang"]')
                            ele_Denthang.click()
                            ele_Denthang.send_keys(Keys.CONTROL+"a")
                            ele_Denthang.send_keys(Keys.BACKSPACE)
                            ele_Denthang.send_keys(str_Denthang)
                    
                            # driver.execute_script("arguments[0].click();", ele_Denthang)
                            # time.sleep(1)
                            # driver.execute_script("document.getElementById('denThang').value = ''")
                            # time.sleep(1)
                            # driver.execute_script("arguments[0].value=arguments[1];", ele_Denthang, str_Denthang)    
                            #  
                
                        except Exception as e:
                            lst_except.append(idx)

                            LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
                            continue

                        time.sleep(1)
                        btn_next_chonthongtintokhai = driver.find_element_by_xpath('//*[@id="submitBtn" and @class="inputBtn awesome"]')
                        btn_next_chonthongtintokhai.click()
                        time.sleep(2)
                        
                        # Check screen "Đã có tờ khai chính thức được chấp nhận. Bạn phải nộp tờ khai bổ sung."
                        ele_txError = '//*[@class="box_common_content"]/label'
                        if check_element(driver, ele_txError, int_Timeout=7) == True:
                            
                            LOG_INFO("Đã có tờ khai chính thức được chấp nhận. Bạn phải nộp tờ khai bổ sung.")
                            LOG_INFO("MA SO THUE: "+ str(str_MST) +" "+ str(driver.find_element_by_xpath(ele_txError).text))
                            send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" "+str_MST+" đã được kê khai trước đó. Vui lòng kiểm tra!", to_email=str_Email)
                            time.sleep(1)

                            driver.quit()
                            continue
                    
                        # Form input ke khai thue -----------------
                        check_kekhai = ke_khai(driver, row)
                        time.sleep(1)

                        if check_kekhai == True: 

                            # Form file dinh kem
                            select_Phuluc = '//*[@id="uploadGiayToDKTForm"]/div/table/tbody/tr/td[2]/select[1]'
                            options_Phuluc = '//*[@id="uploadGiayToDKTForm"]/div/table/tbody/tr/td[2]/select/option'
                            select_xpath_options(driver, select_Phuluc, options_Phuluc, input_option="Các chứng từ khác", timeout=5)
                            time.sleep(3)
                            try:
                                # Choose file
                                btn_insert_file = driver.find_element_by_xpath('//*[@id="uploadGiayToDKTForm"]/div/table/tbody/tr/td[3]/input[1]')
                                btn_insert_file.send_keys(path_File_import)
                                time.sleep(1)
                                btn_Next = driver.find_element_by_xpath('//*[@id="uploadGiayToDKTForm"]/div/table[2]/tbody/tr/td/input[4]')
                                btn_Next.click()
                                time.sleep(2)

                            except:
                                LOG_INFO("KHONG TIM THAY FILE .PDF DINH KEM, VUI LONG KIEM TRA")
                                send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" "+str_MST+" không tìm thấy file .pdf đính kèm. Vui lòng kiểm tra!", to_email=str_Email)
                                time.sleep(1)
                                driver.quit()
                                continue
                            
                            if check_element(driver,'//*[@id="safecode"]',5) == True:
                                # Pass captcha 2
                                while True:
                                    
                                    # element capcha
                                    xpath_capcha = '//*[@id="safecode"]'
                                    str_ocr = screen_capcha(driver, CurDir, xpath_capcha, idx, True)
                                    time.sleep(1)
                                    
                                    element_captcha_2 = driver.find_element_by_xpath('//*[@id="nopTkhaiForm"]/table/tbody/tr[7]/td[2]/input[1]')
                                    element_captcha_2.click()
                                    time.sleep(1)

                                    if len(str_ocr) == 4:
                                        element_captcha_2.send_keys(str_ocr)
                                    else:
                                        driver.find_element_by_xpath('//*[@id="nopTkhaiForm"]/table/tbody/tr[7]/td[2]/a[1]').click()
                                        time.sleep(1)
                                        continue

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
                                            driver.find_element_by_xpath('//*[@id="nopTkhaiForm"]/table/tbody/tr[7]/td[2]/a[1]').click()
                                            time.sleep(2)
                                        else:
                                            LOG_INFO("CAPTCHA IS CORRECT")
                                            break
                                time.sleep(5)

                                # -----------OTP------
                                ele_OTP = '//*[@class="box_common_content"]/form/table/tbody/tr[4]/td[2]/input[1]'
                                btn_GuilaiOTP = '//*[@class="box_common_content"]/form/table/tbody/tr[4]/td[2]/input[2]'

                                # update them ko trung SDT -> continue
                                name_Port = ""
                                for port, str_sdt in data_config_port.items():
                                    if str_sdt == str_Phone_number:
                                        name_Port = str(port)
                                        break
                                time.sleep(1)

                                if name_Port == "":
                                    LOG_INFO("Port không khớp. Vui lòng kiểm tra lại ! ")
                                    send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" "+str_MST+" số điện thoại không khớp với tổng đài. Vui lòng kiểm tra!", to_email=str_Email)
                                    driver.quit()
                                    continue
                                else:
                                    response_opt = wait_OTP(driver, ele_OTP, btn_GuilaiOTP, name_Port)
                                    day_time = response_opt[0]
                                    str_OTP = response_opt[1]
                                    bl_check = response_opt[2]
                                time.sleep(1)

                                if data_config["chay_test"] == False:
                                    time.sleep(3)
                                    if bl_check == False:
                                        LOG_INFO("KHONG TIM THAY OTP")
                                        send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" "+str_MST+" không tìm thấy OTP. Vui lòng kiểm tra!", to_email=str_Email)
                                        time.sleep(1)
                                        driver.quit()
                                        continue
                                
                                    btn_next_OTP = driver.find_element_by_xpath('//*[@class="box_common_content"]/form/table/tbody/tr[6]/td[2]/input[2]').click()
                                    time.sleep(3)
                                    
                                    if check_element(driver, '//*[@class="box_common_content"]/form/table//tr[7]/td[2]',5) == True:
                                        send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" "+str_MST+" không tìm thấy OTP. Vui lòng kiểm tra!", to_email=str_Email)
                                        time.sleep(1)
                                        driver.quit()
                                        continue
                                    
                                    #Form kê khai thành công
                                    if check_element(driver,'//*[@id="form_content"]/div[2]/table/tbody/tr[2]/td/h3[1]') == True:

                                        ele_Noptokhaithanhcong = driver.find_element_by_xpath('//*[@id="form_content"]/div[2]/table/tbody/tr[2]/td/h3[1]')
                                        LOG_INFO(ele_Noptokhaithanhcong.text)

                                        btn_Next_Noptokhaithanhcong= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form_content"]/div[3]/input[1]')))
                                        btn_Next_Noptokhaithanhcong.click()
                                        time.sleep(3)
                                else:
                                    # ------
                                    time.sleep(7)

                            else:

                                lst_except.append(idx)
                                LOG_INFO('Captcha 2 có lỗi')
                                send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" MST "+str_MST+" page captcha có lỗi. Vui lòng kiểm tra!", to_email=str_Email)
                                time.sleep(1)
                                driver.quit()
                                continue

                        else:        
                            lst_except.append(idx)
                            LOG_INFO("FORM KE KHAI CO LOI")
                            send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" MST "+str_MST+" thông tin kê khai có lỗi. Vui lòng kiểm tra!", to_email=str_Email)
                            time.sleep(1)
                            driver.quit()
                            continue

                            
                        if data_config["chay_test"] == False:
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

                            # check logout
                            ele_Dangxuat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="dangnhap"]/span[2]/strong/a')))
                            if str(ele_Dangxuat.text).strip() == "Đăng nhập":
                                LOG_INFO("DANG XUAT THANH CONG")
                            driver.quit()
                        else:
                            LOG_INFO("HOAN THANH CHAY THU")
                            driver.quit()
                    except Exception as e:
                        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))

                # Check row error df_input
                if len(lst_except) != 0:
                    check_df_input(file_name, lst_except)
                    time.sleep(1)
                    lst_except = []
                LOG_INFO("HOAN THANH KE KHAI HO SO: "+ file_name)
                save_record()
        else:
            LOG_INFO("KHONG CO HO SO KE KHAI")
            
    except Exception as e:     
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
        save_record()


def check_df_input(file_name, lst_except):
    "Check lại Data file input"

    df_check = pd.read_excel(path_Move_input+"\\"+file_name, engine="openpyxl", dtype= object)
          
    for idx, i in enumerate(lst_except):
        df_check["Status"][i] = "Thông tin bị lỗi"
        time.sleep(1)

    writer = pd.ExcelWriter(path_Move_input+"\\"+str(file_name))
    df_check.to_excel(writer, index = False, engine='openpyxl')
    writer.save()
    time.sleep(2)
    writer.close()


# ------------------------------
def backup_File(file_input, path_Backup, file_name):
    "Coppy file input"
    import datetime
    x = datetime.datetime.now()
    date_time = x.strftime("%Y-%m-%d")

    try:
        if not os.path.exists(path_Backup+"\\"):
            os.makedirs(path_Backup+"\\")

        shutil.copy2(file_input, path_Backup+"\\"+date_time+"_"+file_name)
    except Exception as e :
        shutil.copy2(file_input, path_Backup+"\\"+date_time+"_"+file_name)
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))

def move_file(file_input, path_Move_input, file_name):

    try:
        if not os.path.exists(path_Move_input+"\\"):
            os.makedirs(path_Move_input+"\\")

        shutil.move(file_input, path_Move_input+"\\" + file_name)
        return True
    except Exception as e :
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
        return False


def ke_khai(driver, str_input):
    "From ke khai"
    try:
        str_MST = str(str_input[0]).strip()
        str_Phone_number = str(str_input[2]).strip()
        str_CT22 = str(str_input[13]).strip()
        str_CT23 = str(str_input[14]).strip()
        str_CT24 = str(str_input[15]).strip()
        str_CT25 = str(str_input[16]).strip()
        str_CT26 = str(str_input[17]).strip()
        str_CT27 = str(str_input[18]).strip()
        str_CT28 = str(str_input[19]).strip()
        str_CT29 = str(str_input[20]).strip()
        str_CT30 = str(str_input[21]).strip()
        str_CT31 = str(str_input[22]).strip()
        str_CT32 = str(str_input[23]).strip()
        str_CT33 = str(str_input[24]).strip()
        str_CT34 = str(str_input[25]).strip()
        str_CT35 = str(str_input[26]).strip()
        str_CT37 = str(str_input[28]).strip()

        #     checkbox_Machitieu_21 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[2]/td[4]/input')
        #     checkbox_Machitieu_21.click()

        input_Machitieu_22 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[3]/td[4]/input')
        input_Machitieu_22.click()
        input_Machitieu_22.clear()
        input_Machitieu_22.send_keys(str_CT22)
        time.sleep(1)     
        
        input_Machitieu_23 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[4]/td[4]/input')
        input_Machitieu_23.click()
        input_Machitieu_23.clear()
        input_Machitieu_23.send_keys(str_CT23)
        time.sleep(1)     

        # ele_Machitieu_24 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[5]/td[4]/input[1]')
            
        ele_Machitieu_25 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[6]/td[4]/input[1]')
        ele_Machitieu_25.click()
        ele_Machitieu_25.clear()
        ele_Machitieu_25.send_keys(str_CT25)
        time.sleep(1)     

        input_Machitieu_26 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[7]/td[4]/input')
        input_Machitieu_26.click()
        input_Machitieu_26.clear()
        input_Machitieu_26.send_keys(str_CT26)
        time.sleep(1)     

        
        input_Machitieu_27 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[8]/td[4]/input')
        input_Machitieu_27.click()
        input_Machitieu_27.clear()
        input_Machitieu_27.send_keys(str_CT27)
        time.sleep(1)     

        
        input_Machitieu_28 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[9]/td[4]/input')
        input_Machitieu_28.click()
        input_Machitieu_28.clear()
        input_Machitieu_28.send_keys(str_CT28)
        time.sleep(1)     

        
        input_Machitieu_29 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[10]/td[4]/input')
        input_Machitieu_29.click()
        input_Machitieu_29.clear()
        input_Machitieu_29.send_keys(str_CT29)
        time.sleep(1)     

        # *-----
        # ele_Machitieu_30 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[11]/td[4]/input[1]')
     
        # ele_Machitieu_31 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[12]/td[4]/input[1]')

        # ele_Machitieu_33 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[14]/td[4]/input[1]')
       
        # ele_Machitieu_34 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[15]/td[4]/input[1]')
      
        input_Machitieu_35 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[17]/td[4]/input')
        input_Machitieu_35.click()
        input_Machitieu_35.clear()
        input_Machitieu_35.send_keys(str_CT35)
        time.sleep(1)
        #  input_Machitieu_36 = driver.find_element_by_xpath('//*[@class="tbl_member"]/table/tbody/tr[18]/td[4]/input')
        
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
        time.sleep(1)
        return False
    return True

def tracuu_Tokhai():
    "Form tra cuu to khai"

    LOG_INFO("BẮT ĐẦU QUY TRÌNH TRA CỨU")
    try:
        list_Move_input = path_move_input()
    
        # ----- Duyet file .xlsx  -----
        for file_Move in list_Move_input:

            file_name = str(file_Move).split("\\")[-1]
            run(path=path_Backup+"/save_record/tra_cuu",name_record=file_name)

            LOG_INFO("BAT DAU TRA CUU HO SO: " + file_name)
    
            df_input = pd.read_excel(file_Move, engine="openpyxl", dtype= object)
            df_input =  df_input.dropna(how='all')
            # print(df_input)
            df_input.astype(str)
            if check_df(df_input) == False:
                # print(df_input)
                for idx, row in df_input.iterrows():
                    try:
                        str_MST = str(df_input.iloc[idx,0]).strip()
                        str_Password = str(df_input.iloc[idx,1]).strip()
                        str_Phone_number = str(df_input.iloc[idx,2]).strip()
                        str_Email = str(df_input.iloc[idx,3]).strip()
                        str_Status = str(df_input.iloc[idx,4]).strip()
                        str_Tokhaidanop = str(df_input.iloc[idx,5]).strip()
                        str_Thongbao_Cucthue = str(df_input.iloc[idx,6]).strip()
                        str_Kykekhai = str(df_input.iloc[idx,7]).strip()
                        str_Nam =  str(df_input.iloc[idx,8]).strip()
                        str_Tuthang = str(df_input.iloc[idx,9]).strip()
                        str_Denthang =  str(df_input.iloc[idx,10]).strip()

                        if str(row).find("CT01") != -1:
                            continue
                        if str(row).find("Tình trạng") != -1:
                            continue
                        if str(df_input["Status"][idx]).lower() != "nan" and str(df_input["Status"][idx]).lower() != "":
                            # print(str(df_input["Status"][idx]).lower())
                            continue  
                        
                        driver = open_driver()  
                     
                        if login(driver, str_MST,str_Password ,idx) == False:
                            LOG_INFO("MST: "+str_MST+ " DANG NHAP KHONG THANH CONG")
                            driver.quit()
                            continue
                        time.sleep(2)
                        
                        driver.switch_to.default_content()
                        # Check 
                        if check_element(driver, '//*[@class="succeed_table_content"]/table/tbody/tr/td/input',5) == True:
                            driver.find_element_by_xpath('//*[@class="succeed_table_content"]/table/tbody/tr/td/input').click()

                        btn_Kekhaithue = driver.find_element_by_xpath('//*[@class="menu basictab"]/ul/li[3]/a')
                        btn_Kekhaithue.click()
                        time.sleep(2)
                    
                        btn_Tracuutokhai = '//*[@class="submenuEpay"]/div/div[3]/ul/li/a'
                        select_xpath_submenu(driver, btn_Tracuutokhai, input_option="Tra cứu tờ khai")
                        time.sleep(2)

                        # --------- Form tra cuu --------
                        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tranFrame"]'))

                        select_Luachon_tracuutokhai = '//*[@class="form"]/form/table/tbody/tr[2]/td[2]/select'
                        list_options_tracuutokhai = '//*[@class="form"]/form/table/tbody/tr[2]/td[2]/select/option'
                        select_xpath_options_khongdau(driver, select_Luachon_tracuutokhai, list_options_tracuutokhai, input_option='02/KK-TNCN')

                        input_Mahopdong = driver.find_element_by_xpath('//*[@class="form"]/form/table/tbody/tr[3]/td[2]/input[1]')

                        #  Sreach------------------------------------
                        input_Tungay = driver.find_element_by_xpath('//*[@class="form"]/form/table/tbody/tr[4]/td[2]/input[1]')
                        input_Tungay.click()
                        input_Tungay.clear()
                        input_Tungay.send_keys('01/'+str_Tuthang)

                        input_Denngay =  driver.find_element_by_xpath('//*[@class="form"]/form/table/tbody/tr[4]/td[2]/input[2]')
                        # input_Denngay.click()
                        # input_Denngay.clear()
                        # input_Denngay.send_keys('30/'+str_Denthang)

                        btn_Tracuu = driver.find_element_by_xpath('//*[@class="form"]/form/table/tbody/tr[5]/td/input[1]').click()
                        time.sleep(2)

                        writer = pd.ExcelWriter(path_Move_input+"\\"+str(file_name))

                        # Check screen dieu kien tra cuu
                        ele_Dieukientracuu = '//*[@id="khung_noidung"]/div[4]/b/i/span'
                        if check_element(driver, ele_Dieukientracuu, int_Timeout=5) == True:
                            # Không tìm thấy bản ghi nào thỏa mãn điều kiện tra cứu
                            LOG_INFO("LOG_ERROR: "+ driver.find_element_by_xpath(ele_Dieukientracuu).text)
                            df_input["Status"][idx] = "Thông tin lỗi"
                            time.sleep(1)

                            df_input["Submitted declaration"][idx] = (driver.find_element_by_xpath(ele_Thongbaoketqua)).text
                            df_input.to_excel(writer, index = False, engine='openpyxl')
                            # writer.save()
                            time.sleep(1)

                            send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" MST "+str_MST+" không tìm thấy bản ghi nào thỏa mãn điều kiện tra cứu. Vui lòng kiểm tra!", to_email=str_Email)

                        else:
                            # ---- Table tra cuu
                            lst_Kytinhthue = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[3]')
                            lst_Ngaynop = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[8]')
                            lst_Trangthai = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[10]')

                            lst_Lannop = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[7]')
                            lst_Lydotuchoi = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[11]')
                            lst_Taive = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/div[2]/table/tbody/tr[*]/td[15]/a')

                            str_Kytinhthue = str_Kykekhai +"/" + str(str_Nam)

                            global str_Ngaynop
                            
                            for idx_Kytinhthue, j_Kytinhthue in enumerate(lst_Kytinhthue):

                                str_Ngaynop = str(lst_Ngaynop[idx_Kytinhthue].text).split(" ")[0].strip()

                                # Check status ----
                                if j_Kytinhthue.text == str_Kytinhthue and (str(lst_Trangthai[idx_Kytinhthue].text).find("Không chấp nhận việc nộp HSKT điện tử") or str(lst_Trangthai[idx_Kytinhthue].text).find("Cơ quan thuế chấp nhận hồ sơ khai thuế điện tử của NNT")):

                                    driver.execute_script("arguments[0].click();",lst_Taive[idx_Kytinhthue-1])
                                    time.sleep(3)
                                    
                                    # Get link .xml
                                    str_dowload_file = get_link_dowload(str_MST)
                                    df_input["Submitted declaration"][idx] = str_dowload_file
                                    LOG_INFO("DA UPDATE DUONG DAN FILE DA NOP: "+ str(df_input["Submitted declaration"][idx]))
                                    time.sleep(1)
                                    
                                    # up Status, str_Thongbao_Cucthue
                                    df_input["Status"][idx] = lst_Trangthai[idx_Kytinhthue].text
                                    df_input.to_excel(writer, index = False, engine='openpyxl')
                                    # writer.save()

                                    time.sleep(1)
                                    LOG_INFO("DA UPDATE HO SO - ID: "+ str_MST + " "+ str(df_input["Status"][idx]))
                                    time.sleep(5)
                                    break

                            driver.switch_to.default_content()
                            
                            btn_Tracuuthongbao = '//*[@class="submenuEpay"]/div/div[3]/ul/li/a'
                            select_xpath_submenu(driver, btn_Tracuuthongbao, input_option="Tra cứu thông báo")
                            time.sleep(1)

                            #--------- Form Tra cuu thong bao
                            driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tranFrame"]'))
                            time.sleep(1)

                            select_xpath_options(driver, '//*[@id="frm"]/table/tbody/tr/td[2]/select', '//*[@id="frm"]/table/tbody/tr/td[2]/select/option',input_option="V/v: Xác nhận nộp hồ sơ thuế điện tử")
                            input_Ngaygui = driver.find_element_by_xpath('//*[@class="form"]/form/table/tbody/tr[2]/td[2]/input[1]')
                            input_Ngaygui.click()
                            input_Ngaygui.clear()
                            input_Ngaygui.send_keys(str_Ngaynop)
                            time.sleep(1)

                            btn_submit_Tracuu = driver.find_element_by_xpath('//*[@id="frm"]/table/tbody/tr[3]/td[2]/input')
                            btn_submit_Tracuu.click()
                            time.sleep(1)
    
                            # Check thong bao 
                            ele_Thongbaoketqua = '//*[@class="frmhienthi"]/b/i/span'
                            if check_element(driver, ele_Thongbaoketqua, 5) == True:

                                send_mail(header="Cảnh báo file "+ file_name, text= "File "+file_name+" MST "+str_MST+" không có kết quả thông báo về vấn đề này. Vui lòng kiểm tra!", to_email=str_Email)
                                LOG_INFO("LOG_ERROR: "+ driver.find_element_by_xpath(ele_Thongbaoketqua).text)
                                time.sleep(1)

                                # Không có kết quả thông báo về vấn đề này
                                df_input["Notification from Tax Departmet"][idx] = (driver.find_element_by_xpath(ele_Thongbaoketqua)).text
                                df_input.to_excel(writer, index = False, engine='openpyxl')
                                # writer.save()
                                time.sleep(1)

                            else:

                                lst_Thongbao = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/table/tbody/tr[*]/td[3]')
                                lst_Ngaygui = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/table/tbody/tr[*]/td[4]')
                                lst_Taifile_request = driver.find_elements_by_xpath('//*[@id="frmtracuu"]/table/tbody/tr[*]/td[5]/a')
                                
                                for idx_request, i_request in enumerate(lst_Taifile_request):
                                    driver.execute_script("arguments[0].click();",i_request)
                                    time.sleep(3)

                                    dowload_file_request = get_link_request(str_MST)
                                    str_dowload_file_request = dowload_file_request[0]
                                    date_time = dowload_file_request[1].replace(":","")
                                    str_rename_file = str_dowload_file_request +"_"+ str_MST+"_"+date_time
                                    os.rename(str_dowload_file_request, str_rename_file)
                                    time.sleep(2)

                                    df_input["Notification from Tax Departmet"][idx] = str_rename_file
                                    df_input.to_excel(writer, index = False, engine='openpyxl')
                                    # writer.save()

                                    LOG_INFO("DA UPDATE DUONG DAN FILE DA NOP: "+ df_input["Notification from Tax Departmet"][idx])
                                    time.sleep(5)
                                    break
                        writer.save()
                        writer.close()        
                        driver.switch_to.default_content()
                        try:
                            btn_Dangxuat = driver.find_element_by_xpath('//*[@class="banner"]/div[3]/span[2]/strong/a').click()
                            time.sleep(3)
                            alert =  Alert(driver)
                            LOG_INFO("ACCEPT: "+ alert.text)
                            alert.accept()
    
                        except NoAlertPresentException:
                            LOG_INFO("KHONG TIM THAY ALERT")
                        time.sleep(2)
                        # Check element button logout
                        ele_Dangxuat = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="dangnhap"]/span[2]/strong/a')))
                        if str(ele_Dangxuat.text).strip() == "Đăng nhập":
                            LOG_INFO("DANG XUAT THANH CONG")

                        driver.quit()
                    except Exception as e:      
                        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
                        writer.save()
                        writer.close()
                        driver.quit()


            if check_df(df_input) == True:
                LOG_INFO("HOAN THANH UPDATE TRANG THAI HO SO: "+ file_name)

                # Check status update
                move_file(file_Move, path_Output , file_name)
                time.sleep(5)
                # Send email successed file
                send_mail(header="Hoàn thành tra cứu "+ file_name, text= "File "+file_name+" đã hoàn thành update trạng thái hồ sơ. Vui lòng kiểm tra!", to_email= email_nhan)
                time.sleep(1)

                save_record()
    except Exception as e:      
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
        save_record()


def get_link_request(str_MST):
    "Get link file request"
    lst_link = []
    
    path_to_download_folder = glob.glob(os.path.join(path_Download)+"\\*")
    for file_dowload in path_to_download_folder:
        # get MST file
        file_name = file_dowload.split("\\")[-1]
        if file_name == "Request":
            lst_link.append(file_dowload)
        time.sleep(1)

    for i_link_dowload in lst_link:
        # get date_time
        f = os.path.getmtime(i_link_dowload)
        date_time = datetime.datetime.fromtimestamp(f)
        str_date = date_time.strftime("%Y-%m-%d %H:%M:%S")
        time_max = get_time_file_request(lst_link)
        if str_date == time_max:
            time.sleep(1)
            return i_link_dowload, str_date


def get_time_file_request(lst_link):
    # get date_time max list lst_link
    import os, datetime
    lst_date = []
    for file in lst_link:
        f = os.path.getmtime(file)
        date_time = datetime.datetime.fromtimestamp(f)
        str_date = date_time.strftime("%Y-%m-%d %H:%M:%S")
        lst_date.append(str_date)
    time.sleep(1)
    time_max = max(lst_date)
    return time_max


def get_link_dowload(str_MST):
    "Get link file dowload"
    
    path_to_download_folder = glob.glob(os.path.join(path_Download)+"\\*.xml")
    lst_link = []
    for file_dowload in path_to_download_folder:
        # get MST file
        file_name_xml = file_dowload.split("\\")[-1]
        check_MST = re.findall(r"\d{10}",file_name_xml)

        for mst in check_MST:
            if mst == str_MST :
                lst_link.append(file_dowload)        
    time.sleep(1)

    for i_link_dowload in lst_link:
        # get date_time
        f = os.path.getmtime(i_link_dowload)
        date_time = datetime.datetime.fromtimestamp(f)
        str_date = date_time.strftime("%Y-%m-%d %H:%M:%S")
        time_max = get_time_file_xml(lst_link)

        mst =  re.findall(r"\d{10}",i_link_dowload)[0]
        if mst == str_MST and str_date == time_max:
            # print(i_link_dowload)
            time.sleep(1)
            return i_link_dowload 


def get_time_file_xml(lst_link):
    # get date_time max list link_MST
    import os, datetime
    lst_date = []
    for file in lst_link:
        f = os.path.getmtime(file)
        date_time = datetime.datetime.fromtimestamp(f)
        str_date = date_time.strftime("%Y-%m-%d %H:%M:%S")
        lst_date.append(str_date)

    time.sleep(1)
    time_max = max(lst_date)
    return time_max


def check_df(df_input):
    "Check Status"

    df_input.astype(str)
    for idx, row in df_input.iterrows():
        if str(row).find("CT01") != -1 or str(row).find("Tình trạng") != -1:
            continue
        if str(df_input["Status"][idx]).lower() == "nan" or str(df_input["Status"][idx]).lower() == "":
            return False
    return True

def wait_OTP(driver, xpath_InputOPT, xpath_SendOPT, name_Port ,timeout = 60):
    "Get OTP"
    import main_API
    date_time = datetime.datetime.now()
    str_date = date_time.strftime("%Y-%m-%d")

    ip_config = data_config["ip_otp"]
 
    count_timeout = 1
    x = 1
    day_times = ""
    str_OTP = ""
    try:
        while True:
            day_times ,str_OTP = main_API.api_otp(ip_config, name_Port)
            day_times = day_times.split(" ")[0]
            
            if str_OTP != "" and str_date == day_times:
                driver.find_element_by_xpath(xpath_InputOPT).send_keys(str_OTP)
                return day_times, str_OTP, True

            elif x == timeout:
                # Refresh OPT
                driver.find_element_by_xpath(xpath_SendOPT).click()
                x = 0
                count_timeout +=1
                time.sleep(5)
            x+=1

            if count_timeout == 4:
                return day_times, str_OTP, False
    except:
        LOG_ERROR("ERROR: KHONG TIM THAY THIET BI. VUI LONG KIEM TRA!")
        return day_times, str_OTP, False

def get_Text():
    "Request text messgase OTP"

    import requests
    import json
    try:
        while True:
            ip_config = data_config["ip_otp"]
            str_textOTP = data_config["thu_muc_text_OTP"]

            lst_Port = ["1","2","3","4","5","6","7","8"]
            for name_port in lst_Port:

                url = "http://"+str(ip_config)+"/API/QueryInfo"
                payload = json.dumps({"event": "newqueryrxsms", "port": ""+str(name_port)+""})
                
                headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic QXBpVXNlckFkbWluOlZicG8xMjM0NQ=='
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                load_text_OTP = json.loads(response.text,strict=False)['content']
                load_text_OTP = re.sub(";","\n",load_text_OTP)

                with open(str_textOTP +"\\" +"request_OTP"+name_port+".txt",mode="w+" ,encoding="utf-8") as load_Text:
                    load_Text.write(load_text_OTP)
                    load_Text.close()
    except:
        pass

def message(header="",text="", file_img=None, file_dinhkem=None):
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg.attach(MIMEText(text))

    if file_img is not None:

        # if type(img) is not list:
        #     # if it isn't a list, make it one
        #     img = [img]  
        for one_img in file_img:
            img_data = open(one_img, 'rb').read()
            msg.attach(MIMEImage(img_data, name=os.path.basename(one_img)))

    if file_dinhkem is not None:

        for one_file_dinhkem in file_dinhkem:
            with open(one_file_dinhkem, 'rb') as f:
                
                # Read in the attachment using MIMEApplication
                file = MIMEApplication(f.read(),name=os.path.basename(one_file_dinhkem))
            
        file['Content-Disposition'] = f'attachment;\filename="{os.path.basename(one_file_dinhkem)}"' 
        msg.attach(file)

    msg['Subject'] = "[PIT-OTP] "+header

    return msg

def send_mail(header="",text="",to_email ="", file_dinhkem = None):
    "Send email"
    import smtplib
    import os
    import ssl
    import glob
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    context = ssl.create_default_context()

    smtp.starttls(context= context)
    smtp.login(id_email_gui, pass_email_gui)
    msg = message(header=header, text=text, file_img = None, file_dinhkem = None)

    # to = ["1235@gmail.com"]
    smtp.sendmail(from_addr= id_email_gui, to_addrs = to_email, msg = msg.as_string())    
    smtp.quit()


if __name__ == "__main__":
    import datetime
    import schedule
    import time
    import threading
    LOG_INFO("BẮT ĐẦU CHẠY")
    
    try:
        thread_run_text = thread_with_trace(target=get_Text)
        thread_run_text.start()
    except:
        LOG_ERROR("ERROR: KHONG TIM THAY THIET BI. VUI LONG KIEM TRA!")
        pass

    if data_config['lien_tuc'] == True:
        while True:
            thu_tuc()
            time.sleep(2)
            tracuu_Tokhai()
    else:
        schedule.every().day.at(data_config['che_do_ke_khai']['thoi_gian_co_dinh']).do(thu_tuc)
        schedule.every().day.at(data_config['che_do_quet_ket_qua']['thoi_gian_co_dinh']).do(tracuu_Tokhai)

    while True:
        schedule.run_pending()
        time.sleep(1)
