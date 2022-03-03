import datetime
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import alert
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import pandas as pd
from pandas import ExcelWriter
import time
import os, inspect, sys
import re
import glob
from PIL import Image
import mysql.connector
import ocr_capcha
import shutil
import threading
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

path_img = os.path.abspath(CurDir +"\\captcha")
path_chrome = os.path.abspath(CurDir +"\\chromedriver.exe")


import logging
global LOG_INFO
global LOG_ERROR

name_Organization = "vpo"
name_Robot = "P.I.T"
name_Version = "1.1.6"
name_Config = "config_pj-vpo_robot.json"
name_Logs = "logs_pj-vpo_robot.txt"
name_Config_port = "config_pj-vpo_port-name.json"


logging.basicConfig(format='------------------ %(asctime)s >>>  %(message)s  <<<------------------', datefmt='%d/%m/%Y %H:%M:%S')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s",datefmt='%d/%m/%Y %H:%M:%S')
LOG_INFO = logging.warning
LOG_ERROR = logging.error
FileHandler = logging.FileHandler(CurDir+"\\" + name_Logs, 'a+', 'utf-8')
FileHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(FileHandler)

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
data_security = readJson(CurDir+"\\conf\\config_pj-vpo_security")

url_terra = data_config['url_terra']
url_service = data_config['url_service']


username_terra = data_security['username_terra']
password_terra =data_security['password_terra']
code_terra = data_security['code_terra']

# ------ API Terra---------

def login_terra():
    import requests
    import json
    url = url_terra
    payload="{\"query\":\"mutation login ($username: String!, $password: String!, $client_code: String) {\\n    login (username: $username, password: $password, client_code: $client_code) {\\n        access_token\\n        refresh_token\\n        expires_in\\n        token_type\\n    }\\n}\",\"variables\":{\"username\":\""+username_terra+"\",\"password\":\""+password_terra+"\",\"client_code\":\""+code_terra+"\"}}"
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def get_clients_terra(access_token_terra):
    import requests
    import json
    url = url_terra
    payload="{\"query\":\"query getWithAssignments($perPage: Int!, $page: Int, $orderBy: [ClientsOrderByOrderByClause!], $where: ClientsWhereWhereConditions) {\\n  clients(orderBy: $orderBy, where: $where, first: $perPage, page: $page) {\\n    paginatorInfo {\\n      count\\n      currentPage\\n      firstItem\\n      hasMorePages\\n      lastItem\\n      lastPage\\n      perPage\\n      total\\n      __typename\\n    }\\n    data {\\n      ...clientFields\\n      assignedInternalEmployees {\\n        id\\n        name\\n        code\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment clientFields on Client {\\n  id\\n  code\\n  company_name\\n  company_contact_phone\\n  company_contact_email\\n  address\\n  company_bank_account\\n  company_account_number\\n  company_bank_name\\n  company_bank_branch\\n  person_signing_a_bank_document\\n  employees_number_foreign\\n  employees_number_vietnamese\\n  rewards_for_achievements\\n  annual_salary_bonus\\n  social_insurance_and_health_insurance_ceiling\\n  unemployment_insurance_ceiling\\n  payroll_creator\\n  payroll_approver\\n  social_insurance_agency\\n  social_insurance_account_name\\n  social_insurance_account_number\\n  social_insurance_bank_name\\n  social_insurance_bank_branch\\n  social_insurance_unit_code\\n  trade_union_agency\\n  trade_union_account_name\\n  trade_union_account_number\\n  trade_union_bank_name\\n  trade_union_bank_branch\\n  presenter_phone\\n  company_contact_fax\\n  presenter_email\\n  presenter_name\\n  company_license_no\\n  company_license_issuer\\n  company_license_issued_at\\n  company_license_updated_at\\n  company_license_at\\n  timesheet_min_time_block\\n  day_payroll_start\\n  day_payroll_end\\n  type_of_business\\n  clientWorkflowSetting {\\n    id\\n    client_id\\n    enable_overtime_request\\n    enable_leave_request\\n    enable_early_leave_request\\n    enable_timesheet_input\\n    enable_social_security_manage\\n    enable_salary_payment\\n    manage_user\\n    enable_wifi_checkin\\n    enable_training_seminar\\n    enable_recruit_function\\n    enable_contract_reminder\\n    __typename\\n  }\\n  created_at\\n  updated_at\\n  is_active\\n  __typename\\n}\\n\",\"variables\":{\"perPage\":1000,\"page\":1,\"orderBy\":[{\"field\":\"COMPANY_NAME\",\"order\":\"ASC\"}],\"where\":{}}}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def get_ReportPits(id_client,access_token_terra):

    import requests
    import json

    url = url_terra

    payload="{\"query\":\"query getReportPits($perPage: Int!, $page: Int, $orderBy: [ReportPitsOrderByOrderByClause!], $where: ReportPitsWhereWhereConditions) {\\r\\n  reportPits(orderBy: $orderBy, where: $where, first: $perPage, page: $page) {\\r\\n    paginatorInfo {\\r\\n      count\\r\\n      currentPage\\r\\n      firstItem\\r\\n      hasMorePages\\r\\n      lastItem\\r\\n      lastPage\\r\\n      perPage\\r\\n      total\\r\\n      __typename\\r\\n    }\\r\\n    data {\\r\\n      id\\r\\n      name\\r\\n      code\\r\\n      date_from_to\\r\\n      form_data\\r\\n      client_id\\r\\n      status\\r\\n      export_status\\r\\n      approved_comment\\r\\n      trang_thai_xu_ly\\r\\n      created_at\\r\\n      updated_at\\r\\n      path\\r\\n      duration_type\\r\\n      quy_value\\r\\n      quy_year\\r\\n      thang_value\\r\\n      client {\\r\\n        code\\r\\n        company_name\\r\\n        __typename\\r\\n      }\\r\\n      __typename\\r\\n    }\\r\\n    __typename\\r\\n  }\\r\\n}\\r\\n\",\"variables\":{\"perPage\":1000,\"page\":1,\"orderBy\":[{\"field\":\"CREATED_AT\",\"order\":\"DESC\"}],\"where\":{\"AND\":[{\"column\":\"CLIENT_ID\",\"operator\":\"EQ\",\"value\":\""+id_client+"\"}]}}}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def post_ReportPitInputUpdate(id_Input_reportPit, access_token_terra, status_Update):
    import requests
    import json

    url = url_terra

    payload="{\"query\":\"mutation update($id: ID!, $input: ReportPitInputUpdate) {\\r\\n  updateReportPit(id: $id, input: $input) {\\r\\n    ...reportPitFields\\r\\n    __typename\\r\\n  }\\r\\n}\\r\\n\\r\\nfragment reportPitFields on ReportPit {\\r\\n  id\\r\\n  status\\r\\n  export_status\\r\\n  __typename\\r\\n}\\r\\n\",\"variables\":{\"id\":\""+id_Input_reportPit+"\",\"input\":{\"trang_thai_xu_ly\":\""+status_Update+"\"}}}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


  

