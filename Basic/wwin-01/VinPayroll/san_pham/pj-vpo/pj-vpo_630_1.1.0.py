import enum
import os
import inspect
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.action_chains import ActionChains
import shutil
import json
import regex
import cv2
import numpy as np
from unidecode import unidecode
import datetime
# ua = UserAgent()
import mysql.connector
import requests
import sys 
import threading
from mysql.connector.locales.eng import client_error




CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
import logging
global LOG_INFO
name_Organization = "vpo"
name_Robot = "630"
name_Version = "1.1.0"
name_Config = "config_pj-vpo_robot.json"
name_Logs = "logs_pj-vpo_robot.txt"


logging.basicConfig(format='------------------ %(asctime)s >>>  %(message)s  <<<------------------', datefmt='%d/%m/%Y %H:%M:%S')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s",datefmt='%d/%m/%Y %H:%M:%S')
LOG_INFO = logging.warning
LOG_ERROR = logging.error
FileHandler = logging.FileHandler(name_Logs, 'a+', 'utf-8')
FileHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(FileHandler)
access_token_terra = ""

# --- HÀM HỖ TRỢ ---
def readJson(str_Path):
    #!/usr/bin/env python
    import chardet # $ pip install chardet
    
    # detect file encoding
    with open(str_Path, 'rb') as data_file:
        raw = data_file.read(32) # at most 32 bytes are returned
        encoding = chardet.detect(raw)['encoding']
    with open(str_Path, encoding=encoding) as data_file:
        data = json.loads(data_file.read())
    return data

data_config = readJson(CurDir+"\\conf\\"+name_Config)
data_security = readJson(CurDir+"\\conf\\config_pj-vpo_security")
mydb = mysql.connector.connect(
  host=data_security['host_mysql'],
  user=data_security['user_mysql'],
  passwd=data_security['passwd_mysql'],
  database=data_security['database_mysql']
)

mycursor = mydb.cursor()


def process_captcha(path_image):
    url = data_config['url_service']+"/detail"
    files = {'media': open(path_image, 'rb')}
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1'
    }
    response = requests.request("POST", url, headers=headers, files=files)
    return response.json()

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


def save(encoded_data, filename):
    import base64
    data = regex.sub(r'data:image/png;base64,','',encoded_data).replace(' ', '+')
    imgdata = base64.b64decode(data)
    with open(filename, 'wb') as f:
            f.write(imgdata)

def open_brower():
    ''' CACH 1 '''
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("user-data-dir="+CurDir+"\\UserData\\TuNA")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-automation")
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-javascript")
    # chrome_options.add_argument("--disable-web-security")
    # chrome_options.add_argument("--allow-running-insecure-content")
    # chrome_options.add_argument("user-agent="+ua.chrome)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) # tắt popup của face
    chrome_options.add_experimental_option("useAutomationExtension", False) 
    prefs = {"credentials_enable_service": False,
            "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    executable_path = "/webdrivers"
    os.environ["webdriver.chrome.driver"] = executable_path
    driver = webdriver.Chrome(executable_path=os.path.abspath(CurDir+"\\chromedriver.exe"), chrome_options=chrome_options)
    driver.maximize_window()
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
            time.sleep(1)

def check_selector_element(driver,selector,int_Timeout=60):
    int_Count = 0
    while True:
        try:
            driver.find_element_by_css_selector(selector)
            return True
        except:
            if int_Count == int_Timeout:
                return False
            int_Count+=1
            time.sleep(1)


def select_xpath_options_bodau(driver,xpath_select,xpath_options,input_option,timeout=1):
    
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(xpath_select))
    time.sleep(timeout)
    for i in driver.find_elements_by_xpath(xpath_options):
        # print(regex.sub(r'\s','_',str(unidecode(i.text)).lower().strip()))
        # print(regex.sub(r'\s','_',str(unidecode(input_option)).lower().strip()))
        if regex.sub(r'\s','_',str(unidecode(i.text)).lower().strip()) == regex.sub(r'\s','_',str(unidecode(input_option)).lower().strip()):
            # print(i.text)
            driver.execute_script("arguments[0].click();", i)
            break

def select_selector_options(driver,selector_select,selector_options,input_option,timeout=1):
    driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector(selector_select))
    time.sleep(timeout)
    for i in driver.find_elements_by_xpath(selector_options):
        # print(i.text)
        if str(i.text).strip() == str(input_option).strip():
            # print(i.text)
            driver.execute_script("arguments[0].click();", i)
            break

def select_selector_options_bodau(driver,selector_select,selector_options,input_option,timeout=1):
    driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector(selector_select))
    time.sleep(timeout)
    for i in driver.find_elements_by_xpath(selector_options):
        # print(regex.sub(r'\s','_',str(unidecode(i.text)).lower().strip()))
        # print(regex.sub(r'\s','_',str(unidecode(input_option)).lower().strip()))
        if regex.sub(r'\s','_',str(unidecode(i.text)).lower().strip()) == regex.sub(r'\s','_',str(unidecode(input_option)).lower().strip()):
            # print(i.text)
            driver.execute_script("arguments[0].click();", i)
            break

def convert_datetime_string(data_input,format_input='%Y-%m-%d',format_output='%d/%m/%Y'):
    data_date = datetime.datetime.strptime(data_input, format_input)
    data_date = data_date.strftime(format_output)
    return data_date

def select_xpath_options(driver,xpath_select,xpath_options,input_option,timeout=1):
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(xpath_select))
    time.sleep(timeout)
    for i in driver.find_elements_by_xpath(xpath_options):
        # print(i.text)
        if str(i.text).strip() == str(input_option).strip():
            # print(i.text)
            driver.execute_script("arguments[0].click();", i)
            break

def select_xpath_options_contains(driver,xpath_select,xpath_options,input_option,timeout=1):
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(xpath_select))
    time.sleep(timeout)
    for i in driver.find_elements_by_xpath(xpath_options):
        # print(i.text)
        if str(input_option).lower().strip() in str(i.text).lower().strip():
            # print(i.text)
            driver.execute_script("arguments[0].click();", i)
            break

def select_xpath_options_contains_bodau(driver,xpath_select,xpath_options,input_option,timeout=1):
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(xpath_select))
    time.sleep(timeout)
    for i in driver.find_elements_by_xpath(xpath_options):
        # print(i.text)
        if unidecode(str(input_option)).lower().strip() in unidecode(str(i.text)).lower().strip():
            # print(i.text)
            driver.execute_script("arguments[0].click();", i)
            break


# --- XỬ LÝ API ---

def get_service(id_client):
    import requests
    payload = ""
    url = data_config['url_service']+"/claim/?company_claim="+str(id_client)
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1'
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def post_service(payload):
    import requests
    import json

    url = data_config['url_service']+"/claim/"
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

    url = data_config['url_service']+"/claim/"+str(id)+"/"
    payload = json.dumps(payload)
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1',
    'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    return response.json()



