# coding: UTF-8
import enum
import os
import inspect
import time
from tkinter.messagebox import NO
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
import glob
import pandas as pd


CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
import logging
global LOG_INFO
name_Organization = "vpo"
name_Robot = "600"
name_Version = "1.1.1"
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
        
        print(i.text)
        if str(i.text).strip() == str(input_option).strip():
            print(i.text)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", i)
            time.sleep(1)
            break

def select_xpath_options_click(driver,xpath_select,xpath_options,input_option,timeout=1):
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(xpath_select))
    time.sleep(timeout)
    for i in driver.find_elements_by_xpath(xpath_options):
        
        # print(i.text)
        if str(i.text).strip() == str(input_option).strip():
            print(i.text)
            time.sleep(1)
            i.click()
            time.sleep(1)
            break

def get_list_Nop_new(list_old,list_new):
    list_result = []
    if list_old is None:
        print("a")
    for idx_new, i_new in enumerate(list_new):
        if list_old is None or idx_new <= len(list_old)-1:
            for idx_desc in range(0,len(i_new['Desc'][0]['STT'])):
                try:
                    if i_new['Desc'][0]['STT'][idx_desc] == list_old[idx_new]['Desc'][0]['STT'][idx_desc]:
                        continue
                except:
                    list_result.append("Bước: "+i_new['Bước']+" | "+"Tên cơ quan: "+i_new['Tên cơ quan']+" | "+"Phòng ban xử lý': "+i_new['Phòng ban xử lý']+" | "+i_new['Desc'][0]['STT'][idx_desc]+" - "+i_new['Desc'][0]['Cán bộ xử lý'][idx_desc]+" - "+i_new['Desc'][0]['Hành động'][idx_desc]+" - "+i_new['Desc'][0]['Thời gian xử lý'][idx_desc])
                    print("Bước: "+i_new['Bước']+" | "+"Tên cơ quan: "+i_new['Tên cơ quan']+" | "+"Phòng ban xử lý': "+i_new['Phòng ban xử lý']+" | "+i_new['Desc'][0]['STT'][idx_desc]+" - "+i_new['Desc'][0]['Cán bộ xử lý'][idx_desc]+" - "+i_new['Desc'][0]['Hành động'][idx_desc]+" - "+i_new['Desc'][0]['Thời gian xử lý'][idx_desc])
        else:
            for idx_desc in range(0,len(i_new['Desc'][0]['STT'])):
                list_result.append("Bước: "+i_new['Bước']+" | "+"Tên cơ quan: "+i_new['Tên cơ quan']+" | "+"Phòng ban xử lý': "+i_new['Phòng ban xử lý']+" | "+i_new['Desc'][0]['STT'][idx_desc]+" - "+i_new['Desc'][0]['Cán bộ xử lý'][idx_desc]+" - "+i_new['Desc'][0]['Hành động'][idx_desc]+" - "+i_new['Desc'][0]['Thời gian xử lý'][idx_desc])
                print("Bước: "+i_new['Bước']+" | "+"Tên cơ quan: "+i_new['Tên cơ quan']+" | "+"Phòng ban xử lý': "+i_new['Phòng ban xử lý']+" | "+i_new['Desc'][0]['STT'][idx_desc]+" - "+i_new['Desc'][0]['Cán bộ xử lý'][idx_desc]+" - "+i_new['Desc'][0]['Hành động'][idx_desc]+" - "+i_new['Desc'][0]['Thời gian xử lý'][idx_desc])
    return list_result

# --- XỬ LÝ API ---

def get_service(id_client):
    payload = ""
    url = data_config['url_service']+"/claim/?company_claim="+str(id_client)
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1'
    }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def post_service(payload):
    url = data_config['url_service']+"/claim/"
    payload = json.dumps(payload)
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1',
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def patch_service(id,payload):

    url = data_config['url_service']+"/claim/"+str(id)+"/"
    payload = json.dumps(payload)
    headers = {
    'Authorization': 'Basic dmJwbzpWYnBvQDEyMzQ1',
    'Content-Type': 'application/json'
    }
    response = requests.request("PATCH", url, headers=headers, data=payload)
    return response.json()

