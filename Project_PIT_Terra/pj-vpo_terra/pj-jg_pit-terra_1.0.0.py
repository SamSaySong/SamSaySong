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
import ocr_capcha
import shutil
import threading
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

path_img = os.path.abspath(CurDir +"\\capcha")
path_chrome = os.path.abspath(CurDir +"\\chromedriver.exe")
data_security_1 = 'leader_test'
data_security_2 = '123456'
data_security_3 = '000000'
path_Download = CurDir + '\\input'

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
FileHandler = logging.FileHandler(name_Logs, 'a+', 'utf-8')
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



# ------ API ---------

def login_terra():
    import requests
    import json
    url = 'https://uat-api.vina-payroll.com/graphql'
    payload="{\"query\":\"mutation login ($username: String!, $password: String!, $client_code: String) {\\n    login (username: $username, password: $password, client_code: $client_code) {\\n        access_token\\n        refresh_token\\n        expires_in\\n        token_type\\n    }\\n}\",\"variables\":{\"username\":\""+data_security_1+"\",\"password\":\""+data_security_2+"\",\"client_code\":\""+data_security_3+"\"}}"
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def get_clients_terra(access_token_terra):
    import requests
    import json
    url = 'https://uat-api.vina-payroll.com/graphql'
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

    url = "https://uat-api.vina-payroll.com/graphql"

    payload="{\"query\":\"query getReportPits($perPage: Int!, $page: Int, $orderBy: [ReportPitsOrderByOrderByClause!], $where: ReportPitsWhereWhereConditions) {\\r\\n  reportPits(orderBy: $orderBy, where: $where, first: $perPage, page: $page) {\\r\\n    paginatorInfo {\\r\\n      count\\r\\n      currentPage\\r\\n      firstItem\\r\\n      hasMorePages\\r\\n      lastItem\\r\\n      lastPage\\r\\n      perPage\\r\\n      total\\r\\n      __typename\\r\\n    }\\r\\n    data {\\r\\n      id\\r\\n      name\\r\\n      date_from_to\\r\\n      form_data\\r\\n      client_id\\r\\n      status\\r\\n      created_at\\r\\n      updated_at\\r\\n      path\\r\\n      __typename\\r\\n    }\\r\\n    __typename\\r\\n  }\\r\\n}\\r\\n\",\"variables\":{\"perPage\":100,\"page\":1,\"orderBy\":[{\"field\":\"NAME\",\"order\":\"ASC\"}],\"where\":{\"AND\":[{\"column\":\"CLIENT_ID\",\"operator\":\"EQ\",\"value\":\""+id_client+"\"}]}}}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    return response.json()

# -----------------------
def get_service(id_client):
    import requests
    payload = ""
    url = "http://192.168.1.64:8000"+"/claim/?company_claim="+str(id_client)
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1'
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def post_service(payload):
    import requests
    import json

    url = "http://192.168.1.64:8000"+"/claim/"
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

    url ="http://192.168.1.64:8000"+"/claim/"+str(id)+"/"
    payload = json.dumps(payload)
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1',
    'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    return response.json()


url_Thuedoanhnghiep = 'https://thuedientu.gdt.gov.vn/etaxnnt/Request?&dse_sessionId=opLE55FV2bAnltX5V-tNM3S&dse_applicationId=-1&dse_pageId=1&dse_operationName=corpIndexProc&dse_errorPage=error_page.jsp&dse_processorState=initial&dse_nextEventName=start'

# def open_driver():

#     options = Options()
#     prefs = {"credentials_enable_service": False,  
#     "profile.password_manager_enabled": False ,  # tắt arlert save password chrome
#     "profile.default_content_settings.popups": 0,
#     "download.default_directory": "", # IMPORTANT - ENDING SLASH V IMPORTANT
#     "download.prompt_for_download": False,
#     "directory_upgrade": True,
#     "safebrowsing.enabled": True}
#     options.add_experimental_option('prefs', prefs)
#     options.add_argument('--safebrowsing-disable-download-protection')
#     options.add_argument("--no-sandbox") 
#     options.add_argument("--start-maximized") 
#     options.add_argument("--disable-dev-shm-usage") 
#     options.add_argument("--disable-web-security")
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option('useAutomationExtension', False)
#     options.add_argument('disable-infobars')
#     options.add_argument("--disable-extensions")
#     options.add_argument("--ignore-ssl-errors=yes")
#     options.add_argument("--allow-insecure-localhost")
#     options.add_argument('ignore-certificate-errors') ## fixx ssl
#     options.add_argument("--disable-blink-features")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
#     # options.add_argument("--allow-running-insecure-content")
#     # options.add_argument("--headless") 
#     driver = webdriver.Chrome(executable_path= path_chrome, options=options)

#     return driver



from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver
import time

access_token_terra = ""
def attach_to_session(executor_url, session_id):

    original_execute = WebDriver.execute
    def new_command_execute(self,command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self,command, params)

    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
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