def login_terra():
    import requests
    import json
    url = data_config['url_terra']
    payload="{\"query\":\"mutation login ($username: String!, $password: String!, $client_code: String) {\\n    login (username: $username, password: $password, client_code: $client_code) {\\n        access_token\\n        refresh_token\\n        expires_in\\n        token_type\\n    }\\n}\",\"variables\":{\"username\":\""+data_security['username_terra']+"\",\"password\":\""+data_security['password_terra']+"\",\"client_code\":\""+data_security['code_terra']+"\"}}"
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def get_clients_terra(access_token_terra):
    import requests
    import json
    url = data_config['url_terra']
    payload="{\"query\":\"query getWithAssignments($perPage: Int!, $page: Int, $orderBy: [ClientsOrderByOrderByClause!], $where: ClientsWhereWhereConditions) {\\n  clients(orderBy: $orderBy, where: $where, first: $perPage, page: $page) {\\n    paginatorInfo {\\n      count\\n      currentPage\\n      firstItem\\n      hasMorePages\\n      lastItem\\n      lastPage\\n      perPage\\n      total\\n      __typename\\n    }\\n    data {\\n      ...clientFields\\n      assignedInternalEmployees {\\n        id\\n        name\\n        code\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment clientFields on Client {\\n  id\\n  code\\n  company_name\\n  company_contact_phone\\n  company_contact_email\\n  address\\n  company_bank_account\\n  company_account_number\\n  company_bank_name\\n  company_bank_branch\\n  person_signing_a_bank_document\\n  employees_number_foreign\\n  employees_number_vietnamese\\n  rewards_for_achievements\\n  annual_salary_bonus\\n  social_insurance_and_health_insurance_ceiling\\n  unemployment_insurance_ceiling\\n  payroll_creator\\n  payroll_approver\\n  social_insurance_agency\\n  social_insurance_account_name\\n  social_insurance_account_number\\n  social_insurance_bank_name\\n  social_insurance_bank_branch\\n  social_insurance_unit_code\\n  trade_union_agency\\n  trade_union_account_name\\n  trade_union_account_number\\n  trade_union_bank_name\\n  trade_union_bank_branch\\n  presenter_phone\\n  company_contact_fax\\n  presenter_email\\n  presenter_name\\n  company_license_no\\n  company_license_issuer\\n  company_license_issued_at\\n  company_license_updated_at\\n  company_license_at\\n  timesheet_min_time_block\\n  day_payroll_start\\n  day_payroll_end\\n  type_of_business\\n  clientWorkflowSetting {\\n    id\\n    client_id\\n    enable_overtime_request\\n    enable_leave_request\\n    enable_early_leave_request\\n    enable_timesheet_input\\n    enable_social_security_manage\\n    enable_salary_payment\\n    manage_user\\n    enable_wifi_checkin\\n    enable_training_seminar\\n    enable_recruit_function\\n    enable_contract_reminder\\n    __typename\\n  }\\n  created_at\\n  updated_at\\n  is_active\\n  __typename\\n}\\n\",\"variables\":{\"perPage\":30,\"page\":1,\"orderBy\":[{\"field\":\"COMPANY_NAME\",\"order\":\"ASC\"}],\"where\":{}}}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def get_socialSecurityClaims_terra(id_client,access_token_terra):
    import requests
    import json
    url = data_config['url_terra']
    payload="{\"query\":\"query get($perPage: Int!, $page: Int, $orderBy: [SocialSecurityClaimsOrderByOrderByClause!], $where: SocialSecurityClaimsWhereWhereConditions) {\\n  socialSecurityClaims(orderBy: $orderBy, where: $where, first: $perPage, page: $page) {\\n    paginatorInfo {\\n      count\\n      currentPage\\n      firstItem\\n      hasMorePages\\n      lastItem\\n      lastPage\\n      perPage\\n      total\\n      __typename\\n    }\\n    data {\\n      ...socialSecurityClaimFields\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment socialSecurityClaimFields on SocialSecurityClaim {\\n  id\\n  client_id\\n  client_employee_id\\n  clientEmployee {\\n    code\\n    full_name\\n    __typename\\n  }\\n  state\\n  client_approved\\n  social_insurance_number\\n  claimed_amount\\n  reason\\n  note\\n  cd_claim_bao_hiem\\n  cd_claim_bao_hiem_sub\\n cd_claim_bao_hiem_sub_sub\\n  cd_claim_bh_tu_ngay\\n  cd_claim_bh_den_ngay\\n  cd_claim_bh_tong_so_ngay_nghi\\n  cd_om_dau_ten_benh\\n  cd_om_dau_tuyen_benh_vien\\n  cd_om_dau_benh_dai_ngay\\n  cd_thai_san_ngay_sinh_con\\n  cd_thai_san_phau_thuat_thai_duoi_32t\\n  cd_thai_san_nghi_duong_thai\\n  cd_thai_san_ngay_nhan_con_nuoi\\n  cd_thai_san_tuoi_thai\\n  cd_thai_san_bien_phap_tranh_thai\\n  cd_thai_san_dieu_kien_sinh_con\\n  cd_thai_san_dieu_kien_khi_kham_thai\\n  cd_thai_san_cha_nghi_cham_con\\n  cd_thai_san_ngay_di_lam_thuc_te\\n  cd_thai_san_ngay_con_chet\\n  cd_thai_san_so_con_chet_khi_sinh\\n  cd_thai_san_ngay_me_chet\\n  cd_thai_san_ngay_ket_luan\\n  ds_ph_suc_khoe_ngay_tro_lai_lam_viec\\n  ds_ph_suc_khoe_ngay_dam_dinh\\n  tinh_trang_chung_tu_lien_quan\\n  ttgqhs_ngay_nop_ho_so\\n  ttgqhs_ngay_hen_tra_ket_qua\\n  ttgqhs_so_ho_so_bhxh_da_ke_khai\\n  ttgqhs_tong_so_ngay_duoc_tinh_huong_tro_cap\\n  ttgqhs_so_tien_duoc_huong\\n  rejected_comment\\n  created_at\\n  updated_at\\n  __typename\\n}\\n\",\"variables\":{\"perPage\":10,\"page\":1,\"orderBy\":[{\"field\":\"CREATED_AT\",\"order\":\"DESC\"}],\"where\":{\"AND\":[{\"column\":\"CLIENT_ID\",\"operator\":\"EQ\",\"value\":\""+id_client+"\"}]}}}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def update_socialSecurityClaims_terra(data_input,access_token_terra):
    import requests
    import json
    data_input = json.dumps(data_input)
    url = data_config['url_terra']
    payload="{\"query\":\"mutation updateSocialSecurityClaim ($id: ID!, $input: SocialSecurityClaimInput) {\\n    updateSocialSecurityClaim (id: $id, input: $input) {\\n        id\\n        client_id\\n        client_employee_id\\n        state\\n        client_approved\\n        social_insurance_number\\n        claimed_amount\\n        reason\\n        cd_claim_bao_hiem\\n        cd_claim_bao_hiem_sub\\n    cd_claim_bao_hiem_sub_sub\\n    cd_claim_bh_tu_ngay\\n        cd_claim_bh_den_ngay\\n        cd_claim_bh_tong_so_ngay_nghi\\n        cd_om_dau_ten_benh\\n        cd_om_dau_tuyen_benh_vien\\n        cd_om_dau_benh_dai_ngay\\n        cd_thai_san_ngay_sinh_con\\n        cd_thai_san_phau_thuat_thai_duoi_32t\\n        cd_thai_san_nghi_duong_thai\\n        cd_thai_san_ngay_nhan_con_nuoi\\n        cd_thai_san_tuoi_thai\\n        cd_thai_san_bien_phap_tranh_thai\\n        cd_thai_san_dieu_kien_sinh_con\\n        cd_thai_san_dieu_kien_khi_kham_thai\\n        cd_thai_san_cha_nghi_cham_con\\n        cd_thai_san_ngay_di_lam_thuc_te\\n        cd_thai_san_ngay_con_chet\\n        cd_thai_san_so_con_chet_khi_sinh\\n        cd_thai_san_ngay_me_chet\\n        cd_thai_san_ngay_ket_luan\\n        ds_ph_suc_khoe_ngay_tro_lai_lam_viec\\n        ds_ph_suc_khoe_ngay_dam_dinh\\n        tinh_trang_chung_tu_lien_quan\\n        ttgqhs_ngay_nop_ho_so\\n        ttgqhs_ngay_hen_tra_ket_qua\\n        ttgqhs_so_ho_so_bhxh_da_ke_khai\\n        ttgqhs_tong_so_ngay_duoc_tinh_huong_tro_cap\\n        ttgqhs_so_tien_duoc_huong\\n        rejected_comment\\n        note\\n        created_at\\n        updated_at\\n    }\\n}\",\"variables\":"+data_input+"}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()