# ---------API Service--------------
def get_service(id_client):
    import requests
    payload = ""
    url = url_service+"/claim/?company_claim="+str(id_client)
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1'
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def post_service(payload):
    import requests
    import json

    url = url_service+"/claim/"
    payload = json.dumps(payload)
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def patch_service(id,payload):
    import requests
    import json

    url =url_service+"/claim/"+str(id)+"/"
    payload = json.dumps(payload)
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1',
    'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    return response.json()


url_Thuedoanhnghiep = 'https://thuedientu.gdt.gov.vn/etaxnnt/Request?&dse_sessionId=opLE55FV2bAnltX5V-tNM3S&dse_applicationId=-1&dse_pageId=1&dse_operationName=corpIndexProc&dse_errorPage=error_page.jsp&dse_processorState=initial&dse_nextEventName=start'

def open_driver():

    options = Options()
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation",'enable-logging']) # tắt popup của face
    options.add_argument("user-data-dir="+CurDir+"\\eSignerChrome")
    options.add_extension(CurDir+ "\\eSignerChrome\\eSignerChrome_1.0.8_0.crx")
    options.add_argument("--start-maximized") 
    options.add_argument("--no-sandbox") 
    options.add_argument('disable-infobars')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    options.add_argument("--profile-directory=Default")
    prefs = {"credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_settings.popups": 0,
            'exit_type': 'Normal',
            }   #--------
    options.add_experimental_option("prefs",  {'profile': prefs}) #disable-restore-pages-poup
    time.sleep(1)
                                            
    
    driver = webdriver.Chrome(executable_path= path_chrome, options=options)
     
    return driver


def screen_capcha(driver, Curdir, xpath_capcha, count_k, bl_a = False):

    driver.save_screenshot(Curdir +"\\captcha\\screen_shot\\" + str(count_k)+".png")
    ele_capcha = driver.find_element_by_xpath(xpath_capcha)
    location = ele_capcha.location
    size = ele_capcha.size
    
    x = location['x']  
    y = location['y']  
    w = size['width']   
    h = size['height'] 
    width = x + w
    height = y + h

    # crop img 
    im = Image.open(CurDir+"\\captcha\\screen_shot\\" +str(count_k) +".png")
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


def select_xpath_submenu(driver, xpath_menu,xpath_submenu, input_option, timeout=60):
    driver.find_element_by_xpath(xpath_menu).click()

    for i, j in enumerate(driver.find_elements_by_xpath(xpath_submenu)):
        if str(j.text).strip() == input_option:
            j.click()
            break

def select_xpath_options(driver, xpath_select, xpath_options, input_option, timeout = 1):
    
    driver.find_element_by_xpath(xpath_select).click()
    time.sleep(timeout)

    for i, j in enumerate(driver.find_elements_by_xpath(xpath_options)):
        if  input_option in str(j.text).strip() :
            j.click()
            break

def sendkeys_Input(driver, xpath, input_option):
    str_value= driver.find_element_by_xpath(xpath)
    str_value.click()
    str_value.clear()
    str_value.send_keys(input_option)

def convert_datetime_string(data_input,format_input='%Y-%m-%d',format_output='%d/%m/%Y'):
    data_date = datetime.datetime.strptime(data_input, format_input)
    data_date = data_date.strftime(format_output)
    return data_date

    