def login(driver, user_name, pass_word):

    try:
        driver.get(url_Thuedoanhnghiep)
        try:
            if check_element(driver, '//*[@class="banner"]/div[3]/span/strong/a',5) == True:
                btn_Dangxuat = driver.find_element_by_xpath('//*[@class="banner"]/div[3]/span/strong/a')
                btn_Dangxuat.click()
                alert = Alert(driver)
                # Check alert logout
                if (alert.text).strip() == 'Quý khách có muốn đăng xuất khỏi dịch vụ?':
                    alert.accept()
                    ele_Dangxuat = driver.find_element_by_xpath('//*[@class="dangnhap"]/span/strong/a')
                    ele_Dangxuat.click()
        except:
            pass

        # Screen Thue Dien Tu
        btn_Doanhnghiep = driver.find_element_by_xpath("//*[@class='khungbaolongin']/div[2]/div/div[2]").click()
        time.sleep(2)

        # Screen Login form
        btn_Login_form = driver.find_element_by_xpath("//*[@class='banner']/div[3]/span[2]/button").click()
        time.sleep(2)

        while True:
            try:
                input_User = driver.find_element_by_xpath('//*[@id="_userName"]')
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
                    return False

                time.sleep(3)
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
                
                elif check_element(driver, '//*[@class="banner"]/div[2]/div[2]/div/span[1]', 5) == True :
                    LOG_INFO("DANG NHAP THANH CONG")
                    return True

            except Exception as e:
                LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))
                return False

    except Exception as e:      
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))
        return False
         
def main():
    'cty -> rp -> input'

    print("CHẠY QUY TRÌNH KÊ KHAI")
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
                    if i_ReportPits['status'] == "completed" :
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
                    # Download file input
                    get_Report_file(list_Claim_Company)

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
                                # get 1 func == list data input------
                                df_input = pd.read_excel(file, sheet_name="Declaration (EN)", engine='openpyxl', dtype=object)
                                for idx, row in df_input.iterrows():
                                    print(df_input)
                                    
                                try:
                                    driver = attach_to_session('http://127.0.0.1:62901', 'da60234d3314c1a1b4e392379efabbbf')
                                    if login(driver, user_name='0109411417-ql', pass_word='123456aA@') == False:
                                        LOG_INFO('dang nhap k thanh cong: send mail')
                                    thu_tuc(driver)
                                    time.sleep(1)
                                    job_kekhai, str_STT = ke_khai(driver)
                                    if job_kekhai == True:
                                        input_data_claim = data_claim.copy()
                                        del input_data_claim['id']
                                        del input_data_claim['created_at']
                                        del input_data_claim['__typename']
                                        del input_data_claim['updated_at']
                                        # print(input_data_claim)
                                        
                                        data_input = {}
                                        data_input['id'] = data_claim['id']
                                        data_input['input'] = input_data_claim
                                        data_input['input']['state'] = "da_ke_khai_ho_so"
                                        data_input['input']['ngay_ke_khai_va_luu_tam_ho_so'] = datetime.datetime.now().strftime("%Y-%m-%d")
                                        # print(data_input)

                                        print(patch_service(i_Claim_Company['id'],{"status_claim":"Running", "note_claim":str(str_STT), "status_process_claim": "Đã kê khai và lưu tạm hồ sơ"}))
                                        LOG_INFO("HỒ SƠ LƯU TẠM "+str(str_STT)+" CẬP NHẬT LƯU TRỮ")

                                    else:
                                        patch_service(i_Claim_Company['id'],{"status_claim":"Error","note_claim":str(str_STT)})
                                        LOG_INFO("HỒ SƠ BỊ LỖI")
                                        print('Thong tin ke khai co loi: Send mail') 
                                        
                                
                                except Exception as e:
                                    print('Send mail')
                                    LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))
                                    patch_service(i_Claim_Company['id'],{"status_claim":"Error","note_claim":str(str_STT)})
                                # driver.quit()
        except Exception as e:
            print('Send mail')
            LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))