def get_clientEmployee(id_clientEmployee,access_token_terra):
    import requests
    import json
    url = data_config['url_terra']
    payload="{\"query\":\"query find($id: ID!) {\\n  clientEmployee(id: $id) {\\n    ...clientEmployeeFields\\n    __typename\\n  }\\n}\\n\\nfragment clientEmployeeFields on ClientEmployee {\\n  id\\n  client_id\\n  full_name\\n  code\\n  probation_start_date\\n  probation_end_date\\n  official_contract_signing_date\\n  type_of_employment_contract\\n  salary\\n  allowance_for_responsibilities\\n  fixed_allowance\\n  is_tax_applicable\\n  is_insurance_applicable\\n  number_of_dependents\\n  bank_account\\n  bank_account_number\\n  bank_name\\n  bank_branch\\n  social_insurance_number\\n  date_of_birth\\n  sex\\n  department\\n  position\\n  title\\n  workplace\\n  marital_status\\n  salary_for_social_insurance_payment\\n  effective_date_of_social_insurance\\n  medical_care_hospital_name\\n  medical_care_hospital_code\\n  nationality\\n  nation\\n  id_card_number\\n  is_card_issue_date\\n  id_card_issue_place\\n  birth_place_address\\n  birth_place_street\\n  birth_place_wards\\n  birth_place_district\\n  birth_place_city_province\\n  contract_no\\n  resident_address\\n  resident_street\\n  resident_wards\\n  resident_district\\n  resident_city_province\\n  contact_address\\n  contact_street\\n  contact_wards\\n  contact_district\\n  contact_city_province\\n  contact_phone_number\\n  household_head_info\\n  household_code\\n  household_head_fullname\\n  household_head_id_card_number\\n  household_head_relation\\n  household_head_phone\\n  resident_record_number\\n  resident_record_type\\n  resident_village\\n  resident_commune_ward_district_province\\n  foreigner_job_position\\n  foreigner_contract_status\\n  education_level\\n  status\\n  role\\n  quitted_at\\n  user_id\\n  created_at\\n  updated_at\\n  work_schedule_group_template_id\\n  year_paid_leave_count\\n  currency\\n  mst_code\\n  career\\n  avatar_path\\n  avatar_path_large\\n  contracts {\\n    id\\n    contract_type\\n    contract_code\\n    contract_signing_date\\n    contract_end_date\\n    __typename\\n  }\\n  __typename\\n}\\n\",\"variables\":{\"id\":\""+id_clientEmployee+"\"}}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()





# --- XỬ LÝ CHÍNH ---

def logout_bhxh(driver):
    try:
        check_element(driver,'//*[@id="accountMenuBtn"]/span/span')
        btn_logout = driver.find_element_by_xpath('//*[@id="accountMenuBtn"]/span/span').click()
        time.sleep(2)
        btn_logout = driver.find_element_by_xpath('//*[@id="accountMenuBtn"]/span/span').click()
        check_element(driver,'//*[@id="header"]/div[1]/div/div/div[2]/div/div/div[2]/div/button')
        btn_logout = driver.find_element_by_xpath('//*[@id="header"]/div[1]/div/div/div[2]/div/div/div[2]/div/button').click()
    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        LOG_ERROR("LOGOUT_BHXH: Không tìm thấy nút!")

def login_bhxh(driver,str_username,str_password):
    driver.get("https://dichvucong.baohiemxahoi.gov.vn/")
    if check_element(driver,'//*[@id="accountMenuBtn"]',2):
        logout_bhxh(driver)

    check_element(driver,'//*[@id="content"]/div[1]/div/div/div[3]/div/ul/li[1]/a/img')
    btn_kekhai = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/div/div[3]/div/ul/li[1]/a/img').click()
    
    check_element(driver,'//*[@formcontrolname="username"]')
    checkbox_tochuc = driver.find_element_by_xpath('//*[@id="mat-checkbox-2"]/label/div').click()
    input_username = driver.find_element_by_xpath('//*[@formcontrolname="username"]').clear()
    input_username = driver.find_element_by_xpath('//*[@formcontrolname="username"]').send_keys(str_username.strip())
    input_password = driver.find_element_by_xpath('//*[@formcontrolname="password"]').clear()
    input_password = driver.find_element_by_xpath('//*[@formcontrolname="password"]').send_keys(str_password.strip())
    int_Count = 0
    while True:
        try:
            
            if int_Count >= 20:
                LOG_ERROR("LOGIN_BHXH: ERROR")
                return False
        
            data_captcha = driver.find_element_by_xpath('//*[@class="captcha-img"]/img').get_attribute("src")
            if "data" not in data_captcha:
                time.sleep(1)
                continue

            int_Count+=1

            save(data_captcha, CurDir+"\\tmp\\"+str_username+".png")
            rq_result_ocr = process_captcha(CurDir+"\\tmp\\"+str_username+".png")
            if rq_result_ocr.get('data') == "success":
                result_ocr = rq_result_ocr['result']
            else:
                LOG_ERROR("CAPTCHA_BHXH: ERROR")

            input_captcha = driver.find_element_by_xpath('//*[@formcontrolname="textCaptcha"]').send_keys(result_ocr)
            time.sleep(3)
            input_dangnhap = driver.find_element_by_xpath('//*[@class="login mat-raised-button mat-primary"]').click()
            time.sleep(1)

            try:
                check_element(driver,'//*[@id="accountMenuBtn"]/span/span',5)
                driver.find_element_by_xpath('//*[@id="header"]/div[2]/app-navbar/div/ul/li[1]/a/span/img') ####
                LOG_INFO("LOGIN_BHXH: THÀNH CÔNG")
                return True
            except:
                input_reset = driver.find_element_by_xpath('//*[@class="refresh"]').click()    ####
                alert_login = driver.find_element_by_id('toast-container').text             ####
                if "Mã kiểm tra không chính xác" in alert_login:
                    LOG_INFO("LOGIN_BHXH: SAI CAPTCHA!")
                    continue
                if "Tài khoản hoặc mật khẩu không chính xác." in alert_login:
                    LOG_INFO("LOGIN_BHXH: SAI THÔNG TIN TÀI KHOẢN!")
                    return False
        
        except Exception as e:
            LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            if check_element(driver,'//*[@id="accountMenuBtn"]/span/span',5):
                LOG_INFO("LOGIN: THÀNH CÔNG")
                return True
    