def login(driver, user_name, pass_word):

    try:
        driver.get(url_Thuedoanhnghiep)
        time.sleep(2)

        # Screen Thue Dien Tu
        btn_Doanhnghiep = driver.find_element_by_xpath("//*[@class='khungbaolongin']/div[2]/div/div[2]").click()
        time.sleep(2)

        # Screen Login form
        btn_Login_form = driver.find_element_by_xpath("//*[@class='banner']/div[3]/span[2]/button").click()
        time.sleep(2)

        while True:
            try:
                input_User = driver.find_element_by_xpath("//input[@id='_userName']")
                input_User.click()
                input_User.clear()
                input_User.send_keys(user_name)
                time.sleep(2)
                    
                input_Password = driver.find_element_by_xpath('//*[@id="password"]')
                input_Password.click()
                input_Password.clear()
                input_Password.send_keys(pass_word)
                time.sleep(2)

                element_select_Doituong = '//*[@id="login_type"]'
                element_options_Doituong = '//*[@id="login_type"]/option'
                select_xpath_options(driver, element_select_Doituong, element_options_Doituong, input_option='Người nộp thuế')
                time.sleep(2)

                element_Captcha = "//*[@class='frm_login_content']/form/table/tbody/tr[4]/td/div/div[2]/img"
                str_ocr = screen_capcha(driver, CurDir, element_Captcha, count_k= 1)
                str_input_captcha = driver.find_element_by_xpath("//*[@class='frm_login_content']/form/table/tbody/tr[4]/td/div/div[1]/input")
                str_input_captcha.click()
                time.sleep(1)

                # ocr capcha
                btn_request_captcha ="//*[@class='frm_login_content']/form/table/tbody/tr[4]/td/div/div[2]/span/a"
                if len(str_ocr) == 4:
                    str_input_captcha.send_keys(str_ocr)
                else:
                    # refresh captcha
                    driver.find_element_by_xpath(btn_request_captcha).click()
                    time.sleep(1)
                    continue

                try:
                    btn_Dangnhap = driver.find_element_by_xpath('//*[@id="dangnhap"]')
                    btn_Dangnhap.click()
                    time.sleep(2)

                    alert = Alert(driver)
                    if str(alert.text).find("Bạn chưa nhập Tên đăng nhập!") != -1:
                        LOG_INFO('MST KHONG DUOC DE TRONG')
                        time.sleep(2)
                        alert.accept()
                        return False
        
                    if str(alert.text).find("Bạn chưa nhập Mật khẩu!") != -1:
                        LOG_INFO('MAT KHAU KHONG DUOC DE TRONG')
                        time.sleep(2)
                        alert.accept()
                        return False
                except:
                    pass

                time.sleep(2)
                # Check pass extension
                if check_element(driver,'//*[@id="dialog"]/form/table/tbody/tr/td/div/p[2]',5) == True:
                    driver.get(url_Thuedoanhnghiep)
                    btn_Doanhnghiep = driver.find_element_by_xpath("//*[@class='khungbaolongin']/div[2]/div/div[2]").click()
                    time.sleep(2)
                    btn_Login_form = driver.find_element_by_xpath("//*[@class='banner']/div[3]/span[2]/button").click()
                    time.sleep(2)
                    # refesh page
                    continue

                # Check login error 
                if check_element(driver,'//*[@class="frm_login_content"]/form/table/tbody/tr[6]/td/span',5) == True:

                    str_errror = driver.find_element(By.XPATH,'//*[@class="frm_login_content"]/form/table/tbody/tr[6]/td/span')  
                    if str(str_errror.text).strip() == "Tên đăng nhập hoặc mật khẩu của bạn không chính xác":
                        LOG_INFO("Tên đăng nhập hoặc mật khẩu của bạn không chính xác")
                        time.sleep(2)
                        return False

                    # check error messgase captcha
                    if str(str_errror.text).strip() == "Mã xác thực không chính xác":
                        # refresh captcha
                        driver.find_element_by_xpath(btn_request_captcha).click()
                        time.sleep(2)
                        continue

                # check password hết hạn
                if check_element(driver, "//*[@class='noidung']//table/tbody/tr[2]/td/input[2]",5) == True:
                    btn_Tieptuc = driver.find_element_by_xpath("//*[@class='noidung']//table/tbody/tr[2]/td/input[2]")
                    btn_Tieptuc.click()
                    time.sleep(2)

                ele_Check_login = driver.find_element_by_xpath('//*[@class="banner"]/div[2]/div[2]/div/span[1]')
                if str(ele_Check_login.text).strip() == 'Mã số thuế:' :
                    LOG_INFO("ĐĂNG NHẬP THÀNH CÔNG")
                    return True

            except Exception as e:
                LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))
                return False

    except Exception as e:      
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))
        return False
         