def login_terra():

    url = data_config['url_terra']
    payload="{\"query\":\"mutation login ($username: String!, $password: String!, $client_code: String) {\\n    login (username: $username, password: $password, client_code: $client_code) {\\n        access_token\\n        refresh_token\\n        expires_in\\n        token_type\\n    }\\n}\",\"variables\":{\"username\":\""+data_security['username_terra']+"\",\"password\":\""+data_security['password_terra']+"\",\"client_code\":\""+data_security['code_terra']+"\"}}"
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def get_clients_terra(access_token_terra):
    
    url = data_config['url_terra']
    payload="{\"query\":\"query getWithAssignments($perPage: Int!, $page: Int, $orderBy: [ClientsOrderByOrderByClause!], $where: ClientsWhereWhereConditions) {\\n  clients(orderBy: $orderBy, where: $where, first: $perPage, page: $page) {\\n    paginatorInfo {\\n      count\\n      currentPage\\n      firstItem\\n      hasMorePages\\n      lastItem\\n      lastPage\\n      perPage\\n      total\\n      __typename\\n    }\\n    data {\\n      ...clientFields\\n      assignedInternalEmployees {\\n        id\\n        name\\n        code\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\\nfragment clientFields on Client {\\n  id\\n  code\\n  company_name\\n  company_contact_phone\\n  company_contact_email\\n  address\\n  company_bank_account\\n  company_account_number\\n  company_bank_name\\n  company_bank_branch\\n  person_signing_a_bank_document\\n  employees_number_foreign\\n  employees_number_vietnamese\\n  rewards_for_achievements\\n  annual_salary_bonus\\n  social_insurance_and_health_insurance_ceiling\\n  unemployment_insurance_ceiling\\n  payroll_creator\\n  payroll_approver\\n  social_insurance_agency\\n  social_insurance_account_name\\n  social_insurance_account_number\\n  social_insurance_bank_name\\n  social_insurance_bank_branch\\n  social_insurance_unit_code\\n  trade_union_agency\\n  trade_union_account_name\\n  trade_union_account_number\\n  trade_union_bank_name\\n  trade_union_bank_branch\\n  presenter_phone\\n  company_contact_fax\\n  presenter_email\\n  presenter_name\\n  company_license_no\\n  company_license_issuer\\n  company_license_issued_at\\n  company_license_updated_at\\n  company_license_at\\n  timesheet_min_time_block\\n  day_payroll_start\\n  day_payroll_end\\n  type_of_business\\n  clientWorkflowSetting {\\n    id\\n    client_id\\n    enable_overtime_request\\n    enable_leave_request\\n    enable_early_leave_request\\n    enable_timesheet_input\\n    enable_social_security_manage\\n    enable_salary_payment\\n    manage_user\\n    enable_wifi_checkin\\n    enable_training_seminar\\n    enable_recruit_function\\n    enable_contract_reminder\\n    __typename\\n  }\\n  created_at\\n  updated_at\\n  is_active\\n  __typename\\n}\\n\",\"variables\":{\"perPage\":1000,\"page\":1,\"orderBy\":[{\"field\":\"COMPANY_NAME\",\"order\":\"ASC\"}],\"where\":{}}}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def get_socialSecurityProfileRequests(id_client,access_token_terra):
    """ Get list hồ sơ kê khai """
    url = data_config['url_terra']

    payload="{\"query\":\"query get($perPage: Int!, $page: Int, $orderBy: [SocialSecurityProfileRequestsOrderByOrderByClause!], $where: SocialSecurityProfileRequestsWhereWhereConditions) {\\r\\n  socialSecurityProfileRequests(orderBy: $orderBy, where: $where, first: $perPage, page: $page) {\\r\\n    paginatorInfo {\\r\\n      count\\r\\n      currentPage\\r\\n      firstItem\\r\\n      hasMorePages\\r\\n      lastItem\\r\\n      lastPage\\r\\n      perPage\\r\\n      total\\r\\n      __typename\\r\\n    }\\r\\n    data {\\r\\n      id\\r\\n      client_id\\r\\n      created_at\\r\\n      ten_ho_so\\r\\n      loai_ho_so_type\\r\\n      tinh_trang_giai_quyet_ho_so\\r\\n      status\\r\\n      approved_date\\r\\n      approved_comment\\r\\n      note\\r\\n      __typename\\r\\n    }\\r\\n    __typename\\r\\n  }\\r\\n}\\r\\n\",\"variables\":{\"perPage\":1000,\"page\":1,\"orderBy\":[{\"field\":\"CREATED_AT\",\"order\":\"DESC\"}],\"where\":{\"AND\":[{\"column\":\"CLIENT_ID\",\"operator\":\"EQ\",\"value\":\""+id_client+"\"}]}}}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def rq_socialSecurityProfileRequests(id_client,access_token_terra):
    """get bộ hồ sơ: kê khai và update kết quả kê khai 600"""
    url = data_config['url_terra']
    payload="{\"query\":\"query find($id: ID!) {\\r\\n  socialSecurityProfileRequest(id: $id) {\\r\\n    ...socialSecurityProfileRequestFields\\r\\n    __typename\\r\\n  }\\r\\n}\\r\\n\\r\\nfragment socialSecurityProfileRequestFields on SocialSecurityProfileRequest {\\r\\n  id\\r\\n  client_id\\r\\n  ten_ho_so\\r\\n  loai_ho_so_type\\r\\n  loai_ho_so_sub\\r\\n  loai_ho_so_from_date\\r\\n  loai_ho_so_to_date\\r\\n  tinh_trang_giai_quyet_ho_so\\r\\n  ngay_ke_khai_va_luu_tam_ho_so\\r\\n  ngay_nop_ho_so\\r\\n  so_ho_so_bhxh_da_ke_khai\\r\\n  ngay_hen_tra_ket_qua\\r\\n  tinh_trang_chung_tu_lien_quan\\r\\n  loai_nhap_ke_khai\\r\\n  media_path\\r\\n  mediaTemp {\\r\\n    id\\r\\n    name\\r\\n    file_name\\r\\n    collection_name\\r\\n    mime_type\\r\\n    created_at\\r\\n    url\\r\\n    __typename\\r\\n  }\\r\\n  note\\r\\n  bo_phan_cd_bhxh_date\\r\\n  bo_phan_cd_bhxh_reviewer\\r\\n  bo_phan_khtc_date\\r\\n  bo_phan_khtc_reviewer\\r\\n  bo_phan_tn_tkq_date\\r\\n  bo_phan_tn_tkq_reviewer\\r\\n  status\\r\\n  created_at\\r\\n  updated_at\\r\\n  note\\r\\n  socialSecurityProfiles {\\r\\n    client_id\\r\\n    client_employee_id\\r\\n    social_security_profile_request_id\\r\\n    loai_nhap_ke_khai\\r\\n    ho_va_ten\\r\\n    so_so_bhxh\\r\\n    so_cmnd_hc\\r\\n    so_dien_thoai\\r\\n    noi_dk_kcb_ban_dau_tinh\\r\\n    noi_dk_kcb_ban_dau_benh_vien\\r\\n    can_cu_theo\\r\\n    so_van_ban\\r\\n    ngay_hieu_luc\\r\\n    ngay_ket_thuc\\r\\n    muc_luong_moi\\r\\n    chuc_vu_moi\\r\\n    gioi_tinh\\r\\n    ngay_sinh\\r\\n    quoc_tich\\r\\n    dan_toc\\r\\n    noi_dk_giay_khai_sinh\\r\\n    dia_chi_lien_he_nhan_ho_so\\r\\n    sdt_lien_he\\r\\n    email\\r\\n    so_ho_gia_dinh_da_cap\\r\\n    muc_tien_dong\\r\\n    phuong_thuc_dong\\r\\n    noi_dung_thay_doi_yeu_cau\\r\\n    comment\\r\\n    mediaTemp {\\r\\n      id\\r\\n      name\\r\\n      file_name\\r\\n      collection_name\\r\\n      mime_type\\r\\n      created_at\\r\\n      url\\r\\n      __typename\\r\\n    }\\r\\n    __typename\\r\\n  }\\r\\n  __typename\\r\\n}\\r\\n\",\"variables\":{\"id\":\""+id_client+"\"}}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def update_SocialSecurityProfileRequests_terra(data_input, access_token_terra):
    "update thông tin kê khai 600 cho bộ hồ sơ"
    # {\"id\":\"0f6f7eb9-d605-4e7f-b66d-4506fd912296\",\"input\":{\"client_id\":\"e6be2511-aacd-4780-8e1d-0c7d429fb167\",\"ten_ho_so\":\"Báo tăng tháng 2.2022.test\",\"ma_ho_so\":null,\"loai_ho_so_type\":\"tang_lao_dong\",\"loai_ho_so_sub\":\"tang_moi\",\"loai_ho_so_from_date\":\"2022-02-01\",\"loai_ho_so_to_date\":\"2022-02-01\",\"tinh_trang_chung_tu_lien_quan\":\"da_gui\",\"note\":\"TeST API\",\"reviewer_id\":null,\"loai_nhap_ke_khai\":\"auto\",\"employees\":[{\"client_id\":\"e6be2511-aacd-4780-8e1d-0c7d429fb167\",\"client_employee_id\":\"7481a516-4071-45d1-b2f8-d7b666a410e9\",\"social_security_profile_request_id\":\"0f6f7eb9-d605-4e7f-b66d-4506fd912296\",\"loai_nhap_ke_khai\":\"auto\",\"ho_va_ten\":\"Huỳnh Văn Anh Tuấn\",\"so_so_bhxh\":\"7910119655\",\"so_cmnd_hc\":\"225156905\",\"so_dien_thoai\":\"000\",\"noi_dk_kcb_ban_dau_tinh\":\"Thành phố Hà Nội\",\"noi_dk_kcb_ban_dau_benh_vien\":\"01805 - Trung tâm y tế Cầu Giấy\",\"can_cu_theo\":\"Hợp đồng lao động\",\"so_van_ban\":\"\",\"ngay_hieu_luc\":\"\",\"ngay_ket_thuc\":\"\",\"muc_luong_moi\":\"\",\"chuc_vu_moi\":\"\",\"gioi_tinh\":\"Male\",\"ngay_sinh\":\"1980-01-01\",\"quoc_tich\":\"VN\",\"dan_toc\":\"Kinh\",\"noi_dk_giay_khai_sinh\":null,\"dia_chi_lien_he_nhan_ho_so\":null,\"sdt_lien_he\":null,\"email\":\"\",\"so_ho_gia_dinh_da_cap\":null,\"muc_tien_dong\":\"20000000\",\"phuong_thuc_dong\":\"Hàng tháng\",\"noi_dung_thay_doi_yeu_cau\":\"\",\"comment\":null},{\"client_id\":\"e6be2511-aacd-4780-8e1d-0c7d429fb167\",\"client_employee_id\":\"ba24a56e-bdf6-47fe-bce7-855932b11359\",\"social_security_profile_request_id\":\"0f6f7eb9-d605-4e7f-b66d-4506fd912296\",\"loai_nhap_ke_khai\":\"auto\",\"ho_va_ten\":\"Phạm Nguyễn Tường Vy\",\"so_so_bhxh\":\"7916436045\",\"so_cmnd_hc\":\"225477816\",\"so_dien_thoai\":\"0000\",\"noi_dk_kcb_ban_dau_tinh\":\"Thành phố Hà Nội\",\"noi_dk_kcb_ban_dau_benh_vien\":\"01819 - Bệnh viện Quân Y 105\",\"can_cu_theo\":\"Hợp đồng lao động\",\"so_van_ban\":\"\",\"ngay_hieu_luc\":\"\",\"ngay_ket_thuc\":\"\",\"muc_luong_moi\":\"\",\"chuc_vu_moi\":\"\",\"gioi_tinh\":\"Female\",\"ngay_sinh\":\"1980-01-01\",\"quoc_tich\":\"VN\",\"dan_toc\":\"Kinh\",\"noi_dk_giay_khai_sinh\":null,\"dia_chi_lien_he_nhan_ho_so\":null,\"sdt_lien_he\":null,\"email\":\"\",\"so_ho_gia_dinh_da_cap\":null,\"muc_tien_dong\":\"30000000\",\"phuong_thuc_dong\":\"Hàng tháng\",\"noi_dung_thay_doi_yeu_cau\":\"\",\"comment\":null}],\"tinh_trang_giai_quyet_ho_so\":\"da_ky_nop_ho_so_to_co_quan_bhxh\",\"ngay_ke_khai_va_luu_tam_ho_so\":\"2022-01-19\",\"ngay_nop_ho_so\":\"2022-01-20\",\"so_ho_so_bhxh_da_ke_khai\":\"123456/2022/012345\",\"ngay_hen_tra_ket_qua\":null,\"bo_phan_cd_bhxh_date\":null,\"bo_phan_cd_bhxh_reviewer\":\"\",\"bo_phan_khtc_date\":null,\"bo_phan_khtc_reviewer\":\"\",\"bo_phan_tn_tkq_date\":null,\"bo_phan_tn_tkq_reviewer\":\"\"}}}"
   
    data_playload = json.dumps(data_input)
    print(data_playload)
    url = data_config['url_terra']
    payload="{\"query\":\"mutation update($id: ID!, $input: SocialSecurityProfileRequestInput) {\\r\\n  updateSocialSecurityProfileRequest(id: $id, input: $input) {\\r\\n    ...socialSecurityProfileRequestFields\\r\\n    __typename\\r\\n  }\\r\\n}\\r\\n\\r\\nfragment socialSecurityProfileRequestFields on SocialSecurityProfileRequest {\\r\\n  id\\r\\n  client_id\\r\\n  ten_ho_so\\r\\n  ma_ho_so\\r\\n  loai_ho_so_type\\r\\n  loai_ho_so_sub\\r\\n  loai_ho_so_from_date\\r\\n  loai_ho_so_to_date\\r\\n  tinh_trang_giai_quyet_ho_so\\r\\n  ngay_ke_khai_va_luu_tam_ho_so\\r\\n  ngay_nop_ho_so\\r\\n  so_ho_so_bhxh_da_ke_khai\\r\\n  ngay_hen_tra_ket_qua\\r\\n  tinh_trang_chung_tu_lien_quan\\r\\n  loai_nhap_ke_khai\\r\\n  media_path\\r\\n  mediaTemp {\\r\\n    id\\r\\n    name\\r\\n    file_name\\r\\n    collection_name\\r\\n    mime_type\\r\\n    created_at\\r\\n    url\\r\\n    __typename\\r\\n  }\\r\\n  note\\r\\n  bo_phan_cd_bhxh_date\\r\\n  bo_phan_cd_bhxh_reviewer\\r\\n  bo_phan_khtc_date\\r\\n  bo_phan_khtc_reviewer\\r\\n  bo_phan_tn_tkq_date\\r\\n  bo_phan_tn_tkq_reviewer\\r\\n  status\\r\\n  created_at\\r\\n  updated_at\\r\\n  note\\r\\n  socialSecurityProfiles {\\r\\n    client_id\\r\\n    client_employee_id\\r\\n    social_security_profile_request_id\\r\\n    loai_nhap_ke_khai\\r\\n    ho_va_ten\\r\\n    so_so_bhxh\\r\\n    so_cmnd_hc\\r\\n    so_dien_thoai\\r\\n    noi_dk_kcb_ban_dau_tinh\\r\\n    noi_dk_kcb_ban_dau_benh_vien\\r\\n    can_cu_theo\\r\\n    so_van_ban\\r\\n    ngay_hieu_luc\\r\\n    ngay_ket_thuc\\r\\n    muc_luong_moi\\r\\n    chuc_vu_moi\\r\\n    gioi_tinh\\r\\n    ngay_sinh\\r\\n    quoc_tich\\r\\n    dan_toc\\r\\n    noi_dk_giay_khai_sinh\\r\\n    dia_chi_lien_he_nhan_ho_so\\r\\n    sdt_lien_he\\r\\n    email\\r\\n    so_ho_gia_dinh_da_cap\\r\\n    muc_tien_dong\\r\\n    phuong_thuc_dong\\r\\n    noi_dung_thay_doi_yeu_cau\\r\\n    comment\\r\\n    mediaTemp {\\r\\n      id\\r\\n      name\\r\\n      file_name\\r\\n      collection_name\\r\\n      mime_type\\r\\n      created_at\\r\\n      url\\r\\n      __typename\\r\\n    }\\r\\n    __typename\\r\\n  }\\r\\n  __typename\\r\\n}\\r\\n\",\"variables\":"+data_playload+"}"
    headers = {
    'Authorization': 'Bearer '+access_token_terra,
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def process_data_terra(data_claim):
    input_data_claim = data_claim.copy()
    del input_data_claim['id']
    del input_data_claim['client_id']
    del input_data_claim['created_at']
    del input_data_claim['updated_at']
    del input_data_claim['media_path']
    del input_data_claim['mediaTemp']
    del input_data_claim['status']
    del input_data_claim['__typename']
    employees = input_data_claim['socialSecurityProfiles']
    del input_data_claim['socialSecurityProfiles']
    input_data_claim['employees'] = employees
    for i_claim in input_data_claim['employees']:
        del i_claim['mediaTemp']
        del i_claim['__typename']
    data_input = {}
    data_input['id'] = data_claim['id']
    data_input['input'] = input_data_claim
    data_input['input']['client_id'] = data_claim['client_id']
    return data_input

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

def login_bhxh(driver,str_username,str_password,code_bhxh):
    driver.get("https://dichvucong.baohiemxahoi.gov.vn/")
    if check_element(driver,'//*[@id="accountMenuBtn"]',2):
        logout_bhxh(driver)

    # check_element(driver,'//*[@id="content"]/div[1]/div/div/div[3]/div/ul/li[1]/a/img')
    # btn_kekhai = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/div/div[3]/div/ul/li[1]/a/img').click()
    
    check_element(driver,'//*[@id="header"]/div/div/div/div[2]/div/div/button[1]/span')
    time.sleep(1)
    btn_kekhai = driver.find_element_by_xpath('//*[@id="header"]/div/div/div/div[2]/div/div/button[1]/span').click()
    time.sleep(1)
    check_element(driver,'//*[@formcontrolname="username"]')
    checkbox_tochuc = driver.find_element_by_xpath('//*[@id="mat-checkbox-2"]/label/div').click()
    time.sleep(1)
    input_username = driver.find_element_by_xpath('//*[@formcontrolname="username"]').clear()
    input_username = driver.find_element_by_xpath('//*[@formcontrolname="username"]').send_keys(str_username.strip())
    time.sleep(1)
    input_password = driver.find_element_by_xpath('//*[@formcontrolname="password"]').clear()
    input_password = driver.find_element_by_xpath('//*[@formcontrolname="password"]').send_keys(str_password.strip())
    int_Count = 0
    while True:
        try:
            if int_Count >= 5:
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
                check_element(driver,'//*[@id="header"]/div/div/div/div[2]/div/div/div[1]/button',10)
                time.sleep(1)
                driver.find_element_by_xpath('/html/body/app-root/app-portal/app-portal-header/div/div/div/div/div[2]/div/div/div[1]/button').click()
                list_coce_bhxh = driver.find_elements_by_xpath('//*[@id="header"]/div/div/div/div[2]/div/div/div[1]/div/button[*]')
                for idx, i_element in enumerate(list_coce_bhxh):
                    if code_bhxh in i_element.text:
                        i_element.click()
                        break
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/div/div[3]/div/ul/li[1]/a/img').click()
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="header"]/div[2]/app-navbar/div/ul/li[1]/a/span/img')
                LOG_INFO("LOGIN_BHXH: THÀNH CÔNG")
                return True
            except Exception as e:
                print(e)
                input_reset = driver.find_element_by_xpath('//*[@class="refresh"]').click()
                alert_login = driver.find_element_by_id('toast-container').text
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