def kekhai_bhxh(driver,input_manghiepvu,input_thang=1,input_nam=2021,input_soluong=2,input_dinhkem=False):
    driver.get("https://dichvucong.baohiemxahoi.gov.vn/#/ke-khai/ke-khai-don-vi")
    if check_selector_element(driver,'body > app-root > ke-khai-layout > div > div > app-danh-sach-thu-tuc > div > div.content-list.ng-star-inserted > div > table > tbody > tr:nth-child(1) > td:nth-child(2) > button'):
        pass
    list_mathutuc = driver.find_elements_by_xpath('//*[@class="table tbl-thongtin scroll-horizontal table-bordered"]/tbody/tr[*]/td[4]')
    list_kekhai = driver.find_elements_by_xpath('//*[@class="table tbl-thongtin scroll-horizontal table-bordered"]/tbody/tr[*]/td[2]/button')
    time.sleep(5)
    for idx_mathutuc, i_mathutuc in enumerate(list_mathutuc):
        if str(i_mathutuc.text).strip() == str(input_manghiepvu).strip():
            driver.execute_script("arguments[0].click();", list_kekhai[idx_mathutuc])
            if check_element(driver,'//*[@id="header-dialog"]'):

                currentMonth = datetime.datetime.now().month
                # Chọn tháng
                select_xpath_options(driver,'//bhxh-month-year/div[1]/mat-form-field[1]/div[1]/div[1]/div[1]/mat-select[1]/div[1]/div[1]/span/span','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option',"Tháng "+str(currentMonth).strip())

                # Nhập năm
                driver.execute_script("arguments[0].value = '" + str(input_nam).strip() +"'",driver.find_element_by_xpath('//bhxh-month-year/div[1]/mat-form-field[2]/div[1]/div[1]/div[1]/input'))

                # Nhập số lượng
                driver.execute_script("arguments[0].value = '" + str(input_soluong).strip() +"'",driver.find_element_by_xpath('//*[@placeholder="Số lần kê khai nhận giá trị từ 01 đến 99"]'))

                # Bỏ tích đính kèm
                if input_dinhkem == False:
                    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//bhxh-input[3]/div[1]/div[1]/div[2]/div[1]/mat-checkbox[1]/label[1]/div[1]/input'))
                
                # Xác nhận
                driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector('#footer-dialog > button.mat-raised-button.mat-primary'))
                