def job_kekhai():
    

    LOG_INFO("CHẠY QUY TRÌNH KÊ KHAI")
    #Lấy access_token để sử dụng api.
    rq_login_terra = login_terra()
    if rq_login_terra.get('data'):
        access_token_terra = rq_login_terra['data']['login']['access_token']
        LOG_INFO("LOGIN_TERRA: LẤY ACCESS TOKEN THÀNH CÔNG")
    else:
        LOG_INFO("LOGIN_TERRA: KHÔNG LẤY ĐƯỢC ACCESS TOKEN!")
        return


    #Lấy danh sách các khách hàng của tài khoản.
    rq_get_clients_terra = get_clients_terra(access_token_terra)
    if rq_get_clients_terra.get('data'):
        list_clients_terra = rq_get_clients_terra['data']['clients']['data']
        LOG_INFO("CLIENT_TERRA: LẤY DANH SÁCH KHÁCH HÀNG THÀNH CÔNG")
    else:
        LOG_INFO("CLIENT_TERRA: LỖI KHÔNG LẤY ĐƯỢC DANH SÁCH KHÁCH HÀNG!")
        return

    #For từng khách hàng để truy vấn danh sách hồ sơ ke khai.
    for i_client_terra in list_clients_terra:
        try:
            id_client = i_client_terra['id']
            code_client = i_client_terra['code']
            rq_get_ReportPits_terra = get_ReportPits(id_client,access_token_terra)
            if rq_get_ReportPits_terra.get('data'):
                list_ReportPits = rq_get_ReportPits_terra['data']['reportPits']['data']
                list_Claim_Company = []

                #For từng hồ sơ để xử lý
                for i_ReportPits in list_ReportPits:
                    if i_ReportPits['trang_thai_xu_ly'] == "da_phe_duyet_noi_bo" :
                        LOG_INFO("CLAIMS_TERRA: LẤY DANH SÁCH HỒ SƠ - "+i_client_terra['company_name'])
                        pass
                    else:
                        continue
                    r_result = post_service({"name_claim":i_ReportPits['id'], "data_claim":i_ReportPits, "company_claim":code_client, "status_claim":"Wait"})
                    if r_result.get('name_claim')[0] == 'claim with this name claim already exists.':
                        continue

                list_Claim_Company = get_service(code_client)
                list_Claim_Company = [x for x in list_Claim_Company if x['status_claim'] == 'Wait']

                if len(list_Claim_Company) != 0:
                    LOG_INFO(("Số lượng hồ sơ cần kê khai: "+str(len(list_Claim_Company))))
                    try:
                        mydb = mysql.connector.connect(
                        host=data_security['host_mysql'],
                        user=data_security['user_mysql'],
                        passwd=data_security['passwd_mysql'],
                        database=data_security['database_mysql']
                        )

                        mycursor = mydb.cursor()
                        mycursor.execute("SELECT * FROM social_accounts WHERE client_code = (%s)", (str(code_client),))
                        myresult = mycursor.fetchall()
                    except:
                        LOG_ERROR("KHÔNG TÌM THẤY MÃ CÔNG TY "+ str(code_client))
                        continue
                    if len(myresult) > 0:
                        myresult = myresult[0]
                    else:
                        LOG_ERROR("Không tìm thấy thông tin công ty có mã: "+str(code_client))
                        continue

                    # Download file input
                    get_Report_file(list_Claim_Company, id_client, access_token_terra)

                    lst_input = path_input()
                    # For ds số lượng hồ sơ cần kê khai
                    for i_Claim_Company in list_Claim_Company:
                        path_name_input = str(i_Claim_Company["data_claim"]["path"]).split('?')[0].split('/')[-1]
                        data_claim = i_Claim_Company['data_claim']
                        for file in lst_input:
                            if str(file).find("~$") != -1:
                                continue
                            file_name = str(file).split("\\")[-1]
                            if path_name_input == file_name:
                                # -----------
                                df_input = pd.read_excel(file, sheet_name="Declaration (EN)", engine='openpyxl', dtype=object)
                                for idx, row in df_input.iterrows():
                                    if str(row).find('[01]') and str(row).find("Quarter") != -1:

                                        str_Quykekhai = (re.findall('(?<=\(Quarter\)\s)\d{1}',df_input.iloc[idx,1]))[0]
                                        str_Namkekhai = (re.findall('(?<=\(Year\)\s)\d{4}',df_input.iloc[idx,1]))[0]
                                        str_Thangkekhai = ""

                                    if str(row).find('[01]') and str(row).find("Month") != -1:
                                        str_Namkekhai = (re.findall('(?<=\(Year\)\s)\d{4}',df_input.iloc[idx,1]))[0]
                                        str_Thangkekhai = (re.findall('(?<=\(Month\)\s)\d{1,2}',df_input.iloc[idx,1]))[0]
                                        str_Quykekhai = ""

                                    if str(row).find('[02]') != -1:
                                        
                                        if str(row).find("Lần đầu (First time):     [ X ]") != -1:
                                            str_Tokhai = "Tờ khai chính chức"      
                                        else :                                            
                                            str_Tokhai = "Tờ khai bổ sung"

                                         
                                try:
                                    driver = open_driver()
                                    if login(driver,myresult[2],myresult[3]) == False:
                                        driver.quit()
                                        LOG_INFO('dang nhap k thanh cong: send mail')
                                        continue
                                    
                                    if thu_tuc(driver, to_khai=str_Tokhai, quy_kekhai=str_Quykekhai, thang_kekhai=str_Thangkekhai, nam_kekhai=str_Namkekhai) == False:
                                        driver.quit()
                                        time.sleep(1)
                                        continue
                                    else:
                                        job_kekhai, str_STT = ke_khai(driver, file)
                           
                                        if job_kekhai == True:
                                           
                                            post_ReportPitInputUpdate(data_claim['id'], access_token_terra, status_Update="da_ke_khai_va_luu_tam")
                                            LOG_INFO("HỒ SƠ LƯU TẠM "+str(i_Claim_Company['data_claim']['id'])+" "+str(str_STT)+" CẬP NHẬT TERRA")

                                            new_Dataclaim = get_New_dataclaim(id_client,access_token_terra, i_Claim_Company['data_claim']['id'])
                                            (patch_service(i_Claim_Company['id'],{'data_claim':new_Dataclaim,"status_claim":"Running", "note_claim":str(str_STT), "status_process_claim": "Đã kê khai và lưu tạm hồ sơ"}))
                                            LOG_INFO("HỒ SƠ LƯU TẠM "+str(i_Claim_Company['data_claim']['id'])+" "+str(str_STT)+" CẬP NHẬT LƯU TRỮ")

                                            #  MOVE DATA INPUT -> OUTPUT
                                            move_file(file, data_config['thu_muc_backup'],data_claim['id'])

                                        else:
                                            patch_service(i_Claim_Company['id'],{"status_claim":"Error","note_claim":str(str_STT)})
                                            move_file(file, data_config['thu_muc_backup'],data_claim['id'])
                                            LOG_INFO("HỒ SƠ BỊ LỖI")
                                             
                                    driver.quit()
         
                                except Exception as e:
                                   
                                    LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))
                                    patch_service(i_Claim_Company['id'],{"status_claim":"Error","note_claim":str(str_STT)})
                                    move_file(file, data_config['thu_muc_backup'],data_claim['id'])

        except Exception as e:                        
            LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))