def select_xpath_options_phuong_an(driver,xpath_select, xpath_options, input_option, timeout = 1):
    "sreach options Chọn phương án"
    
    driver.find_element_by_xpath(xpath_select).click()
    # move chuot toi element 10,20
    try:
        time.sleep(1)
        ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@class="cdk-overlay-pane"]/div/mat-option[10]')).perform()
        time.sleep(3)
        ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@class="cdk-overlay-pane"]/div/mat-option[1]')).perform()
        time.sleep(3)
        ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@class="cdk-overlay-pane"]/div/mat-option[10]')).perform()
        time.sleep(3)
        ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@class="cdk-overlay-pane"]/div/mat-option[20]')).perform()
        time.sleep(1)
        # a = (driver.find_elements_by_xpath('//*[@class="cdk-overlay-pane"]/div/mat-option'))
        for idx, element in enumerate(driver.find_elements_by_xpath('//*[@class="cdk-overlay-pane"]/div/mat-option')):
            i_phuong_an = str(element.text).split(' - ')[1]
            print(regex.sub(r'\s','_',str(unidecode(i_phuong_an)).lower().strip()))
            if regex.sub(r'\s','_',str(unidecode(i_phuong_an)).lower().strip()) ==  str(unidecode(input_option)).lower().strip():
                driver.execute_script("arguments[0].click();", element)
                time.sleep(timeout)
                break
            else:
                ActionChains(driver).move_to_element(driver.find_element_by_xpath('//*[@class="cdk-overlay-pane"]/div/mat-option['+str(idx +1)+']')).perform()            
    except Exception as e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, e)



def select_option_bo_dau_phan_loai(driver,xpath_select,xpath_options,input_option,timeout=1):
    "chọn phân loại hồ sơ 600"
    time.sleep(1)
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(xpath_select))
    time.sleep(timeout)
    for i in driver.find_elements_by_xpath(xpath_options):
        # print(regex.sub(r'\s','_',str(unidecode(i.text)).lower().strip()))
        # print(regex.sub(r'\s','_',str(unidecode(input_option)).lower().strip()))
        if input_option == 'tang_muc_dong':
            input_option = 'tang_tien_luong'
        if input_option == 'giam_muc_dong':
            input_option = 'giam_tien_luong'

        if regex.sub(r'\s','_',str(unidecode(i.text)).lower().strip()) == (input_option).lower().strip():
            # print(i.text)
            driver.execute_script("arguments[0].click();", i)
            break

def kekhai_bhxh(driver,input_manghiepvu,input_thang=1,input_nam=2021,input_soluong=2,input_dinhkem=True):
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
                select_xpath_options(driver,'//bhxh-month-year/div[1]/mat-form-field[1]/div[1]/div[1]/div[1]/mat-select[1]/div[1]/div[1]/span/span','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option',"Tháng "+str(input_thang).strip())
                time.sleep(2)
                # Nhập năm
                driver.find_element_by_xpath('//bhxh-month-year/div[1]/mat-form-field[2]/div[1]/div[1]/div[1]/input').clear()
                time.sleep(1)
                driver.find_element_by_xpath('//bhxh-month-year/div[1]/mat-form-field[2]/div[1]/div[1]/div[1]/input').send_keys(str(input_nam).strip())

                # driver.execute_script("arguments[0].value = '" + str(input_nam).strip() +"'",driver.find_element_by_xpath('//bhxh-month-year/div[1]/mat-form-field[2]/div[1]/div[1]/div[1]/input'))

                # # Nhập số lượng
                # driver.execute_script("arguments[0].value = '" + str(input_soluong).strip() +"'",driver.find_element_by_xpath('//*[@placeholder="Số lần kê khai nhận giá trị từ 01 đến 99"]'))

                # Bỏ tích đính kèm
                if input_dinhkem == False:
                    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//bhxh-input[3]/div[1]/div[1]/div[2]/div[1]/mat-checkbox[1]/label[1]/div[1]/input'))
                
                # Xác nhận
                driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector('#footer-dialog > button.mat-raised-button.mat-primary'))
                break