def thu_tuc(driver):

    select_xpath_submenu(driver, xpath_menu='//*[@id="ddtabs1"]/ul/li[3]/a', xpath_submenu= '//*[@class="submenuEpay"]/div/div[3]/ul/li[*]/a', input_option='Kê khai trực tuyến', timeout= 5)
    time.sleep(3)

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
    select_xpath_options(driver, xpath_select_Loaitokhai, xpath_option_Loaitokhai, input_option='Tờ khai chính thức')
    time.sleep(1)

    # Ky ke khai 
    xpath_select_Kykekhai = '//*[@id="LapTKhaiOnlineForm"]/table/tbody/tr/td/table/tbody/tr[4]/td/select'
    xpath_option_Kykekhai = '//*[@id="LapTKhaiOnlineForm"]/table/tbody/tr/td/table/tbody/tr[4]/td/select/option'

    if len(driver.find_elements_by_xpath(xpath_option_Kykekhai)) == 4:
        # Check screen ke khai theo quy
        select_xpath_options(driver, xpath_select_Kykekhai, xpath_option_Kykekhai,input_option="Q4")

    elif len(driver.find_elements_by_xpath(xpath_option_Kykekhai)) == 12:
        # Check screen ke khai theo thang
        select_xpath_options(driver, xpath_select_Kykekhai, xpath_option_Kykekhai, input_option="12")
    time.sleep(1)

    input_Namkekhai = driver.find_element_by_xpath('//*[@id="LapTKhaiOnlineForm"]/table/tbody/tr/td/table/tbody/tr[4]/td/input[2]')
    input_Namkekhai.click()
    input_Namkekhai.clear()
    input_Namkekhai.send_keys("2021")

    button_Tieptuc = driver.find_element_by_xpath('//*[@id="tieptucBT"]')
    button_Tieptuc.click()
    time.sleep(1)

    # Đã có tờ khai chính thức được chấp nhận. Bạn phải nộp tờ khai bổ sung.
    if check_element(driver,'//*[@class="box_common_content"]/b/span',5) == True:
        print(driver.find_element_by_xpath('//*[@class="box_common_content"]/b/span').text)


def ke_khai(driver):
    "Screen form Ke khai"

    try:
        str_CT21 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[2]/td[5]/input')
        str_CT21.click()
        str_CT21.clear()
        str_CT21.send_keys('0')
        time.sleep(1)

        str_CT22 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[3]/td[4]/input')
        str_CT22.click()
        str_CT22.clear()
        str_CT22.send_keys('0')
        time.sleep(1)

        str_CT24 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[5]/td[5]/input')
        str_CT24.click()
        str_CT24.clear()
        str_CT24.send_keys('0')   
        time.sleep(1)

        str_CT25 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[6]/td[5]/input')
        str_CT25.click()
        str_CT25.clear()
        str_CT25.send_keys('0')    
        time.sleep(1)

        str_CT27 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[8]/td[5]/input')
        str_CT27.click()
        str_CT27.clear()
        str_CT27.send_keys('0')    
        time.sleep(1)

        str_CT28 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[9]/td[5]/input')
        str_CT28.click()
        str_CT28.clear()
        str_CT28.send_keys('0')   
        time.sleep(1)

        str_CT30 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[11]/td[5]/input')
        str_CT30.click()
        str_CT30.clear()
        str_CT30.send_keys('0')    
        time.sleep(1)

        str_CT31 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[12]/td[5]/input')
        str_CT31.click()
        str_CT31.clear()
        str_CT31.send_keys('0')    
        time.sleep(1)

        str_CT33 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[14]/td[5]/input')
        str_CT33.click()
        str_CT33.clear()
        str_CT33.send_keys('0') 
        time.sleep(1)

        str_CT34 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[15]/td[5]/input')
        str_CT34.click()
        str_CT34.clear()
        str_CT34.send_keys('0') 
        time.sleep(1)

        str_CT35 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[16]/td[5]/input')
        str_CT35.click()
        str_CT35.clear()
        str_CT35.send_keys('0') 
        time.sleep(1)

        str_CT36 = driver.find_element_by_xpath('//*[@id="div_tkhai"]/table[2]/tbody/tr/td/div/table/tbody/tr[17]/td[5]/input')
        str_CT36.click()
        str_CT36.clear()
        str_CT36.send_keys('0') 
        time.sleep(1)
        
        btn_Luubannhap = driver.find_element_by_xpath('//*[@class="btn_type1 awesome" and @value="Lưu bản nháp"]')
        time.sleep(3)
        # btn_Luubannhap.click()
        try:
            alert = Alert(driver)
            if str(alert.text).strip() == 'Có lưu bản nháp không?':
                alert.accept()
            driver.switch_to.default_content()
            time.sleep(2)
            btn_Dangxuat = driver.find_element_by_xpath('//*[@class="banner"]/div[3]/span/strong/a')
            btn_Dangxuat.click()
            
            if str(alert.text).strip() == 'Quý khách có muốn đăng xuất khỏi dịch vụ?':
                print(alert.text)
                alert.accept()
        except:
            pass

    except Exception as e:
        print('có lỗi')
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
        return False, "Kê khai có lỗi"
    return True, "Kê khai thành công"


def get_Report_file(list_Claim_Company):
    import requests
    for i_Claim_Company in list_Claim_Company:

        path_input = i_Claim_Company["data_claim"]["path"]
        local_filename = path_input.split('?')[0].split('/')[-1]
        r = requests.get(path_input)
        f = open(CurDir+"\\input\\"+local_filename, 'wb')
        for chunk in r.iter_content(chunk_size=512 * 1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
        f.close()

def path_input():
    "Check folder input" 
    path_folder_input = glob.glob(os.path.abspath(CurDir+"\\input") + "\\*.xlsx")
    # print(path_folder_input)
    return path_folder_input

if __name__ == "__main__":   
    s = time.perf_counter()
   
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} Thời gian chạy trong {elapsed:0.2f} giây.")