def job_tracuu():
    try:
        LOG_INFO("CHẠY QUY TRÌNH TRA CỨU")
        #Lấy access_token để sử dụng api.
        rq_login_terra = login_terra()
        if rq_login_terra.get('data'):
            access_token_terra = rq_login_terra['data']['login']['access_token']
            LOG_INFO("LOGIN_TERRA: LẤY ACCESS TOKEN THÀNH CÔNG")
        else:
            LOG_INFO("LOGIN_TERRA: KHÔNG LẤY ĐƯỢC ACCESS TOKEN!")
            return


        #Lấy danh sách các khách hàng của tài khoản.
        rq_get_clients_terra = get_clients_terra(access_token_terra)
        if rq_get_clients_terra.get('data'):
            list_clients_terra = rq_get_clients_terra['data']['clients']['data']
            LOG_INFO("CLIENT_TERRA: LẤY DANH SÁCH KHÁCH HÀNG THÀNH CÔNG")
        else:
            LOG_INFO("CLIENT_TERRA: LỖI KHÔNG LẤY ĐƯỢC DANH SÁCH KHÁCH HÀNG!")
            return

        #For từng khách hàng để truy vấn danh sách hồ sơ ke khai.
        for i_client_terra in list_clients_terra:
            try:
                id_client = i_client_terra['id']
                code_client = i_client_terra['code']
                rq_get_ReportPits_terra = get_ReportPits(id_client,access_token_terra)
                if rq_get_ReportPits_terra.get('data'):
                    list_ReportPits = rq_get_ReportPits_terra['data']['reportPits']['data']
                    list_Claim_Company = []

                    #For từng hồ sơ để xử lý
                    for i_ReportPits in list_ReportPits:
                        if i_ReportPits['trang_thai_xu_ly'] == "da_ky_nop_ho_so" :
                            LOG_INFO("CLAIMS_TERRA: LẤY DANH SÁCH HỒ SƠ - "+i_client_terra['company_name'])
                        else:
                            continue

                    list_Claim_Company = get_service(code_client)
                    list_Claim_Company = [x for x in list_Claim_Company if x['status_claim'] == 'Running']
                    for i_ReportPits in list_ReportPits:
                        if len(list_Claim_Company) != 0 and i_ReportPits['trang_thai_xu_ly'] == "da_ky_nop_ho_so":
                            LOG_INFO(("Số lượng hồ sơ cần tra cứu: "+str(len(list_Claim_Company))))
                            try:
                                mydb = mysql.connector.connect(
                                host=data_security['host_mysql'],
                                user=data_security['user_mysql'],
                                passwd=data_security['passwd_mysql'],
                                database=data_security['database_mysql']
                                )

                                mycursor = mydb.cursor()
                                mycursor.execute("SELECT * FROM social_accounts WHERE client_code = (%s)", (str(code_client),))
                                myresult = mycursor.fetchall()
                            except:
                                LOG_ERROR("KHÔNG TÌM THẤY MÃ CÔNG TY "+ str(code_client))
                                continue
                            if len(myresult) > 0:
                                myresult = myresult[0]
                            else:
                                LOG_ERROR("Không tìm thấy thông tin công ty có mã: "+str(code_client))
                                continue

                            # For ds số lượng hồ sơ cần kê khai
                            for i_Claim_Company in list_Claim_Company:
                                try:
                                    driver = open_driver()
                                    if login(driver,myresult[2],myresult[3]) == False:
                                        driver.quit()
                                        LOG_INFO('ĐĂNG NHẬP KHÔNG THÀNH CÔNG!')
                                        continue

                                    #  ----------------
                                    bl_check,str_Noteclaim =  tracuu_tokhai(driver, i_Claim_Company['data_claim'])
                                    if bl_check == True:
                                        if str_Noteclaim == 'CHƯA CÓ KẾT QUẢ TRA CỨU':
                                            LOG_INFO("CHƯA CÓ KẾT QUẢ TRA CỨU")
                                            driver.quit()
                                            continue

                                        else:
                                            (post_ReportPitInputUpdate(i_Claim_Company['data_claim']['id'], access_token_terra, status_Update="chap_nhan_khong_chap_nhan_ho_so_thue_dien_tu"))
                                            LOG_INFO("HỒ SƠ ĐANG XỬ LÍ "+str(i_Claim_Company['data_claim']['id'])+" "+str(str_Noteclaim)+" CẬP NHẬT TERRA")
                                        
                                            new_Dataclaim = get_New_dataclaim(id_client,access_token_terra, i_Claim_Company['data_claim']['id'])
                                            (patch_service(i_Claim_Company['id'],{'data_claim':new_Dataclaim,"status_claim":"Complete", "note_claim":str(str_Noteclaim), "status_process_claim": "Đã có kết quả"}))
                                            LOG_INFO("HỒ SƠ ĐANG XỬ LÍ "+str(i_Claim_Company['data_claim']['id'])+" "+str(str_Noteclaim)+" CẬP NHẬT LƯU TRỮ")

                                    else:
                                        patch_service(i_Claim_Company['id'],{"status_claim":"Error","note_claim":str(str_Noteclaim)})
                                        LOG_INFO("HỒ SƠ BỊ LỖI")
                

                                    driver.quit()
        
                                except Exception as e:
                                    LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))
                                    patch_service(i_Claim_Company['id'],{"status_claim":"Error","note_claim":str(str_Noteclaim)})
            except Exception as e:                        
                LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))
                driver.quit()

    except Exception as e:                        
            LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))

def get_New_dataclaim(id_client,access_token_terra, data_input):

    rq_get_ReportPits_terra = get_ReportPits(id_client,access_token_terra)
    if rq_get_ReportPits_terra.get('data'):
        list_ReportPits = rq_get_ReportPits_terra['data']['reportPits']['data']

        #For từng hồ sơ
        for i_ReportPits in list_ReportPits:
            if i_ReportPits['id'] == data_input:
                return i_ReportPits