def thutuc_bhxh(driver,data_claim,input_thang,input_nam):
    time.sleep(5)
    count_ke_khai = 0
    for i_data_claim in data_claim['socialSecurityProfiles']:
        try:
            if check_selector_element(driver,'body > app-root > ke-khai-layout > div > div > app-thutuc-donvi > div > div > div > button > span'):
                # Chọn lao động
                for i in range(0,5):
                    try:
                        driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector('body > app-root > ke-khai-layout > div > div > app-thutuc-donvi > div > div > div > button > span'))
                        time.sleep(5)
                        # nếu xuất hiện màm hình chọn lao động thì chọn phân loại rồi thoát
                        if check_element(driver,'//*[@id="footer-dialog"]/button[1]/span'):
                            time.sleep(5)
                            break
                    except Exception as e:
                        driver.find_element_by_xpath('//*[@id="footer-dialog"]/button[2]/span').click()
                        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                        LOG_ERROR("THUTUC_BHXH: LỖI")
            else:
                LOG_ERROR("THUTUC_BHXH: KHONG TIM THAY NUT CHON LAO DONG!")
                return False, "THUTUC_BHXH: KHONG TIM THAY NUT CHON LAO DONG!"
            
            if check_element(driver,'//*[@formcontrolname="ten"]'):
                # nhập họ tên nhân viên
                driver.find_element_by_xpath('//*[@formcontrolname="ten"]').send_keys(str(i_data_claim['ho_va_ten']).strip())
                time.sleep(2)
                # chọn tìm kiếm
                driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector('#body-dialog > form > div > div.col-md-7.col-lg-8.col-xl-2.bhxh-label.btn-timkiem > button > span'))
                time.sleep(5)
                # # Chọn nhân viên cần nhập
                # if check_element(driver,'/html/body/div[2]/div[2]/div/mat-dialog-container/app-dialog-chon-lao-dong/div/div[2]/div/table/tbody/tr[1]'):
                #     pass
                list_checkbox = driver.find_elements_by_xpath('//*[@id="body-dialog"]/div/table/tbody/tr[*]/td[2]')
                list_masobhxh = driver.find_elements_by_xpath('//*[@id="body-dialog"]/div/table/tbody/tr[*]/td[7]')
                for idx_masobhxh, i_masobhxh in enumerate(list_masobhxh):
                    time.sleep(1)
                    # nếu giống số BHXH thì click vào ô checkbox
                    if str(i_data_claim['so_so_bhxh']).strip() == "" or str(i_data_claim['so_so_bhxh']).strip() == "0":
                        LOG_ERROR("THUTUC_BHXH: NHÂN VIÊN "+str(i_data_claim['ho_va_ten']) + " KHÔNG CÓ MÃ SỐ BHXH!")
                        return False, str(i_data_claim['ho_va_ten']) + " KHÔNG CÓ MÃ SỐ BHXH"
                    if str(i_masobhxh.text).strip() == str(i_data_claim['so_so_bhxh']).strip():
                        list_checkbox[idx_masobhxh].click()
                        time.sleep(1)
                        break
                    if idx_masobhxh == len(list_masobhxh)-1:
                        LOG_ERROR("THUTUC_BHXH: KHONG TIM THAY NHAN VIEN! "+str(i_data_claim['ho_va_ten']))
                        return False, str(i_data_claim['ho_va_ten'])
                        
                time.sleep(5)
                
                # chọn phân loại
                select_option_bo_dau_phan_loai(driver,'//*[@class="col-md-3"]/mat-form-field/div/div//div/mat-select','//*[@class="mat-select-content ng-trigger ng-trigger-fadeInContent"]/mat-option/span',data_claim['loai_ho_so_type'])
                
                btn_Apdung = driver.find_element_by_xpath('//*[@id="footer-dialog"]/button[1]')
                driver.execute_script("arguments[0].click();", btn_Apdung)     
                
                time.sleep(5)
                check_element(driver,'//*[@class="table-box table-height"]/div/div/table/tbody/tr/td[4]/p')
                
                # check mã số BHXH form kê khai thông tin == mã số BHXH HS nhân viên
                element_TT_BHXH = driver.find_elements_by_xpath('//*[@class="table-box table-height"]/div/div/table/tbody/tr/td[4]/p')
                time.sleep(1)
                for idx_element, ele_BHXH in enumerate(element_TT_BHXH):
                    if str(ele_BHXH.text).strip() == str(i_data_claim['so_so_bhxh']).strip():
                        driver.execute_script("arguments[0].click();", ele_BHXH)
                        time.sleep(1)
                        break

                # Form kê khai thông tin
                time.sleep(2)
                check_element(driver,'//*[@class="cl-B ng-star-inserted"]/bhxh-input/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div/div/input')
                # select chọn phương án
                time.sleep(2)
                select_xpath_options_phuong_an(driver,'//*[@class="cl-B ng-star-inserted"]/bhxh-input/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div/div/input','//*[@class="cdk-overlay-pane"]/div/mat-option', input_option= data_claim["loai_ho_so_sub"])
                time.sleep(3)
                
                # nhập CMND
                if i_data_claim['so_cmnd_hc'] != "":
                    input_CMND = driver.find_element_by_xpath('//*[@class="cl-5 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
                    driver.execute_script("arguments[0].click();", input_CMND)
                    input_CMND.clear()
                    input_CMND.send_keys(str(i_data_claim['so_cmnd_hc']).strip())
                    time.sleep(1)

                # # nhập mã BHXH
                # if i_data_claim['so_cmnd_hc'] != "":
                #      /html/body/app-root/ke-khai-layout/div/div/app-thutuc-donvi/div/div/form/mat-tab-group/div/mat-tab-body[1]/div/div/app-load-to-khai-donvi/div/app-do2-ts/div/div[2]/div/div/table/tbody/tr[3]/td[4]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div/input
                #     input_CMND = driver.find_element_by_xpath('//*[@class="cl-5 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
                #     driver.execute_script("arguments[0].click();", input_CMND)
                #     input_CMND.clear()
                #     input_CMND.send_keys(str(i_data_claim['so_cmnd_hc']).strip())
                #     time.sleep(1)
                
                # nhập chức vụ điều chỉnh
                if i_data_claim['chuc_vu_moi'] != "":
                    input_chuc_vu_dieu_chinh = driver.find_element_by_xpath('//*[@class="cl-6 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/textarea')
                    driver.execute_script("arguments[0].click();",input_chuc_vu_dieu_chinh )
                    input_chuc_vu_dieu_chinh.clear()
                    input_chuc_vu_dieu_chinh.send_keys(str(i_data_claim['chuc_vu_moi']).strip())
                    time.sleep(1)
                
                if i_data_claim['muc_luong_moi'] != "":
                    input_Phucapluong = driver.find_element_by_xpath('//*[@class="cl-19 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/input')
                    driver.execute_script("arguments[0].click();", input_Phucapluong)
                    input_Phucapluong.clear()
                    input_Phucapluong.send_keys(str(i_data_claim['muc_luong_moi']).strip())

                # Ghi chú
                if i_data_claim['comment'] != "" and i_data_claim['comment'] != None:
                    input_ghi_chu = driver.find_element_by_xpath('//*[@class="cl-36 ng-star-inserted"]/bhxh-input/div/div/div/mat-form-field/div/div/div/textarea')
                    driver.execute_script("arguments[0].click();", input_ghi_chu)
                    input_ghi_chu.clear()
                    input_ghi_chu.send_keys(str(i_data_claim['comment']).strip())
                    time.sleep(1)
                count_ke_khai +=1
    
            else:
                LOG_ERROR("THUTUC_BHXH: KHONG TIM THAY HO TEN!")
        except Exception as e:
            LOG_INFO('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, e)
            return False, i_data_claim['ho_va_ten']

    # CLICK QUA TỜ KHAI TK1-TS
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('/html/body/app-root/ke-khai-layout/div/div/app-thutuc-donvi/div/div/form/mat-tab-group/mat-tab-header/div[2]/div/div/div[2]'))
    count_tk = 0
    list_ele_so_bhxh = driver.find_elements_by_xpath('/html/body/app-root/ke-khai-layout/div/div/app-thutuc-donvi/div/div/form/mat-tab-group/div/mat-tab-body[2]/div/div/app-load-to-khai-donvi/div/app-tk1-ts/div[2]/div/div/div/table/tbody/tr[*]/td[2]')
    time.sleep(1)
    for idx_bhxh,ele_BHXH in enumerate(list_ele_so_bhxh):
        try:
            # click vào Nơi DK KCB element của mỗi người

            if str(ele_BHXH.text).strip() == str(data_claim['socialSecurityProfiles'][idx_bhxh]['so_so_bhxh']).strip() and str(data_claim['socialSecurityProfiles'][idx_bhxh]['noi_dk_kcb_ban_dau_tinh']).strip() != "" and str(data_claim['socialSecurityProfiles'][idx_bhxh]['noi_dk_kcb_ban_dau_benh_vien']).strip() != "":
                driver.execute_script("arguments[0].click();", ele_BHXH)
                # click tinh thanh
                ele_tinh_thanh  = driver.find_element_by_xpath('//*[@class="table-holder table-height"]/table/tbody/tr/td[15]/bhxh-input/div/div/div/div/dia-chi-kcb/div/mat-form-field[1]/div/div/div/input')
                ele_tinh_thanh.click()
                # select  tỉnh thành
                list_Tinhthanh = driver.find_elements_by_xpath('//*[@class="cdk-overlay-container"]/div/div/div/mat-option/span/span/span')
                str_tinh_thanh = regex.sub(r'\s','_',str(unidecode(data_claim['socialSecurityProfiles'][idx_bhxh]['noi_dk_kcb_ban_dau_tinh'].lower().strip()))) 
                for ele_tinh_thanh in list_Tinhthanh:
                    str_ele = regex.split(r' - ',str(unidecode(str(ele_tinh_thanh.text).lower().strip())))[1]
                    str_element = regex.sub(r'\s','_',str(str_ele))
                    if str_element == str_tinh_thanh:
                        driver.execute_script("arguments[0].click();", ele_tinh_thanh)
                        time.sleep(1)
                        break

                ele_benh_vien = driver.find_element_by_xpath('//*[@class="table-holder table-height"]/table/tbody/tr/td[15]/bhxh-input/div/div/div/div/dia-chi-kcb/div/mat-form-field[2]/div/div/div/input')
                ele_benh_vien.click()
                list_benh_vien = driver.find_elements_by_xpath('//*[@class="cdk-overlay-container"]/div/div/div/mat-option/span/span/span')
                str_benh_vien = regex.sub(r'\s','_',str(unidecode(data_claim['socialSecurityProfiles'][idx_bhxh]['noi_dk_kcb_ban_dau_benh_vien'].lower().strip()))) 
                for ele_benh_vien in list_benh_vien:
                    str_element = regex.sub(r'\s','_',str(unidecode(str(ele_benh_vien.text))).lower().strip())
                    if str_element == str_benh_vien:
                        driver.execute_script("arguments[0].click();", ele_benh_vien)
                        time.sleep(1)
                        break
                       
            # số sổ hộ gia đình đã cấp 
            if data_claim['socialSecurityProfiles'][idx_bhxh]['so_ho_gia_dinh_da_cap'] != None :
                ele_so_so_hgd = driver.find_element_by_xpath('/html/body/app-root/ke-khai-layout/div/div/app-thutuc-donvi/div/div/form/mat-tab-group/div/mat-tab-body[2]/div/div/app-load-to-khai-donvi/div/app-tk1-ts/div[2]/div/div/div/table/tbody/tr['+str(idx_bhxh+1)+']/td[14]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div/input')
                ele_so_so_hgd.click()
                ele_so_so_hgd.clear()       
                ele_so_so_hgd.send_keys(str(data_claim['socialSecurityProfiles'][idx_bhxh]['so_ho_gia_dinh_da_cap']).strip())
                time.sleep(1)

            # muc tien dong
            if data_claim['socialSecurityProfiles'][idx_bhxh]['muc_tien_dong'] != "" :
                ele_muc_tien = driver.find_element_by_xpath('/html/body/app-root/ke-khai-layout/div/div/app-thutuc-donvi/div/div/form/mat-tab-group/div/mat-tab-body[2]/div/div/app-load-to-khai-donvi/div/app-tk1-ts/div[2]/div/div/div/table/tbody/tr['+str(idx_bhxh+1)+']/td[16]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div/input')
                ele_muc_tien.click()
                ele_muc_tien.clear()
                ele_muc_tien.send_keys(str(data_claim['socialSecurityProfiles'][idx_bhxh]['muc_tien_dong']).strip())
                time.sleep(1)

            # phuong thuc dong
            if data_claim['socialSecurityProfiles'][idx_bhxh]['phuong_thuc_dong'] != "":
                # //*[@formcontrolname="Phuongthuc"]/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div/div/input
                ele_phuong_thuc_dong = driver.find_element_by_xpath('/html/body/app-root/ke-khai-layout/div/div/app-thutuc-donvi/div/div/form/mat-tab-group/div/mat-tab-body[2]/div/div/app-load-to-khai-donvi/div/app-tk1-ts/div[2]/div/div/div/table/tbody/tr['+str(idx_bhxh+1)+']/td[17]/bhxh-input/div/div/div/div/bhxh-autocomplete-input/mat-form-field/div/div[1]/div/input')
                ele_phuong_thuc_dong.click()
                time.sleep(1)
                # List Phuong thuc dong:   //*[@class="cdk-overlay-container"]/div/div/div/mat-option/span/span/span
                list_elements = driver.find_elements_by_xpath('//*[@class="cdk-overlay-container"]/div/div/div/mat-option/span/span/span')
                input_new = regex.sub(r'\s','_',str(unidecode(str(data_claim['socialSecurityProfiles'][idx_bhxh]['phuong_thuc_dong']))).lower().strip())
                for i_ele in list_elements:
                    str_ele = regex.split(r' - ',str(unidecode(str(i_ele.text))))[1].lower().strip()
                    str_ele_new = regex.sub(r'\s','_',str(str_ele))
                    if str_ele_new == input_new:
                        driver.execute_script("arguments[0].click();", i_ele)
                        time.sleep(1)
                        break

            # noi dung thay doi yeu cau
            if data_claim['socialSecurityProfiles'][idx_bhxh]['noi_dung_thay_doi_yeu_cau'] != "" :
                # //*[@formcontrolname="noiDung_ThayDoi"]/div/div/div/mat-form-field/div/div/div/textarea
                # ele_thay_doi = driver.find_element_by_xpath('/html/body/app-root/ke-khai-layout/div/div/app-thutuc-donvi/div/div/form/mat-tab-group/div/mat-tab-body[2]/div/div/app-load-to-khai-donvi/div/app-tk1-ts/div[2]/div/div/div/table/tbody/tr['+str(count_thay_doi)+']/td[18]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div/textarea')
                ele_thay_doi = driver.find_element_by_xpath('//*[@formcontrolname="noiDung_ThayDoi"]/div/div/div/mat-form-field/div/div/div/textarea')
                ele_thay_doi.click()
                ele_thay_doi.clear()
                ele_thay_doi.send_keys(str(data_claim['socialSecurityProfiles'][idx_bhxh]['noi_dung_thay_doi_yeu_cau']).strip())
                time.sleep(1)
            
            # sdt liên hệ
            if data_claim['socialSecurityProfiles'][idx_bhxh]['sdt_lien_he'] != None:
                ele_sdt = driver.find_element_by_xpath('/html/body/app-root/ke-khai-layout/div/div/app-thutuc-donvi/div/div/form/mat-tab-group/div/mat-tab-body[2]/div/div/app-load-to-khai-donvi/div/app-tk1-ts/div[2]/div/div/div/table/tbody/tr['+str(idx_bhxh+1)+']/td[11]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div/input')
                ele_sdt.click()
                ele_sdt.clear()
                ele_sdt.send_keys(str(data_claim['socialSecurityProfiles'][idx_bhxh]['sdt_lien_he']).strip())
                time.sleep(1)
            
            # email
            if data_claim['socialSecurityProfiles'][idx_bhxh]['email'] != "":
                ele_mail = driver.find_element_by_xpath('/html/body/app-root/ke-khai-layout/div/div/app-thutuc-donvi/div/div/form/mat-tab-group/div/mat-tab-body[2]/div/div/app-load-to-khai-donvi/div/app-tk1-ts/div[2]/div/div/div/table/tbody/tr['+str(idx_bhxh+1)+']/td[12]/bhxh-input/div/div/div/mat-form-field/div/div[1]/div/input')
                ele_mail.click()
                ele_mail.clear()
                ele_mail.send_keys(str(data_claim['socialSecurityProfiles'][idx_bhxh]['email']).strip())
                time.sleep(1)

            count_tk +=1
        except Exception as e:
            LOG_ERROR(str(e))
            return False, data_claim['socialSecurityProfiles'][idx_bhxh]['ho_va_ten']

    # Lưu kê khai
    if count_ke_khai == len(data_claim['socialSecurityProfiles']) and count_tk == len(data_claim['socialSecurityProfiles']) :
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@class="row Gui-chung-tu"]/div[1]/button[1]'))
        time.sleep(10)
        str_url = driver.current_url
        if "thu-tuc-don-vi" in str_url:
            input_dotkekhai = regex.findall(r'(?<=\d{2}-\d{4}\/)\d{1,2}',str_url)[0]
            input_kykekhai = regex.findall(r'\d{2}-\d{4}',str_url)[0]
            input_kykekhai = regex.sub(r'-','/',input_kykekhai)
            str_note = "600"+"|"+input_dotkekhai+"|"+input_kykekhai
            list_note = regex.split(r'\|',str_note)
            str_Mathutuc = str(list_note[0])
            str_Dotkekhai = str(list_note[1]).strip()
            str_Kykekhai = str(list_note[2]).strip().replace("/", "-")
            str_Macoquan = macoquan_bhxh(driver)
            if check_bhxh(driver,str_Macoquan,str_Mathutuc,str_Dotkekhai,str_Kykekhai,data_claim):
                LOG_INFO("HỒ SƠ: " +str(data_claim['ten_ho_so']).strip()+" KÊ KHAI THÀNH CÔNG")
                return True, str_note
            else:
                LOG_INFO("HỒ SƠ: " +str(data_claim['ten_ho_so']).strip()+" KÊ KHAI THẤT BẠI")
                return False, 'Tạo thất bại'
        else:
            return False, 'Chưa tạo được'
    else:
        return False, 'Chưa tạo được'