def thutuc_bhxh(driver,data_claim):
    time.sleep(5)
    if check_selector_element(driver,'body > app-root > ke-khai-layout > div > div > app-thutuc-donvi > div > div > div > button > span'):
        # Chọn lao động
        for i in range(0,5):
            try:
                driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector('body > app-root > ke-khai-layout > div > div > app-thutuc-donvi > div > div > div > button > span'))
                time.sleep(5)
                if driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/mat-dialog-container/app-dialog-chon-lao-dong/div/div[3]/div/div[2]/mat-form-field/div/div[1]/div/mat-select/div/div[1]/span/span').text == "Ốm đau":
                    break
            except Exception as e:
                driver.find_element_by_xpath('//*[@id="footer-dialog"]/button[2]/span').click()
                LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                LOG_ERROR("THUTUC_BHXH: LỖI")
                
    else:
        LOG_ERROR("THUTUC_BHXH: KHONG TIM THAY NUT CHON LAO DONG!")
        return False, "THUTUC_BHXH: KHONG TIM THAY NUT CHON LAO DONG!"
    
    
    if check_element(driver,'//*[@formcontrolname="ten"]'):
        # driver.execute_script("arguments[0].value = '" + str(data_claim['clientEmployee']['full_name']).strip() +"'",driver.find_element_by_css_selector('#mat-input-9'))
        driver.find_element_by_xpath('//*[@formcontrolname="ten"]').send_keys(str(data_claim['clientEmployee']['full_name']).strip())
        time.sleep(2)
        driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector('#body-dialog > form > div > div.col-md-7.col-lg-8.col-xl-2.bhxh-label.btn-timkiem > button > span'))
        time.sleep(5)

        # Chọn nhân viên cần nhập
        if check_element(driver,'/html/body/div[2]/div[2]/div/mat-dialog-container/app-dialog-chon-lao-dong/div/div[2]/div/table/tbody/tr[1]'):
            pass
        list_checkbox = driver.find_elements_by_xpath('//*[@id="body-dialog"]/div/table/tbody/tr[*]/td[2]')
        list_masobhxh = driver.find_elements_by_xpath('//*[@id="body-dialog"]/div/table/tbody/tr[*]/td[7]')
        for idx_masobhxh, i_masobhxh in enumerate(list_masobhxh):
            time.sleep(1)
            if str(i_masobhxh.text).strip() == data_claim['social_insurance_number'].strip():
                list_checkbox[idx_masobhxh].click()
                time.sleep(1)
                break
                
            if idx_masobhxh == len(list_masobhxh)-1:
                LOG_ERROR("THUTUC_BHXH: KHONG TIM THAY NHAN VIEN!")
                return False, "THUTUC_BHXH: KHONG TIM THAY NHAN VIEN!"

        time.sleep(5)
        if data_claim['cd_claim_bao_hiem'] == "che_do_om_dau":
            select_xpath_options(driver,'/html/body/div[2]/div[2]/div/mat-dialog-container/app-dialog-chon-lao-dong/div/div[3]/div/div[2]/mat-form-field/div/div[1]/div/mat-select/div/div[1]','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option',"Ốm đau") 
        
        elif data_claim['cd_claim_bao_hiem'] == "che_do_thai_san":
            select_xpath_options(driver,'/html/body/div[2]/div[2]/div/mat-dialog-container/app-dialog-chon-lao-dong/div/div[3]/div/div[2]/mat-form-field/div/div[1]/div/mat-select/div/div[1]','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option',"Thai sản") 

        elif data_claim['cd_claim_bao_hiem'] == "duong_suc_phuc_hoi_suc_khoe":
            select_xpath_options(driver,'/html/body/div[2]/div[2]/div/mat-dialog-container/app-dialog-chon-lao-dong/div/div[3]/div/div[2]/mat-form-field/div/div[1]/div/mat-select/div/div[1]','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option',"Dưỡng sức") 
        else:
            LOG_ERROR("THUTUC_BHXH: SAI THÔNG TIN cd_claim_bao_hiem!")
            return False, "THUTUC_BHXH: SAI THÔNG TIN cd_claim_bao_hiem!"
        
        time.sleep(2)
        if data_claim['cd_claim_bao_hiem_sub'] == "duong_suc_dau_om":
            data_claim['cd_claim_bao_hiem_sub'] = "duong_suc_sau_om"
        if data_claim['cd_claim_bao_hiem_sub_sub'] == "suy_giam_kha_nang_lao_dong_lonhonbang_51":
            data_claim['cd_claim_bao_hiem_sub_sub'] = "suy_giam_kha_nang_lao_dong_ti_le_>=_51%"
        if data_claim['cd_claim_bao_hiem_sub_sub'] == "suy_giam_kha_nang_lao_dong_tu_31_50":
            data_claim['cd_claim_bao_hiem_sub_sub'] = "suy_giam_kha_nang_lao_dong_ti_le_tu_31%_den_50%"
        if data_claim['cd_claim_bao_hiem_sub_sub'] == "suy_giam_kha_nang_lao_dong_tu_15_30":
            data_claim['cd_claim_bao_hiem_sub_sub'] = "suy_giam_kha_nang_lao_dong_ti_le_tu_15%_den_30%"

        select_xpath_options_bodau(driver,'/html/body/div[2]/div[2]/div/mat-dialog-container/app-dialog-chon-lao-dong/div/div[3]/div/div[3]/mat-form-field/div/div[1]/div/mat-select/div/div[1]/span','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option',data_claim['cd_claim_bao_hiem_sub'])
        
        if data_claim['cd_claim_bao_hiem'] == "che_do_thai_san":
            #Nghỉ dưỡng thai
            if data_claim['cd_thai_san_nghi_duong_thai'] != "":
                element_tungaydonvidenghi = driver.find_elementS_by_xpath('//*[@class="mat-checkbox mat-accent ng-untouched ng-pristine ng-valid"]/label/div[1]')
                driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                time.sleep(3)

        time.sleep(2)
        if data_claim['cd_claim_bao_hiem'] == "duong_suc_phuc_hoi_suc_khoe":
            select_xpath_options_bodau(driver,'/html/body/div[2]/div[2]/div/mat-dialog-container/app-dialog-chon-lao-dong/div/div[3]/div/div[4]/mat-form-field/div/div[1]/div/mat-select/div/div[1]/span','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option',data_claim['cd_claim_bao_hiem_sub_sub'])
        
        driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector('#footer-dialog > button.mat-raised-button.mat-primary > span'))
        time.sleep(5)
        # Nhập thông tin cần kê khai
        try:
            if data_claim['cd_claim_bao_hiem'] == "che_do_om_dau":
                list_so_so_bhxh = driver.find_elements_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr[*]/td[3]')
                for idx,i_so_so_bhxh in enumerate(list_so_so_bhxh):
                    # print(i_so_so_bhxh.text)
                    if str(i_so_so_bhxh.text).strip() == str(data_claim["social_insurance_number"]).strip():
                        i_so_so_bhxh.click()
                        
                        #Nhập Từ ngày
                        element_tungay = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[8]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_tungay)
                        time.sleep(1)
                        element_tungay.send_keys(convert_datetime_string(data_claim['cd_claim_bh_tu_ngay']))
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()
                        

                        #Nhập Đến ngày
                        element_denngay = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[9]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_denngay)
                        time.sleep(1)
                        element_denngay.send_keys(convert_datetime_string(data_claim['cd_claim_bh_den_ngay']))
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()
                        

                        #Nhập Từ ngày đơn vị đề nghị
                        element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[10]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                        time.sleep(1)
                        element_tungaydonvidenghi.send_keys(convert_datetime_string(data_claim['cd_claim_bh_tu_ngay']))
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()

                        #Nhập Tổng số
                        element_tongso = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[12]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_tongso)
                        time.sleep(1)
                        element_tongso.send_keys(str(data_claim['cd_claim_bh_tong_so_ngay_nghi']))
                        time.sleep(1)

                        #Nhập Tuyến bệnh viện
                        if data_claim['cd_om_dau_tuyen_benh_vien'] != "":
                            select_xpath_options_contains(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[15]/bhxh-input/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div[1]/div/input','//*[@class="mat-autocomplete-panel auto-width-select-box mat-autocomplete-visible ng-star-inserted"]/mat-option',data_claim['cd_om_dau_tuyen_benh_vien'])
                            time.sleep(3)

                        #Nhập Bệnh dài ngày
                        if data_claim['cd_om_dau_benh_dai_ngay'] != "":
                            element_tongso = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[16]/bhxh-input/div/div/div/div/bhxh-benh-dai-ngay/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tongso)
                            time.sleep(1)
                            element_tongso.send_keys(str(data_claim['cd_om_dau_benh_dai_ngay']))
                            time.sleep(1)

                        #Nhập Tên bệnh
                        if data_claim['cd_om_dau_ten_benh'] != "":
                            element_tongso = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[17]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tongso)
                            time.sleep(1)
                            element_tongso.send_keys(str(data_claim['cd_om_dau_ten_benh']))
                            time.sleep(3)

                        #Nhập Hình thức nhận
                        select_xpath_options(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[22]/bhxh-input/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div[1]/div/input','//*[@class="mat-autocomplete-panel auto-width-select-box mat-autocomplete-visible ng-star-inserted"]/mat-option','ATM - Chi trả qua ATM')
                        time.sleep(5)

                        #Nhập Số tài khoản
                        element_tongso = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[23]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_tongso)
                        time.sleep(1)
                        element_tongso.send_keys(str(data_claim['thong_tin_nhan_vien']['bank_account_number']))
                        time.sleep(3)

                        #Nhập Chọn tỉnh
                        select_xpath_options_contains(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[25]/bhxh-input/div/div/div/div/bhxh-nganhang-combo-box/div/mat-form-field[1]/div/div[1]/div/input','//*[@class="mat-autocomplete-panel auto-width-select-box ng-star-inserted mat-autocomplete-visible"]/mat-option',str(data_claim['thong_tin_nhan_vien']['bank_branch']))
                        time.sleep(3)

                        #Nhập Chọn ngân hàng
                        select_xpath_options_contains(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[25]//bhxh-input/div/div/div/div/bhxh-nganhang-combo-box/div/mat-form-field[2]/div/div[1]/div/input','//*[@class="mat-autocomplete-panel auto-width-select-box ng-star-inserted mat-autocomplete-visible"]/mat-option',str(data_claim['thong_tin_nhan_vien']['bank_name']))
                        time.sleep(3)
                
                        break


                time.sleep(2)
            elif data_claim['cd_claim_bao_hiem'] == "che_do_thai_san":
                list_so_so_bhxh = driver.find_elements_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr[*]/td[3]')
                for idx,i_so_so_bhxh in enumerate(list_so_so_bhxh):
                    # print(i_so_so_bhxh.text)
                    if str(i_so_so_bhxh.text).strip() == str(data_claim["social_insurance_number"]).strip():
                        i_so_so_bhxh.click()
                        
                        #Nhập Từ ngày
                        element_tungay = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[6]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_tungay)
                        time.sleep(1)
                        element_tungay.send_keys(convert_datetime_string(data_claim['cd_claim_bh_tu_ngay']))
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()
                        

                        #Nhập Đến ngày
                        element_denngay = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[7]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_denngay)
                        time.sleep(1)
                        element_denngay.send_keys(convert_datetime_string(data_claim['cd_claim_bh_den_ngay']))
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()
                        

                        #Nhập Từ ngày đơn vị đề nghị
                        element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[8]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                        time.sleep(1)
                        element_tungaydonvidenghi.send_keys(convert_datetime_string(data_claim['cd_claim_bh_tu_ngay']))
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()

                        #Ngày sinh con
                        if data_claim['cd_thai_san_ngay_sinh_con'] != None:
                            element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[11]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                            time.sleep(1)
                            element_tungaydonvidenghi.send_keys(convert_datetime_string(data_claim['cd_claim_bh_tu_ngay']))
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()

                        #Điều kiện khi khám thai
                        if data_claim['cd_thai_san_dieu_kien_khi_kham_thai'] != "":
                            select_xpath_options_contains(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[13]/bhxh-input/div/div/div/div/mat-form-field/div/div[1]/div[1]/mat-select','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option',str(data_claim['cd_thai_san_dieu_kien_khi_kham_thai']))
                            time.sleep(3)

                        #Biện pháp tránh thai
                        if data_claim['cd_thai_san_bien_phap_tranh_thai'] != "":
                            select_xpath_options_contains_bodau(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[14]/bhxh-input/div/div/div/div/mat-form-field/div/div[1]/div[1]/mat-select','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option',str(data_claim['cd_thai_san_bien_phap_tranh_thai']))
                            time.sleep(3)

                        #Tuổi thai
                        if data_claim['cd_thai_san_tuoi_thai'] != "":
                            element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[15]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                            time.sleep(1)
                            element_tungaydonvidenghi.send_keys(data_claim['cd_thai_san_tuoi_thai'])
                            time.sleep(1)

                        #Điều kiện sinh con
                        if data_claim['cd_thai_san_dieu_kien_sinh_con'] != "":
                            select_xpath_options_contains_bodau(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[16]/bhxh-input/div/div/div/div/mat-form-field/div/div[1]/div[1]/mat-select','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option',str(data_claim['cd_thai_san_dieu_kien_sinh_con']))
                            time.sleep(3)

                        #Cha nghỉ chăm con
                        if data_claim['cd_thai_san_cha_nghi_cham_con'] != "":
                            element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[18]/bhxh-input/div[1]/div[1]/div[1]/div[1]/mat-checkbox/label/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                            time.sleep(3)

                        #Ngày nhận nuôi con
                        if data_claim['cd_thai_san_ngay_nhan_con_nuoi'] != "":
                            element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[19]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                            time.sleep(1)
                            element_tungaydonvidenghi.send_keys(convert_datetime_string(data_claim['cd_thai_san_ngay_nhan_con_nuoi']))
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()

                        #Ngày đi làm thực tế
                        if data_claim['cd_thai_san_ngay_di_lam_thuc_te'] != "":
                            element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[20]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                            time.sleep(1)
                            element_tungaydonvidenghi.send_keys(convert_datetime_string(data_claim['cd_thai_san_ngay_di_lam_thuc_te']))
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()

                        #Ngày con chết
                        if data_claim['cd_thai_san_ngay_con_chet'] != "":
                            element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[21]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                            time.sleep(1)
                            element_tungaydonvidenghi.send_keys(convert_datetime_string(data_claim['cd_thai_san_ngay_con_chet']))
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()

                        #Ngày mẹ chết
                        if data_claim['cd_thai_san_ngay_me_chet'] != "":
                            element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[22]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                            time.sleep(1)
                            element_tungaydonvidenghi.send_keys(convert_datetime_string(data_claim['cd_thai_san_ngay_me_chet']))
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()

                        #Ngày kết luận
                        if data_claim['cd_thai_san_ngay_ket_luan'] != "":
                            try:
                                element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[23]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                                driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                                time.sleep(1)
                                element_tungaydonvidenghi.send_keys(convert_datetime_string(data_claim['cd_thai_san_ngay_ket_luan']))
                                time.sleep(1)
                                driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()
                            except:
                                LOG_ERROR("Ngày kết luận")

                        #Phẩu thuật thai dưới 32 tuần
                        if data_claim['cd_thai_san_phau_thuat_thai_duoi_32t'] != "":
                            element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[32]/bhxh-input/div[1]/div[1]/div[1]/div[1]/mat-checkbox/label/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                            time.sleep(3)

                        #Số ngày nghỉ đơn vị đề nghị
                        element_tongso = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[33]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_tongso)
                        time.sleep(1)
                        element_tongso.send_keys(str(data_claim['cd_claim_bh_tong_so_ngay_nghi']))
                        time.sleep(1)

                        #Nhập Hình thức nhận
                        select_xpath_options(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[38]/bhxh-input/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div[1]/div/input','//*[@class="mat-autocomplete-panel auto-width-select-box mat-autocomplete-visible ng-star-inserted"]/mat-option','ATM - Chi trả qua ATM')
                        time.sleep(5)

                        #Nhập Số tài khoản
                        element_tongso = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[39]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_tongso)
                        time.sleep(1)
                        element_tongso.send_keys(str(data_claim['thong_tin_nhan_vien']['bank_account_number']))
                        time.sleep(3)

                        #Nhập Chọn tỉnh
                        select_xpath_options_contains(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[41]/bhxh-input/div/div/div/div/bhxh-nganhang-combo-box/div/mat-form-field[1]/div/div[1]/div/input','//*[@class="mat-autocomplete-panel auto-width-select-box ng-star-inserted mat-autocomplete-visible"]/mat-option',str(data_claim['thong_tin_nhan_vien']['bank_branch']))
                        time.sleep(3)

                        #Nhập Chọn ngân hàng
                        select_xpath_options_contains(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[41]//bhxh-input/div/div/div/div/bhxh-nganhang-combo-box/div/mat-form-field[2]/div/div[1]/div/input','//*[@class="mat-autocomplete-panel auto-width-select-box ng-star-inserted mat-autocomplete-visible"]/mat-option',str(data_claim['thong_tin_nhan_vien']['bank_name']))
                        time.sleep(3)
                
                        break


                time.sleep(2)
            elif data_claim['cd_claim_bao_hiem'] == "duong_suc_phuc_hoi_suc_khoe":
                list_so_so_bhxh = driver.find_elements_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr[*]/td[3]')
                for idx,i_so_so_bhxh in enumerate(list_so_so_bhxh):
                    # print(i_so_so_bhxh.text)
                    if str(i_so_so_bhxh.text).strip() == str(data_claim["social_insurance_number"]).strip():
                        i_so_so_bhxh.click()
                        
                        #Nhập Ngày giám định
                        if data_claim['ds_ph_suc_khoe_ngay_dam_dinh'] != '':
                            element_tungay = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[5]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungay)
                            time.sleep(1)
                            element_tungay.send_keys(convert_datetime_string(data_claim['ds_ph_suc_khoe_ngay_dam_dinh']))
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()

                        #Nhập Ngày trở lại làm việc
                        if data_claim['ds_ph_suc_khoe_ngay_tro_lai_lam_viec'] != '':
                            element_tungay = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[6]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungay)
                            time.sleep(1)
                            element_tungay.send_keys(convert_datetime_string(data_claim['ds_ph_suc_khoe_ngay_tro_lai_lam_viec']))
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()

                        #Nhập Số ngày đơn vị đề nghị
                        if data_claim['cd_claim_bh_tong_so_ngay_nghi'] != '':
                            element_tongso = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[8]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tongso)
                            time.sleep(1)
                            element_tongso.send_keys(str(data_claim['cd_claim_bh_tong_so_ngay_nghi']))
                            time.sleep(1)


                        #Nhập Từ ngày
                        if data_claim['cd_claim_bh_tu_ngay'] != '':
                            element_tungay = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[9]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungay)
                            time.sleep(1)
                            element_tungay.send_keys(convert_datetime_string(data_claim['cd_claim_bh_tu_ngay']))
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()
                        

                        #Nhập Đến ngày
                        if data_claim['cd_claim_bh_den_ngay'] != '':
                            element_denngay = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[10]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_denngay)
                            time.sleep(1)
                            element_denngay.send_keys(convert_datetime_string(data_claim['cd_claim_bh_den_ngay']))
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()
                        

                        #Nhập Từ ngày đơn vị đề nghị
                        if data_claim['cd_claim_bh_tu_ngay'] != '':
                            element_tungaydonvidenghi = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[11]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                            driver.execute_script("arguments[0].click();", element_tungaydonvidenghi)
                            time.sleep(1)
                            element_tungaydonvidenghi.send_keys(convert_datetime_string(data_claim['cd_claim_bh_tu_ngay']))
                            time.sleep(1)
                            driver.find_element_by_xpath('//*[@class="cdk-overlay-container"]').click()

                        #Nhập Hình thức nhận
                        select_xpath_options(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[15]/bhxh-input/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div[1]/div/input','//*[@class="mat-autocomplete-panel auto-width-select-box mat-autocomplete-visible ng-star-inserted"]/mat-option','ATM - Chi trả qua ATM')
                        time.sleep(5)

                        #Nhập Số tài khoản
                        element_tongso = driver.find_element_by_xpath('//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[16]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div[1]/input')
                        driver.execute_script("arguments[0].click();", element_tongso)
                        time.sleep(1)
                        element_tongso.send_keys(str(data_claim['thong_tin_nhan_vien']['bank_account_number']))
                        time.sleep(3)

                        #Nhập Chọn tỉnh
                        select_xpath_options_contains(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[18]/bhxh-input/div/div/div/div/bhxh-nganhang-combo-box/div/mat-form-field[1]/div/div[1]/div/input','//*[@class="mat-autocomplete-panel auto-width-select-box ng-star-inserted mat-autocomplete-visible"]/mat-option',str(data_claim['thong_tin_nhan_vien']['bank_branch']))
                        time.sleep(3)

                        #Nhập Chọn ngân hàng
                        select_xpath_options_contains(driver,'//*[@class="mat-expansion-panel-content ng-trigger ng-trigger-bodyExpansion mat-expanded"]/div/div/table/tbody/tr['+str(idx+1)+']/td[18]//bhxh-input/div/div/div/div/bhxh-nganhang-combo-box/div/mat-form-field[2]/div/div[1]/div/input','//*[@class="mat-autocomplete-panel auto-width-select-box ng-star-inserted mat-autocomplete-visible"]/mat-option',str(data_claim['thong_tin_nhan_vien']['bank_name']))
                        time.sleep(3)
                
                        break


                time.sleep(2)
            else:
                LOG_ERROR("THUTUC_BHXH: SAI THÔNG TIN cd_claim_bao_hiem!")
                return False, "THUTUC_BHXH: SAI THÔNG TIN cd_claim_bao_hiem!"

            driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@class="row Gui-chung-tu"]/div[1]/button[1]'))
            time.sleep(5)
            driver.get("https://dichvucong.baohiemxahoi.gov.vn/#/ke-khai/thu-tuc-don-vi/lich-su-ke-khai")
            time.sleep(5)
            thoi_gian_luu_tam = driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[1]/td[6]").text
            time.sleep(5)
            return True, thoi_gian_luu_tam

        except Exception as e:
            LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return False, e

    else:
        LOG_ERROR("THUTUC_BHXH: KHONG TIM THAY HO TEN!")
    
def job_kekhai():
    try:
        LOG_INFO("CHẠY QUY TRÌNH KÊ KHAI")
        #Lấy access_token để sử dụng api.
        rq_login_terra = login_terra()
        if rq_login_terra.get('data'):
            access_token_terra = rq_login_terra['data']['login']['access_token']
            LOG_INFO("LOGIN_TERRA: LẤY ACCESS TOKEN THÀNH CÔNG")
        else:
            LOG_ERROR("LOGIN_TERRA: KHÔNG LẤY ĐƯỢC ACCESS TOKEN!")
            return

        

        #Lấy danh sách các khách hàng của tài khoản.
        rq_get_clients_terra = get_clients_terra(access_token_terra)
        print(rq_get_clients_terra)
        
        if rq_get_clients_terra.get('data'):
            list_clients_terra = rq_get_clients_terra['data']['clients']['data']
            LOG_INFO("CLIENT_TERRA: LẤY DANH SÁCH KHÁCH HÀNG THÀNH CÔNG")
        else:
            LOG_ERROR("CLIENT_TERRA: LỖI KHÔNG LẤY ĐƯỢC DANH SÁCH KHÁCH HÀNG!")
            return

        #For từng khách hàng để truy vấn danh sách hồ sơ.
        for i_client_terra in list_clients_terra:
            id_client = i_client_terra['id']
            code_client = i_client_terra['code']
            rq_get_socialSecurityClaims_terra = get_socialSecurityClaims_terra(id_client,access_token_terra)
            print(rq_get_socialSecurityClaims_terra)

            if rq_get_socialSecurityClaims_terra.get('data'):
                list_socialSecurityClaims = rq_get_socialSecurityClaims_terra['data']['socialSecurityClaims']['data']
                LOG_INFO("CLAIMS_TERRA: LẤY DANH SÁCH HỒ SƠ - "+i_client_terra['company_name'])


                # #Chạy test
                # if "VPĐD HANKYU HANSHIN PROPERTIES CORP. TẠI TP HỒ CHÍ MINH" not in i_client_terra['company_name']:
                #     continue

                list_Claim_Company = []
                #For từng hồ sơ để xử lý
                for i_socialSecurityClaim in list_socialSecurityClaims:
                    # print(i_socialSecurityClaim)
                    if i_socialSecurityClaim['state'] == "da_phe_duyet" :
                        pass
                    else:
                        continue

                    rq_get_clientEmployee = get_clientEmployee(i_socialSecurityClaim['client_employee_id'],access_token_terra)
                    if rq_get_clientEmployee.get('data') and rq_get_clientEmployee['data']['clientEmployee'] != None:
                        dic_clientEmployee = rq_get_clientEmployee['data']['clientEmployee']
                        LOG_INFO("EMPLOYEE_TERRA: LẤY THÔNG TIN NHÂN VIÊN - "+dic_clientEmployee['full_name'])
                    else:
                        LOG_ERROR("EMPLOYEE_TERRA: LỖI KHÔNG LẤY ĐƯỢC THÔNG TIN NHÂN VIÊN! - ["+i_socialSecurityClaim['client_employee_id']+"]")
                        break

                    i_socialSecurityClaim['thong_tin_nhan_vien'] = dic_clientEmployee

                    r_result = post_service({"name_claim":i_socialSecurityClaim['id'], "data_claim":i_socialSecurityClaim, "company_claim":code_client, "status_claim":"Wait"})
                    if r_result.get('name_claim')[0] == 'claim with this name claim already exists.':
                        continue

                list_Claim_Company = get_service(code_client)
                print(list_Claim_Company)

                list_Claim_Company = [x for x in list_Claim_Company if x['status_claim'] == 'Wait']
                LOG_INFO("Số lượng hồ sơ cần kê khai: "+str(len(list_Claim_Company)))
                if len(list_Claim_Company) != 0:
                    mycursor.execute("SELECT * FROM social_accounts WHERE client_code = (%s)", (str(code_client),))
                    myresult = mycursor.fetchall()[0]
                    driver = open_brower()           
                    login_bhxh(driver,myresult[-2],myresult[-1])
                    driver.get("https://dichvucong.baohiemxahoi.gov.vn/")
                    for i_Claim_Company in list_Claim_Company:
                        try:
                            data_claim = i_Claim_Company['data_claim']
                            input_thang = int(regex.split(r'-',data_claim['cd_claim_bh_tu_ngay'])[1])
                            input_nam = int(regex.split(r'-',data_claim['cd_claim_bh_tu_ngay'])[0])
                            kekhai_bhxh(driver,"630",str(input_thang),str(input_nam),1)
                            bl_return, str_Note = thutuc_bhxh(driver,data_claim)
                            LOG_INFO(str_Note)
                            if bl_return:
                                patch_service(i_Claim_Company['id'],{"status_claim":"Running","note_claim":str(str_Note)})
                                # update_socialSecurityClaims_terra(data_claim['id'],'da_ke_khai_ho_so')
                                input_data_claim = data_claim.copy()
                                del input_data_claim['id']
                                del input_data_claim['thong_tin_nhan_vien']
                                del input_data_claim['created_at']
                                del input_data_claim['__typename']
                                del input_data_claim['updated_at']
                                del input_data_claim['clientEmployee']
                                
                                data_input = {}
                                data_input['id'] = data_claim['id']
                                data_input['input'] = input_data_claim
                                data_input['input']['state'] = "da_ke_khai_ho_so"
                                update_socialSecurityClaims_terra(data_input,access_token_terra)
                                LOG_INFO("HỒ SƠ ĐÃ LƯU TẠM")
                            else:
                                patch_service(i_Claim_Company['id'],{"status_claim":"Error","note_claim":str(str_Note)})
                                LOG_ERROR("HỒ SƠ BỊ LỖI")
                        except Exception as e:
                            LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                            patch_service(i_Claim_Company['id'],{"status_claim":"Error","note_claim":str(str_Note)})
                            LOG_ERROR("HỒ SƠ BỊ LỖI")
                            continue

                    driver.quit()
    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
def job_quet():
    try:
        #Lấy access_token để sử dụng api.
        LOG_INFO("CHẠY QUY TRÌNH QUÉT KẾT QUẢ")
        rq_login_terra = login_terra()
        if rq_login_terra.get('data'):
            access_token_terra = rq_login_terra['data']['login']['access_token']
            LOG_INFO("LOGIN_TERRA: LẤY ACCESS TOKEN THÀNH CÔNG")
        else:
            LOG_ERROR("LOGIN_TERRA: KHÔNG LẤY ĐƯỢC ACCESS TOKEN!")
            return

        

        #Lấy danh sách các khách hàng của tài khoản.
        rq_get_clients_terra = get_clients_terra(access_token_terra)
        print(rq_get_clients_terra)
        if rq_get_clients_terra.get('data'):
            list_clients_terra = rq_get_clients_terra['data']['clients']['data']
            LOG_INFO("CLIENT_TERRA: LẤY DANH SÁCH KHÁCH HÀNG THÀNH CÔNG")
        else:
            LOG_ERROR("CLIENT_TERRA: LỖI KHÔNG LẤY ĐƯỢC DANH SÁCH KHÁCH HÀNG!")
            return

        #For từng khách hàng để truy vấn danh sách hồ sơ.
        for i_client_terra in list_clients_terra:
            id_client = i_client_terra['id']
            code_client = i_client_terra['code']
            rq_get_socialSecurityClaims_terra = get_socialSecurityClaims_terra(id_client,access_token_terra)
            print(rq_get_socialSecurityClaims_terra)
            if rq_get_socialSecurityClaims_terra.get('data'):
                list_socialSecurityClaims = rq_get_socialSecurityClaims_terra['data']['socialSecurityClaims']['data']
                LOG_INFO("CLAIMS_TERRA: LẤY DANH SÁCH HỒ SƠ - "+i_client_terra['company_name'])


                # #Chạy test
                # if "VPĐD HANKYU HANSHIN PROPERTIES CORP. TẠI TP HỒ CHÍ MINH" not in i_client_terra['company_name']:
                #     continue

                list_Claim_Company = []
                #For từng hồ sơ để xử lý
                for i_socialSecurityClaim in list_socialSecurityClaims:
                    # print(i_socialSecurityClaim)
                    if i_socialSecurityClaim['state'] == "da_phe_duyet" :
                        pass
                    else:
                        continue

                    rq_get_clientEmployee = get_clientEmployee(i_socialSecurityClaim['client_employee_id'],access_token_terra)
                    print(rq_get_clientEmployee)
                    if rq_get_clientEmployee.get('data') and rq_get_clientEmployee['data']['clientEmployee'] != None:
                        dic_clientEmployee = rq_get_clientEmployee['data']['clientEmployee']
                        LOG_INFO("EMPLOYEE_TERRA: LẤY THÔNG TIN NHÂN VIÊN - "+dic_clientEmployee['full_name'])
                    else:
                        LOG_ERROR("EMPLOYEE_TERRA: LỖI KHÔNG LẤY ĐƯỢC THÔNG TIN NHÂN VIÊN! - ["+i_socialSecurityClaim['client_employee_id']+"]")
                        break

                    i_socialSecurityClaim['thong_tin_nhan_vien'] = dic_clientEmployee

                    r_result = post_service({"name_claim":i_socialSecurityClaim['id'], "data_claim":i_socialSecurityClaim, "company_claim":code_client, "status_claim":"Wait"})
                    if r_result.get('name_claim')[0] == 'claim with this name claim already exists.':
                        continue

                list_Claim_Company = get_service(code_client)
                print(list_Claim_Company)
                
                list_Claim_Company = [x for x in list_Claim_Company if x['status_claim'] == 'Running']
                LOG_INFO("Số lượng hồ sơ cần quét kết quả: "+str(len(list_Claim_Company)))
                if len(list_Claim_Company) != 0:
                    mycursor.execute("SELECT * FROM social_accounts WHERE client_code = (%s)", (str(code_client),))
                    myresult = mycursor.fetchall()[0]
                    driver = open_brower()         
                    login_bhxh(driver,myresult[-2],myresult[-1])
                    driver.get("https://dichvucong.baohiemxahoi.gov.vn/")
                    for i_Claim_Company in list_Claim_Company:
                        try:
                            data_claim = i_Claim_Company['data_claim']
                            input_thang = int(regex.split(r'-',data_claim['cd_claim_bh_tu_ngay'])[1])
                            input_nam = int(regex.split(r'-',data_claim['cd_claim_bh_tu_ngay'])[0])
                            # kekhai_bhxh(driver,"630",str(input_thang),str(input_nam),1)
                            time.sleep(5)
                            driver.get("https://dichvucong.baohiemxahoi.gov.vn/#/ke-khai/thu-tuc-don-vi/lich-su-ke-khai")
                            time.sleep(5)
                            driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[1]/div/div[2]/mat-form-field/div/div[1]/div/input").clear()
                            driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[1]/div/div[2]/mat-form-field/div/div[1]/div/input").send_keys(str(int(input_thang)))
                            driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[6]/button").click()
                            time.sleep(5)
                            list_MATHUTUC = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[2]")
                            list_SOHOSO = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[3]")
                            list_DOTKEKHAI = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[4]")
                            list_KYKEKHAI = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[5]")
                            list_NGAYKEKHAI = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[6]")
                            list_TRANGTHAI = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[7]")
                            for idx_NGAYKEKHAI, i_NGAYKEKHAI in enumerate(list_NGAYKEKHAI):
                                if str(i_NGAYKEKHAI.text) == str(i_Claim_Company['note_claim']):
                                    if str(list_TRANGTHAI[idx_NGAYKEKHAI].text) != "Đã lưu tạm":
                                        patch_service(i_Claim_Company['id'],{"status_claim":"Complete","note_claim":str(list_SOHOSO[idx_NGAYKEKHAI].text)})
                                        # update_socialSecurityClaims_terra(data_claim['id'],'da_ke_khai_ho_so')
                                        input_data_claim = data_claim.copy()
                                        del input_data_claim['id']
                                        del input_data_claim['thong_tin_nhan_vien']
                                        del input_data_claim['created_at']
                                        del input_data_claim['__typename']
                                        del input_data_claim['updated_at']
                                        del input_data_claim['clientEmployee']
                                        
                                        data_input = {}
                                        data_input['id'] = data_claim['id']
                                        data_input['input'] = input_data_claim
                                        data_input['input']['state'] = "done"
                                        print(update_socialSecurityClaims_terra(data_input,access_token_terra))
                                        LOG_INFO("HỒ SƠ LƯU TẠM "+str(i_Claim_Company['note_claim'])+" ĐÃ NỘP")
                                    else:
                                        LOG_INFO("HỒ SƠ LƯU TẠM "+str(i_Claim_Company['note_claim'])+" CHƯA CẬP NHẬT")
                        except Exception as e:
                            LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                            continue
                    driver.quit()
    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


def job_backup():
    LOG_INFO("CHẠY QUY TRÌNH QUÉT KẾT QUẢ")
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
    
    assert object_to_backup_path.exists()  # Validate the object we are about to backup exists before we continue

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
            job_quet()
    else:
        schedule.every().day.at(data_config['che_do_ke_khai']['thoi_gian_co_dinh']).do(job_kekhai)
        schedule.every().day.at(data_config['che_do_quet_ket_qua']['thoi_gian_co_dinh']).do(job_quet)

    while True:
        schedule.run_pending()
        time.sleep(1)