def tracuu_tokhai(driver,data_input):
    'Form tra cứu tờ khai'
    try:
        select_xpath_submenu(driver, xpath_menu='//*[@id="ddtabs1"]/ul/li[3]/a', xpath_submenu= '//*[@class="submenuEpay"]/div/div[3]/ul/li[*]/a', input_option='Tra cứu tờ khai', timeout= 5)
        time.sleep(2)

        #------   Screen Tra cứu  ---------
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tranFrame"]'))

        # ------ Tờ khai ------
        xpath_select_Tokhai = '//*[@class="indent"]/table/tbody/tr[1]/td[2]/select'
        xpath_options_Tokhai = '//*[@class="indent"]/table/tbody/tr[1]/td[2]/select/option'
        select_xpath_options(driver, xpath_select_Tokhai, xpath_options_Tokhai, input_option='05/KK-TNCN')
        time.sleep(1)

        # ----- Ngày nộp từ ngày -------
        daytime_update = str(data_input['created_at']).split(" ")[0]                    
        day_Time_Noptungay = convert_datetime_string(daytime_update)

        # day_Time_Noptungay = '15/09/2021'        # INPUT TEST
        ele_Ngaynoptungay = '//*[@class="indent"]/table/tbody/tr[3]/td[2]/input'
        sendkeys_Input(driver, ele_Ngaynoptungay, input_option=day_Time_Noptungay)            
        time.sleep(1)

        ele_Denngay = '//*[@class="indent"]/table/tbody/tr[3]/td[4]/input'
        str_Denngay = datetime.datetime.now().strftime('%d/%m/%Y')
        sendkeys_Input(driver, ele_Denngay, input_option=str_Denngay)
        time.sleep(1)
        
        button_Tracuu = driver.find_element_by_xpath('//*[@class="indent"]/table[2]/tbody/tr[1]/td/div/input').click()
        if check_element(driver, xpath='//*[@id="traCuuKhaiForm"]/div[4]/div/strong', int_Timeout= 5):
            LOG_INFO('Chưa có tờ khai nào được gửi thỏa mãn điều kiện tra cứu trên!')
            return True, "CHƯA CÓ KẾT QUẢ TRA CỨU"
        time.sleep(1)


        #  ------ Table Kết quả tra cứu ------
        if data_input['quy_value'] != 0:
            str_Kytinhthue = "Q"+str(data_input['quy_value'])+"/"+str(data_input['quy_year'])
        else:
            str_Kytinhthue = str(data_input['thang_value']).replace('-',"/")

        # str_Kytinhthue = 'Q3/2021'    # INPUT TEST
        lst_Kytinhthue = driver.find_elements_by_xpath('//*[@id="allResultTableBody"]/tr/td[4]')
        lst_Trangthai = driver.find_elements_by_xpath('//*[@id="allResultTableBody"]/tr/td[11]')

        for idx_kytinhthue, i_kytinhthue in enumerate(lst_Kytinhthue):
            if str(i_kytinhthue.text).strip() == str_Kytinhthue and str(lst_Trangthai[idx_kytinhthue].text).strip() == 'Cơ quan thuế chấp nhận hồ sơ khai thuế điện tử của NNT':
                LOG_ERROR("ID: "+ str(data_input['id'])+ " CƠ QUAN THUẾ CHẤP NHẬN HỒ SƠ")
                return True, "TRA CỨU HOÀN TẤT"
            elif str(i_kytinhthue.text).strip() == str_Kytinhthue and str(lst_Trangthai[idx_kytinhthue].text).strip().lower().find('không chấp nhận') != -1:
                LOG_ERROR("ID: "+ str(data_input['id'])+ " CƠ QUAN THUẾ KhÔNG CHẤP NHẬN HỒ SƠ")
                return True, "TRA CỨU HOÀN TẤT"
            else:
                LOG_INFO('Chưa có tờ khai nào được gửi thỏa mãn điều kiện tra cứu trên!')
                return True, "CHƯA CÓ KẾT QUẢ TRA CỨU"
        time.sleep(1)

    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))
        return False, "TRA CỨU CÓ LỖI"


def thu_tuc(driver, to_khai="", quy_kekhai="", thang_kekhai="", nam_kekhai = ""):
    try:
        select_xpath_submenu(driver, xpath_menu='//*[@id="ddtabs1"]/ul/li[3]/a', xpath_submenu= '//*[@class="submenuEpay"]/div/div[3]/ul/li[*]/a', input_option='Kê khai trực tuyến', timeout= 5)
        time.sleep(2)

        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="tranFrame"]'))

        #------   Screen Kê khai trực tuyến  ---------
        xpath_select_Tokhai = '//*[@id="LapTKhaiOnlineForm"]/table/tbody/tr/td/table/tbody/tr[1]/td/select'
        xpath_options_Tokhai = '//*[@id="LapTKhaiOnlineForm"]/table/tbody/tr/td/table/tbody/tr[1]/td/select/option'
        
        #  To Khai
        select_xpath_options(driver, xpath_select_Tokhai, xpath_options_Tokhai, input_option='05/KK-TNCN')
        time.sleep(1)

        # Loai to khai
        xpath_select_Loaitokhai = '//*[@id="LapTKhaiOnlineForm"]/table/tbody/tr/td/table/tbody/tr[3]/td/select'
        xpath_option_Loaitokhai = '//*[@id="LapTKhaiOnlineForm"]/table/tbody/tr/td/table/tbody/tr[3]/td/select/option'
        select_xpath_options(driver, xpath_select_Loaitokhai, xpath_option_Loaitokhai, input_option= to_khai)
        time.sleep(1)

        # Ky ke khai 
        xpath_select_Kykekhai = '//*[@id="LapTKhaiOnlineForm"]/table/tbody/tr/td/table/tbody/tr[4]/td/select'
        xpath_option_Kykekhai = '//*[@id="LapTKhaiOnlineForm"]/table/tbody/tr/td/table/tbody/tr[4]/td/select/option'

        if len(driver.find_elements_by_xpath(xpath_option_Kykekhai)) == 4:
            # Check screen ke khai theo quy
            select_xpath_options(driver, xpath_select_Kykekhai, xpath_option_Kykekhai,input_option= "Q"+quy_kekhai)

        elif len(driver.find_elements_by_xpath(xpath_option_Kykekhai)) == 12:
            # Check screen ke khai theo thang

            # thang_kekhai = "6"         # INPUT TEST
            select_xpath_options(driver, xpath_select_Kykekhai, xpath_option_Kykekhai, input_option=thang_kekhai)     
        time.sleep(1)

        input_Namkekhai = driver.find_element_by_xpath('//*[@id="LapTKhaiOnlineForm"]/table/tbody/tr/td/table/tbody/tr[4]/td/input[2]')
        input_Namkekhai.click()
        input_Namkekhai.clear()
        input_Namkekhai.send_keys(nam_kekhai)

        button_Tieptuc = driver.find_element_by_xpath('//*[@id="tieptucBT"]')
        button_Tieptuc.click()
        time.sleep(1)

        # Đã có tờ khai chính thức được chấp nhận. Bạn phải nộp tờ khai bổ sung.
        if check_element(driver,'//*[@class="box_common_content"]/b/span',5) == True:
            LOG_INFO(driver.find_element_by_xpath('//*[@class="box_common_content"]/b/span').text)
            return False

        return True
    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
        return False