def macoquan_bhxh(driver):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get("https://dichvucong.baohiemxahoi.gov.vn/#/tai-khoan")
    str_Macoquan = driver.find_element_by_xpath('//*[@class="col-md-12"]/div[4]/div/mat-form-field/div/div/div/input').get_attribute('value').strip()
    driver.execute_script("window.close('');")   # Close tab
    driver.switch_to.window(driver.window_handles[0])
    return str_Macoquan

def check_bhxh(driver,str_Macoquan,str_Mathutuc,str_Dotkekhai,str_Kykekhai,data_claim):
    pass
    # Switch to tab the new window
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])

    time.sleep(5)
    # get page thông tin hồ sơ từng NV
    driver.get("https://dichvucong.baohiemxahoi.gov.vn/#/ke-khai/thu-tuc-don-vi/" +str(str_Mathutuc)+ "/ke-khai/"+str(str_Macoquan)+"/"+ str_Kykekhai+ "/" +str_Dotkekhai) 
    

    if check_element(driver,'//*[@class="table-box table-height"]/div/div/table/tbody/tr/td[4]/p',60):
        pass
    
    # check mã số BHXH form == mã số BHXH HS terra
    element_TT_BHXH = driver.find_elements_by_xpath('//*[@class="table-box table-height"]/div/div/table/tbody/tr/td[4]/p')
    time.sleep(1)
    for idx_element, ele_BHXH in enumerate(element_TT_BHXH):
        if str(ele_BHXH.text).strip() == str(data_claim['socialSecurityProfiles'][0]['so_so_bhxh']).strip():
            LOG_INFO("Check id_card_number => True")
            driver.execute_script("window.close('');")   # Close tab
            driver.switch_to.window(driver.window_handles[0])
            return True
        
    LOG_INFO("Check id_card_number => False")
    driver.execute_script("window.close('');")   # Close tab
    driver.switch_to.window(driver.window_handles[0])
    return False

def quatrinhnop_bhxh(driver):
    "Get thông tin các bước xử lí Hồ sơ"
    
    # Test dữ liệu
    dct_All = {"form":[]}

    dct_table = { "Bước": "",
            "Tên cơ quan": "",
            "Phòng ban xử lý": "",
            "Thời gian gửi":"",
            "Trạng thái hồ sơ":"",
            "Desc": []         
        }
    dict_con = {
                "STT": [],
                "Cán bộ xử lý":[],
                "Hành động": [],
                "Thời gian xử lý":[],
                }

    button_arrow = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[1]')
    hd_Buoc = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[2]')
    hd_Tencoquan = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[3]')
    hd_Phongbanxuly = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[4]')
    hd_Thoigiangui = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[5]')
    hd_Trangthaihoso = driver.find_elements_by_xpath('//*[@class="table-body ng-star-inserted"]/div/div[6]')

    # for từng bước 
    for idx_button_arrow, i_button_arrow in enumerate(button_arrow) :

        dct_table['Bước'] = hd_Buoc[idx_button_arrow].text
        dct_table['Tên cơ quan'] = hd_Tencoquan[idx_button_arrow].text
        dct_table['Phòng ban xử lý'] = hd_Phongbanxuly[idx_button_arrow].text
        dct_table['Thời gian gửi'] = hd_Thoigiangui[idx_button_arrow].text
        dct_table['Trạng thái hồ sơ'] = hd_Trangthaihoso[idx_button_arrow].text

        i_button_arrow.click()
        time.sleep(2)

        # element_rowTr = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]')
        # element_rowTd = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td')
        ele_STT = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[1]')
        ele_Canboxuly = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[2]')
        ele_Hanhdong = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[3]')
        ele_Thoigianxuly = driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[4]')

        # for STT mỗi bước 
        for idx, stt in enumerate(ele_STT):
            dict_con['STT'].append(stt.text)
            dict_con['Cán bộ xử lý'].append(ele_Canboxuly[idx].text)
            dict_con['Hành động'].append(ele_Hanhdong[idx].text)
            dict_con['Thời gian xử lý'].append(ele_Thoigianxuly[idx].text)
        time.sleep(2)

        # dict_con["STT"].append(i.text for i in (driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[1]')))
        # dict_con["Cán bộ xử lý"].append(i.text for i in (driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[2]')))
        # dict_con["Hành động"].append(i.text for i in (driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[3]')))
        # dict_con["Thời gian xử lý"].append(i.text for i in (driver.find_elements_by_xpath('//*[@class="table responsive-table"]/tbody/tr[*]/td[4]')))
        
        dct_table["Desc"].append(dict_con)
        dct_All["form"].append(dct_table)
        i_button_arrow.click()
        time.sleep(2)

        
        dict_con = {
            'STT': [],
            'Cán bộ xử lý':[],
            'Hành động': [],
            'Thời gian xử lý':[],
            }

        dct_table = { 'Bước': '',
                'Tên cơ quan': '',
                'Phòng ban xử lý': '',
                'Thời gian gửi':'',
                'Trạng thái hồ sơ':'',
                'Desc': [],           
            } 
    try:              
        btn_dong = driver.find_element_by_xpath('//*[@class="cdk-overlay-pane"]/mat-dialog-container/app-dialog-qua-trinh-xu-ly/div/div[3]/button')
        btn_dong.click()
        # driver.execute_script("arguments[0].click();", btn_dong)
        time.sleep(2)
    except Exception as e:
        print("chua co nut dong" + e)

    return dct_All

def job_kekhai():
    try:
        LOG_INFO("CHẠY QUY TRÌNH KÊ KHAI")
        #Lấy access_token để sử dụng api.
        rq_login_terra = login_terra()
        if rq_login_terra.get('data'):
            access_token_terra = rq_login_terra['data']['login']['access_token']
            # LOG_INFO("LOGIN_TERRA: LẤY ACCESS TOKEN THÀNH CÔNG")
        else:
            LOG_ERROR("LOGIN_TERRA: KHÔNG LẤY ĐƯỢC ACCESS TOKEN!")
            return

        #Lấy danh sách các khách hàng của tài khoản.
        rq_get_clients_terra = get_clients_terra(access_token_terra)
        if rq_get_clients_terra.get('data'):
            list_clients_terra = rq_get_clients_terra['data']['clients']['data']
            # LOG_INFO("CLIENT_TERRA: LẤY DANH SÁCH KHÁCH HÀNG THÀNH CÔNG")
        else:
            LOG_ERROR("CLIENT_TERRA: LỖI KHÔNG LẤY ĐƯỢC DANH SÁCH KHÁCH HÀNG!")
            return

        #For từng khách hàng để truy vấn danh sách hồ sơ.
        for i_client_terra in list_clients_terra:
            try:
                id_client = i_client_terra['id']
                code_client = i_client_terra['code']
                rq_get_socialSecurityProfileRequests_terra = get_socialSecurityProfileRequests(id_client,access_token_terra)
                if rq_get_socialSecurityProfileRequests_terra.get('data'):
                    list_socialSecurityProfileRequests = rq_get_socialSecurityProfileRequests_terra['data']['socialSecurityProfileRequests']['data']
                    
                    # #Chạy test
                    if "VPĐD HANKYU HANSHIN PROPERTIES CORP. TẠI TP HỒ CHÍ MINH" not in i_client_terra['company_name']:
                        continue

                    #For từng hồ sơ để xử lý
                    LOG_INFO("CLAIMS_TERRA: LẤY DANH SÁCH HỒ SƠ - "+i_client_terra['company_name'])
                    for i_socialSecurityProfile in list_socialSecurityProfileRequests:
                        if i_socialSecurityProfile['tinh_trang_giai_quyet_ho_so'] == "da_phe_duyet_noi_bo" :
                            pass
                        else:
                            continue
                        # print(i_socialSecurityProfile)
                        rq_data_socialSecurityProfileRequests = rq_socialSecurityProfileRequests(i_socialSecurityProfile['id'],access_token_terra)
                        if rq_data_socialSecurityProfileRequests.get('data'):
                            data_claim = rq_data_socialSecurityProfileRequests['data']['socialSecurityProfileRequest']
                        LOG_INFO("EMPLOYEE_TERRA: LẤY THÔNG TIN HỒ SƠ - "+i_socialSecurityProfile['ten_ho_so'])
                        
                        r_result = post_service({"name_claim":i_socialSecurityProfile['id'], "data_claim":data_claim, "company_claim":code_client, "status_claim":"Wait"})
                        if r_result.get('name_claim')[0] == 'claim with this name claim already exists.':
                            continue

                    list_Claim_Company = get_service(code_client)
                    list_Claim_Company = [x for x in list_Claim_Company if x['status_claim'] == 'Wait']
                    LOG_INFO("Số lượng hồ sơ cần kê khai: "+str(len(list_Claim_Company)))
                    if len(list_Claim_Company) != 0:
                        try:
                            mydb = mysql.connector.connect(
                            host=data_security['host_mysql'],
                            user=data_security['user_mysql'],
                            passwd=data_security['passwd_mysql'],
                            database=data_security['database_mysql'])

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
                        driver = open_brower()           
                        login_bhxh(driver,myresult[2],myresult[3],myresult[4])
                        driver.get("https://dichvucong.baohiemxahoi.gov.vn/")
                        str_Note = ''
                        for i_Claim_Company in list_Claim_Company:
                            try:
                                data_claim = i_Claim_Company['data_claim']
                                input_thang = int(regex.split(r'-',data_claim['loai_ho_so_from_date'])[1])
                                input_nam = int(regex.split(r'-',data_claim['loai_ho_so_to_date'])[0])
                                kekhai_bhxh(driver,"600",str(input_thang),str(input_nam),1)
                                bl_return, str_Note = thutuc_bhxh(driver,data_claim,str(input_thang),str(input_nam))
                                LOG_INFO(str_Note)
                                if bl_return:                                    
                                    input_data_claim = data_claim.copy()
                                    del input_data_claim['id']
                                    del input_data_claim['client_id']
                                    del input_data_claim['created_at']
                                    del input_data_claim['updated_at']
                                    del input_data_claim['media_path']
                                    del input_data_claim['mediaTemp']
                                    del input_data_claim['status']
                                    del input_data_claim['__typename']
                                    employees = input_data_claim['socialSecurityProfiles']
                                    del input_data_claim['socialSecurityProfiles']
                                    input_data_claim['employees'] = employees
                                    for i_claim in input_data_claim['employees']:
                                        del i_claim['mediaTemp']
                                        del i_claim['__typename']
                                    data_input = {}
                                    data_input['id'] = data_claim['id']
                                    data_input['input'] = input_data_claim
                                    data_input['input']['client_id'] = data_claim['client_id']
                                    data_input['input']['ngay_ke_khai_va_luu_tam_ho_so'] = datetime.datetime.now().strftime("%Y-%m-%d")
                                    data_input['input']['tinh_trang_giai_quyet_ho_so'] = "da_ke_khai_va_luu_tam_ho_so"
                                    data_input['input']['note'] = "Robot đã cập nhật ngay_ke_khai_va_luu_tam_ho_so"

                                    LOG_INFO(update_SocialSecurityProfileRequests_terra(data_input,access_token_terra))
                                    LOG_INFO("HỒ SƠ LƯU TẠM "+str(str_Note)+" CẬP NHẬT TERRA")

                                    LOG_INFO(patch_service(i_Claim_Company['id'],{"status_claim":"Running", "note_claim":str(str_Note), "status_process_claim": "Đã kê khai và lưu tạm hồ sơ"}))
                                    LOG_INFO("HỒ SƠ LƯU TẠM "+str(str_Note)+" CẬP NHẬT LƯU TRỮ")

                                else:
                                    patch_service(i_Claim_Company['id'],{"status_claim":"Error","note_claim":str(str_Note)})
                                    LOG_ERROR("HỒ SƠ LỖI "+str(str_Note)+" CẬP NHẬT LƯU TRỮ")

                                    data_input = process_data_terra(data_claim)
                                    data_input['input']['note'] = "HỒ SƠ LỖI: " + str(str_Note)
                                    update_SocialSecurityProfileRequests_terra(data_input, access_token_terra)
                                    LOG_INFO("HỒ SƠ LỖI: " +str(str_Note)+" CẬP NHẬT TERRA")

                            except Exception as e:
                                LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                                patch_service(i_Claim_Company['id'],{"status_claim":"Error","note_claim":str(str_Note)})
                                LOG_ERROR("HỒ SƠ LỖI"+str(str_Note)+" CẬP NHẬT LƯU TRỮ")
                                driver.quit()

                                data_input = process_data_terra(data_claim)
                                data_input['input']['note'] = "HỒ SƠ LỖI: " + str(str_Note)
                                update_SocialSecurityProfileRequests_terra(data_input, access_token_terra)
                                LOG_INFO("HỒ SƠ LỖI: " +str(str_Note)+" CẬP NHẬT TERRA")

                        driver.quit()
            except Exception as e:
                LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