def ke_khai(driver, file):
    "Screen form Ke khai"

    try:

        df_input = pd.read_excel(file, sheet_name="Declaration (EN)", engine='openpyxl', dtype=object)
        for idx, row in df_input.iterrows():
            # ---------
            if str(row).find('[21]') != -1:
                str_CT21 = get_Input_data(file, row= idx, column=19)
            if str(row).find('[22]') != -1:
                str_CT22 = get_Input_data(file, row= idx, column=19)
            
            # ---------
            if str(row).find('[24]') != -1:
                str_CT24 = get_Input_data(file, row= idx, column=19)
            if str(row).find('[25]') != -1:
                str_CT25 = get_Input_data(file, row= idx, column=19)
            
            # ---------
            if str(row).find('[27]') != -1:
                str_CT27 = get_Input_data(file, row= idx, column=19)
            if str(row).find('[28]') != -1:
                str_CT28 = get_Input_data(file, row= idx, column=19)

            # --------- 
            if str(row).find('[30]') != -1:
                str_CT30 = get_Input_data(file, row= idx, column=19)
            if str(row).find('[31]') != -1:
                str_CT31 = get_Input_data(file, row= idx, column=19)
              
            # ---------
            if str(row).find('[33]') != -1:
                str_CT33 = get_Input_data(file, row= idx, column=19)
            if str(row).find('[34]') != -1:
                str_CT34 = get_Input_data(file, row= idx, column=19)  


        # str_CT21 =0
        ele_CT21 = '//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td[5]/input'
        sendkeys_Input(driver, ele_CT21, str_CT21)
        # time.sleep(1)

        # str_CT22 =0
        ele_CT22 = '//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[3]/td[4]/input'
        sendkeys_Input(driver, ele_CT22, str_CT22)
        time.sleep(1)

        # str_CT24 =0
        ele_CT24 = '//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[5]/td[5]/input'
        sendkeys_Input(driver, ele_CT24, str_CT24)
        # time.sleep(1)

        # str_CT25 =0
        ele_CT25 = '//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[6]/td[5]/input'
        sendkeys_Input(driver, ele_CT25, str_CT25)
        time.sleep(1)

        # str_CT27 =0
        ele_CT27 = '//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[8]/td[5]/input'
        sendkeys_Input(driver, ele_CT27, str_CT27)
        # time.sleep(1)

        # str_CT28 =0
        ele_CT28 = '//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[9]/td[5]/input'
        sendkeys_Input(driver, ele_CT28, str_CT28)
        time.sleep(1)

        # str_CT30 =0
        ele_CT30 = '//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[11]/td[5]/input'
        sendkeys_Input(driver, ele_CT30, str_CT30)  
        time.sleep(1)

        # str_CT31 =0
        ele_CT31 = '//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[12]/td[5]/input'
        sendkeys_Input(driver, ele_CT31, str_CT31)  
        time.sleep(1)

        # str_CT33 =0
        ele_CT33 = '//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[14]/td[5]/input'
        sendkeys_Input(driver, ele_CT33, str_CT33)   
        time.sleep(1)

        # str_CT34 =0
        ele_CT34 = '//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[15]/td[5]/input'
        sendkeys_Input(driver, ele_CT34, str_CT34)   
        time.sleep(1)

        # str_CT35 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[16]/td[5]/input')
        # str_CT35.click()
        # str_CT35.clear()
        # str_CT35.send_keys('0') 
        # time.sleep(1)

        # str_CT36 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[17]/td[5]/input')
        # str_CT36.click()
        # str_CT36.clear()
        # str_CT36.send_keys('0') 
        # time.sleep(1)
        
        btn_Luubannhap = driver.find_element_by_xpath('//*[@class="btn_type1 awesome" and @value="Lưu bản nháp"]')
        btn_Luubannhap.click()
        time.sleep(1)
        alert = Alert(driver)
        if str(alert.text).strip() == 'Có lưu bản nháp không?':
            alert.accept()
        time.sleep(1)

        driver.switch_to.default_content()
        time.sleep(2)
        btn_Dangxuat = driver.find_element_by_xpath('//*[@class="banner"]/div[3]/span/strong/a')
        btn_Dangxuat.click()
        
        if str(alert.text).strip() == 'Quý khách có muốn đăng xuất khỏi dịch vụ?':
            
            alert.accept()
        time.sleep(1)

    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
        return False, "THÔNG TIN KÊ KHAI CÓ LỖI"
    return True, "KÊ KHAI THÀNH CÔNG"

def move_file(file_input, path_Move_input, file_name):
    "move output"
    try:
        if not os.path.exists(path_Move_input+"\\"):
            os.makedirs(path_Move_input+"\\")

        shutil.move(file_input, path_Move_input+"\\" + file_name+".xlsx")
        return True
    except Exception as e :
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
        return False