def format_datetime(str_input):
    try:
        str_ngaykekhai = regex.findall(r"\d{2}\/\d{2}\/\d{4}",str_input)[0]
        str_ngaykekhai = regex.split(r'\/',str_ngaykekhai)
        return str_ngaykekhai[2]+"-"+str_ngaykekhai[1]+"-"+str_ngaykekhai[0]
    except Exception as e:
        LOG_INFO(e)
        return ''

def job_quet():
    try:
        #Lấy access_token để sử dụng api.
        LOG_INFO("CHẠY QUY TRÌNH QUÉT KẾT QUẢ")
        rq_login_terra = login_terra()
        if rq_login_terra.get('data'):
            access_token_terra = rq_login_terra['data']['login']['access_token']
            # LOG_INFO("LOGIN_TERRA: LẤY ACCESS TOKEN THÀNH CÔNG")
        else:
            LOG_ERROR("LOGIN_TERRA: KHÔNG LẤY ĐƯỢC ACCESS TOKEN!")
            return

        #Lấy danh sách các khách hàng của tài khoản.
        rq_get_clients_terra = get_clients_terra(access_token_terra)
        if rq_get_clients_terra.get('data'):
            list_clients_terra = rq_get_clients_terra['data']['clients']['data']
            # LOG_INFO("CLIENT_TERRA: LẤY DANH SÁCH KHÁCH HÀNG THÀNH CÔNG")
        else:
            LOG_ERROR("CLIENT_TERRA: LỖI KHÔNG LẤY ĐƯỢC DANH SÁCH KHÁCH HÀNG!")
            return

        #For từng khách hàng để truy vấn danh sách hồ sơ.
        for i_client_terra in list_clients_terra:
            try:
                id_client = i_client_terra['id']
                code_client = i_client_terra['code']
                rq_get_socialSecurityProfileRequests_terra = get_socialSecurityProfileRequests(id_client,access_token_terra)
                if rq_get_socialSecurityProfileRequests_terra.get('data'):
                    list_socialSecurityProfileRequests = rq_get_socialSecurityProfileRequests_terra['data']['socialSecurityProfileRequests']['data']
                    
                    # # #Chạy test
                    if "VPĐD HANKYU HANSHIN PROPERTIES CORP. TẠI TP HỒ CHÍ MINH" not in i_client_terra['company_name']:
                        continue

                    #For từng hồ sơ để xử lý
                    LOG_INFO("CLAIMS_TERRA: LẤY DANH SÁCH HỒ SƠ - "+i_client_terra['company_name'])
                    for i_socialSecurityProfile in list_socialSecurityProfileRequests:
                        if i_socialSecurityProfile['tinh_trang_giai_quyet_ho_so'] == "da_phe_duyet_noi_bo" :
                            pass
                        else:
                            continue
                        rq_data_socialSecurityProfileRequests = rq_socialSecurityProfileRequests(i_socialSecurityProfile['id'],access_token_terra)
                        if rq_data_socialSecurityProfileRequests.get('data'):
                            data_claim = rq_data_socialSecurityProfileRequests['data']['socialSecurityProfileRequest']
                        LOG_INFO("EMPLOYEE_TERRA: LẤY THÔNG TIN HỒ SƠ - "+i_socialSecurityProfile['ten_ho_so'])
                        
                        r_result = post_service({"name_claim":i_socialSecurityProfile['id'], "data_claim":data_claim, "company_claim":code_client, "status_claim":"Wait"})
                        if r_result.get('name_claim')[0] == 'claim with this name claim already exists.':
                            continue

                    list_Claim_Company = get_service(code_client)
                    list_Claim_Company = [x for x in list_Claim_Company if x['status_claim'] == 'Running']
                    LOG_INFO("Số lượng hồ sơ cần quét kết quả: "+str(len(list_Claim_Company)))
                    if len(list_Claim_Company) != 0:
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

                        driver = open_brower()         
                        login_bhxh(driver,myresult[2],myresult[3],myresult[4])
                        driver.get("https://dichvucong.baohiemxahoi.gov.vn/")
                        for i_Claim_Company in list_Claim_Company:
                            try:
                                data_claim = i_Claim_Company['data_claim']
                                input_thang = int(regex.split(r'-',data_claim['loai_ho_so_from_date'])[1])
                                input_nam = int(regex.split(r'-',data_claim['loai_ho_so_from_date'])[0])
                                time.sleep(5)
                                driver.get("https://dichvucong.baohiemxahoi.gov.vn/#/ke-khai/thu-tuc-don-vi/lich-su-ke-khai")
                                time.sleep(5)
                                list_note = regex.split("\|",str(i_Claim_Company['note_claim']))
                                input_thang = regex.split("\/",list_note[-1])[0]
                                input_nam = regex.split("\/",list_note[-1])[1]
                                #Search 
                                driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[1]/div/div[2]/mat-form-field/div/div[1]/div/input").clear()
                                driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[1]/div/div[2]/mat-form-field/div/div[1]/div/input").send_keys(str(int(input_thang)))
                                driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[1]/div/div[3]/mat-form-field/div/div[1]/div/input").clear()
                                driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[1]/div/div[3]/mat-form-field/div/div[1]/div/input").send_keys(str(int(input_nam)))
                                driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[2]/div/div[2]/mat-form-field/div/div[1]/div/input").clear()
                                driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[2]/div/div[2]/mat-form-field/div/div[1]/div/input").send_keys(str(list_note[1]))
                                

                                select_xpath_options(driver, '//*[@placeholder="Chọn mã thủ tục" and @aria-label="Chọn mã thủ tục"]',  "/html/body/div[3]/div[2]/div/div/div/mat-option[*]", "600")
                                time.sleep(1)
                                driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[6]/button").click()
                                time.sleep(5)

                                driver.find_element_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/div/form/div/div[6]/button").click()
                                time.sleep(5)
 
                                list_MATHUTUC = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[2]")
                                list_SOHOSO = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[3]")
                                list_DOTKEKHAI = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[4]")
                                list_KYKEKHAI = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[5]")
                                list_NGAYKEKHAI = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[6]")
                                list_TRANGTHAI = driver.find_elements_by_xpath("/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr[*]/td[7]")
                                for idx_NGAYKEKHAI, i_NGAYKEKHAI in enumerate(list_NGAYKEKHAI):
                                    str_note = regex.split("\|",str(i_Claim_Company['note_claim']))
                                    if list_MATHUTUC[idx_NGAYKEKHAI].text == str(str_note[0]) and list_DOTKEKHAI[idx_NGAYKEKHAI].text == str(str_note[1]) and list_KYKEKHAI[idx_NGAYKEKHAI].text == str(str_note[2]):
                                        str_Macoquan = macoquan_bhxh(driver)
                                        str_Mathutuc = str(str_note[0])
                                        str_Dotkekhai = str(str_note[1]).strip()
                                        str_Kykekhai = str(str_note[2]).strip().replace("/", "-")
                                        if check_bhxh(driver,str_Macoquan,str_Mathutuc,str_Dotkekhai,str_Kykekhai,data_claim):
                                            rq_data_socialSecurityProfileRequests = rq_socialSecurityProfileRequests(i_Claim_Company['name_claim'],access_token_terra)
                                            i_socialSecurityProfile = rq_data_socialSecurityProfileRequests['data']['socialSecurityProfileRequest']
                                            input_data_claim = i_socialSecurityProfile.copy()
                                            del input_data_claim['id']
                                            del input_data_claim['client_id']
                                            del input_data_claim['created_at']
                                            del input_data_claim['updated_at']
                                            del input_data_claim['media_path']
                                            del input_data_claim['mediaTemp']
                                            del input_data_claim['status']
                                            del input_data_claim['__typename']
                                            employees = input_data_claim['socialSecurityProfiles']
                                            del input_data_claim['socialSecurityProfiles']
                                            input_data_claim['employees'] = employees
                                            for i_claim in input_data_claim['employees']:
                                                del i_claim['mediaTemp']
                                                del i_claim['__typename']
                                            if list_TRANGTHAI[idx_NGAYKEKHAI].text == "Đã nộp":
                                                if i_Claim_Company['status_process_claim'] == "Đã kê khai và lưu tạm hồ sơ": 
                                                    str_ngaykekhai = format_datetime(i_NGAYKEKHAI.text)
                                                    str_sohosokekhai = list_SOHOSO[idx_NGAYKEKHAI].text
                                                    data_input = {}
                                                    data_input['id'] = data_claim['id']
                                                    data_input['input'] = input_data_claim
                                                    data_input['input']['client_id'] = data_claim['client_id']
                                                    data_input['input']['tinh_trang_giai_quyet_ho_so'] = "da_ky_nop_ho_so_to_co_quan_bhxh"
                                                    data_input['input']['ngay_nop_ho_so'] = str_ngaykekhai
                                                    data_input['input']['so_ho_so_bhxh_da_ke_khai'] = str_sohosokekhai
                                                    data_input['input']['note'] = "Robot đã cập nhật ngay_nop_ho_so + so_ho_so_bhxh_da_ke_khai"

                                                    print(data_input)
                                                    LOG_INFO(update_SocialSecurityProfileRequests_terra(data_input,access_token_terra))
                                                    LOG_INFO("HỒ SƠ LƯU TẠM "+str(i_Claim_Company['note_claim'])+" CẬP NHẬT TERRA")
                                                    
                                                    LOG_INFO(patch_service(i_Claim_Company['id'],{"status_process_claim": "Đã ký nộp hồ sơ và nộp chứng từ cho cơ quan BHXH"}))
                                                    LOG_INFO("HỒ SƠ ĐÃ NỘP "+str(i_Claim_Company['note_claim'])+" CẬP NHẬT LƯU TRỮ")

                                                button_Nop = driver.find_element(By.XPATH,"/html/body/app-root/ke-khai-layout/div/div/app-lich-su-ke-khai/div/table/tbody/tr["+str(idx_NGAYKEKHAI+1)+"]/td[8]/button")
                                                driver.execute_script("arguments[0].click();", button_Nop)
                                                time.sleep(2)
                                                data_tracking = quatrinhnop_bhxh(driver)
                                                bl_DaKetqua = False
                                                str_tracking_service = unidecode(str(i_Claim_Company['tracking_claim']))
                                                str_tracking_service = regex.sub(r"'Trang thai ho so': 'Con \d{1,2} ngay \d{1,2} gio \d{1,2} phut', |'Trang thai ho so': 'Tre han \d{1,2} ngay \d{1,2} gio \d{1,2} phut', ","",str_tracking_service)
                                                str_tracking_bhxh = unidecode(str(data_tracking['form']))
                                                str_tracking_bhxh = regex.sub(r"'Trang thai ho so': 'Con \d{1,2} ngay \d{1,2} gio \d{1,2} phut', |'Trang thai ho so': 'Tre han \d{1,2} ngay \d{1,2} gio \d{1,2} phut', ","",str_tracking_bhxh)
                                                print("a:"+str_tracking_service)
                                                print("b:"+str_tracking_bhxh)

                                                if str_tracking_service != str_tracking_bhxh:
                                                    data_input = {}
                                                    data_input['id'] = data_claim['id']
                                                    data_input['input'] = input_data_claim

                                                    str_bo_phan_tn_tkq_date = ''
                                                    str_bo_phan_tn_tkq_reviewer = ''
                                                    str_bo_phan_cd_bhxh_date = ''
                                                    str_bo_phan_cd_bhxh_reviewer = ''
                                                    str_bo_phan_khtc_date = ''
                                                    str_bo_phan_khtc_reviewer = ''
                                                    for i_data_tracking in data_tracking['form']:
                                                        if "Tiếp nhận và trả kết quả TTHC" in i_data_tracking['Phòng ban xử lý']:
                                                            for i_desc in i_data_tracking['Desc']:
                                                                str_bo_phan_tn_tkq_date = i_desc['Thời gian xử lý'][-1]
                                                                str_bo_phan_tn_tkq_reviewer = i_desc['Cán bộ xử lý'][-1]
                                                                data_input['input']['bo_phan_tn_tkq_date'] = format_datetime(str_bo_phan_tn_tkq_date)
                                                                data_input['input']['bo_phan_tn_tkq_reviewer'] = str_bo_phan_tn_tkq_reviewer

                                                                for i_hanhdong in i_desc['Hành động']:
                                                                    if i_hanhdong == "Trả kết quả":
                                                                        bl_DaKetqua = True
                                                                
                                                        if "Chế độ Bảo hiểm xã hội" in i_data_tracking['Phòng ban xử lý']:
                                                            for i_desc in i_data_tracking['Desc']:
                                                                str_bo_phan_cd_bhxh_date = i_desc['Thời gian xử lý'][-1]
                                                                str_bo_phan_cd_bhxh_reviewer = i_desc['Cán bộ xử lý'][-1]
                                                                data_input['input']['bo_phan_cd_bhxh_date'] = format_datetime(str_bo_phan_cd_bhxh_date)
                                                                data_input['input']['bo_phan_cd_bhxh_reviewer'] = str_bo_phan_cd_bhxh_reviewer
                                                        
                                                        if "Kế hoạch - tài chính" in  i_data_tracking['Phòng ban xử lý']:
                                                            for i_desc in i_data_tracking['Desc']:
                                                                str_bo_phan_khtc_date = i_desc['Thời gian xử lý'][-1]
                                                                str_bo_phan_khtc_reviewer = i_desc['Cán bộ xử lý'][-1]
                                                                data_input['input']['bo_phan_khtc_date'] = format_datetime(str_bo_phan_khtc_date)
                                                                data_input['input']['bo_phan_khtc_reviewer'] = str_bo_phan_khtc_reviewer
                                                    
        
                                                    data_input['input']['tinh_trang_giai_quyet_ho_so'] = "da_xu_ly_tai_co_quan_bhxh"
                                                    str_status_process_claim = "Đang xử lý (tại BHXH)"


                                                    for i_Nop_new in get_list_Nop_new(i_Claim_Company['tracking_claim'],data_tracking['form']):
                                                        list_state = regex.findall("(?<= Bước\: )\d{1,2}|(?<=\| )\d{1,2}",i_Nop_new)
                                                        str_status_process_claim = "x".join(list_state)
                                                        data_input['input']['tinh_trang_giai_quyet_ho_so'] = str_status_process_claim
                                                        data_input['input']['note'] = "Robot cập nhật: "+str(i_Nop_new)
                                                        LOG_INFO(update_SocialSecurityProfileRequests_terra(data_input,access_token_terra))
                                                        time.sleep(2)


                                                    if bl_DaKetqua == True:
                                                        LOG_INFO("HỒ SƠ BHXH TRẢ KẾT QUẢ "+str(i_Claim_Company['note_claim'])+" CẬP NHẬT LƯU TRỮ")
                                                        patch_service(i_Claim_Company['id'],{"status_claim":"Complete"})
                                                        data_input['input']['tinh_trang_giai_quyet_ho_so'] = "da_co_ket_qua"
                                                        str_status_process_claim = "Đã có kết quả"
                                                        data_input['input']['note'] = "Hoàn thành hồ sơ"
                                                        LOG_INFO(update_SocialSecurityProfileRequests_terra(data_input,access_token_terra))

                                                    LOG_INFO(patch_service(i_Claim_Company['id'],{"tracking_claim":data_tracking['form'], "status_process_claim": str_status_process_claim}))
                                                    LOG_INFO("HỒ SƠ BHXH ĐANG XỬ LÝ "+str(i_Claim_Company['note_claim'])+" CẬP NHẬT LƯU TRỮ")

                            except Exception as e:
                                LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                                continue
                        driver.quit()
                        if mydb.is_connected():
                            mycursor.close()
                            mydb.close()

            except Exception as e:
                LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)

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

    LOG_INFO("BẮT ĐẦU CHẠY ROBOT 600")
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