def get_Input_data(path, row , column):
    "Read file execl input"

    try:
        import sys, os
        import re
        import shutil
        import win32com.client as win32

        xlApp =win32.dynamic.Dispatch("Excel.Application")
        xlApp.DisplayAlerts = False

        xlwb = xlApp.Workbooks.Open(path, True, False, None)
        xlSheet = xlwb.Worksheets('Declaration (EN)')
        value =  xlSheet.cells(row+2,column+1).value

    except:   
        MODULE_LIST = [m.__name__ for m in sys.modules.values()]
        for module in MODULE_LIST:
            if re.match(r'win32com\.gen_py\..+', module):
                del sys.modules[module]

        shutil.rmtree(os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py'))
        
        xlApp =win32.dynamic.Dispatch("Excel.Application")
        xlApp.DisplayAlerts = False

        xlwb = xlApp.Workbooks.Open(path, True, False, None)
        xlSheet = xlwb.Worksheets('Declaration (EN)')
        value =  xlSheet.cells(row+2,column+1).value

    xlwb.Close(True)
    del xlApp
    return round(value)


def get_Report_file(list_Claim_Company, id_client, access_token_terra):
    'Download file input execl'
    import requests
    rq_get_ReportPits_terra = get_ReportPits(id_client,access_token_terra)
    list_ReportPits = rq_get_ReportPits_terra['data']['reportPits']['data']
    

    #For từng hồ sơ để xử lý
    for i_ReportPits in list_ReportPits:
        for i_Claim_Company in list_Claim_Company:
            if i_ReportPits['id'] == i_Claim_Company['name_claim']:

                path_input = i_ReportPits["path"]
                local_filename = path_input.split('?')[0].split('/')[-1]
                r = requests.get(path_input)

                time.sleep(1)
                f = open(CurDir+"\\input\\"+local_filename, 'wb')
                for chunk in r.iter_content(chunk_size=512 * 1024): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                f.close()

def path_input():
    "Check folder input" 
    path_folder_input = glob.glob(os.path.abspath(CurDir+"\\input") + "\\*.xlsx")
    return path_folder_input


def job_backup():
    LOG_INFO("CHẠY QUY TRÌNH BACKUP")
    from datetime import datetime
    from pathlib import Path
    import zipfile


    OBJECT_TO_BACKUP_1 = data_config['path_service']+"//db.sqlite3"  # The file or directory to backup
    OBJECT_TO_BACKUP_2 = CurDir+"//logs_pj-vpo_robot.txt"  # The file or directory to backup
    BACKUP_DIRECTORY = data_config['thu_muc_backup']  # The location to store the backups in
    MAX_BACKUP_AMOUNT = 90  # The maximum amount of backups to have in BACKUP_DIRECTORY


    object_to_backup_path = Path(OBJECT_TO_BACKUP_1)
    object_to_backup_path_2 = Path(OBJECT_TO_BACKUP_2)
    backup_directory_path = Path(BACKUP_DIRECTORY)
    assert object_to_backup_path.exists()   # Validate the object we are about to backup exists before we continue

    # Validate the backup directory exists and create if required
    backup_directory_path.mkdir(parents=True, exist_ok=True)

    # Get the amount of past backup zips in the backup directory already
    existing_backups = [
        x for x in backup_directory_path.iterdir()
        if x.is_file() and x.suffix == '.zip' and x.name.startswith('backup-')
    ]

    # Enforce max backups and delete oldest if there will be too many after the new backup
    oldest_to_newest_backup_by_name = list(sorted(existing_backups, key=lambda f: f.name))
    while len(oldest_to_newest_backup_by_name) >= MAX_BACKUP_AMOUNT:  # >= because we will have another soon
        backup_to_delete = oldest_to_newest_backup_by_name.pop(0)
        backup_to_delete.unlink()

    # Create zip file (for both file and folder options)
    backup_file_name = f'backup-{datetime.now().strftime("%Y%m%d%H%M%S")}.zip'
    LOG_INFO(backup_file_name)
    zip_file = zipfile.ZipFile(str(backup_directory_path / backup_file_name), mode='w')

    if object_to_backup_path.is_file():
        # If the object to write is a file, write the file
        zip_file.write(
            object_to_backup_path.absolute(),
            arcname=object_to_backup_path.name,
            compress_type=zipfile.ZIP_DEFLATED
        )

    elif object_to_backup_path.is_dir():
        # If the object to write is a directory, write all the files
        for file in object_to_backup_path.glob('**/*'):
            if file.is_file():
                zip_file.write(
                    file.absolute(),
                    arcname=str(file.relative_to(object_to_backup_path)),
                    compress_type=zipfile.ZIP_DEFLATED
                )

    if object_to_backup_path_2.is_file():
        # If the object to write is a file, write the file
        zip_file.write(
            object_to_backup_path_2.absolute(),
            arcname=object_to_backup_path_2.name,
            compress_type=zipfile.ZIP_DEFLATED
        )

    elif object_to_backup_path_2.is_dir():
        # If the object to write is a directory, write all the files
        for file in object_to_backup_path_2.glob('**/*'):
            if file.is_file():
                zip_file.write(
                    file.absolute(),
                    arcname=str(file.relative_to(object_to_backup_path_2)),
                    compress_type=zipfile.ZIP_DEFLATED
                )
    
    # Close the created zip file
    zip_file.close()

def process_backup():
    LOG_INFO("BACKUP")
    schedule.every().day.at(data_config['thoi_gian_backup']).do(job_backup)

    while True:
        schedule.run_pending()
        time.sleep(1)

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

if __name__ == "__main__":

    import datetime
    import schedule
    import time
    import shutil

    LOG_INFO("BẮT ĐẦU CHẠY")
    thread_device = thread_with_trace(target=process_backup)
    thread_device.start()
    if data_config['lien_tuc'] == True:
        while True:
            job_kekhai()
            job_tracuu()
    else:
        schedule.every().day.at(data_config['che_do_ke_khai']['thoi_gian_co_dinh']).do(job_kekhai)
        schedule.every().day.at(data_config['che_do_quet_ket_qua']['thoi_gian_co_dinh']).do(job_tracuu)

    while True:
        schedule.run_pending()
        time.sleep(1)
