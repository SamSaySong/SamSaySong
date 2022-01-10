from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from time import sleep
import os, inspect
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path = os.path.abspath(CurDir + "\\data_input\\")

def open_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    prefs = {"credentials_enable_service": False,               #tắt arlert save password chrome
        "profile.password_manager_enabled": False,
        "profile.managed_default_content_settings.images": 2}    # tắt image web 
    chrome_options.add_experimental_option('prefs', prefs)
    #chrome_options.add_argument("--headless") #chạy ngầm browwser
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path= r"D:\Win\Train Python\wwin-01\selenium03\chromedriver.exe",chrome_options=chrome_options)
    return driver

def input():
    df_input = pd.read_excel(path+"\\Data.xlsx", sheet_name= "Sheet1",skiprows=1,engine="openpyxl")
    return df_input

def Main():
    df_input = input()
    driver = open_driver()
    driver.get("https://qlnkt.xyz/")
    #user
    driver.find_element_by_name("username").send_keys("adminvbpo")
    #pass
    driver.find_element_by_name("password").send_keys("Vbpo@12345")
    #login
    driver.find_element_by_class_name("login100-form-btn").click()
    
    Wait = WebDriverWait(driver, 10)
 
    button_NTT = driver.find_elements_by_xpath('//*[@id="accordionSidebar"]/li[1]/a')
    for i,j in enumerate(button_NTT):
        driver.get(j.get_attribute("href"))
    sleep(3)

    #nhập thông tin
    select_TP = Select((driver.find_element_by_id('select_tinh')))
    select_TP.select_by_value("48")
    sleep(3)
    select_Quan = Select((driver.find_element_by_id("select_quan")))
    select_Quan.select_by_value("494")
    sleep(3)
    select_Phuong = Select((driver.find_element_by_id("select_phuong")))
    select_Phuong.select_by_value("20287")
    sleep(3)
    for idx, row in df_input.iterrows():

        #Thông tin chung
        ho_va_ten = driver.find_element_by_name("ho_ten_khai_sinh_nkt")
        ho_va_ten.send_keys(row["Họ và tên"])
        
        khai_sinh = driver.find_element_by_name("noi_dk_khai_sinh")
        khai_sinh.send_keys(row["Nơi đăng kí khai sinh"])

        que_quan = driver.find_element_by_name("que_quan")
        que_quan.send_keys(row["Quê quán"])

        dia_chi_TT = driver.find_element_by_name("dia_chi_thuong_tru")
        dia_chi_TT.send_keys(row["Địa chỉ "])

        ngay_sinh = driver.find_element_by_id("id_ngay_sinh_nkt")
        ngay_sinh.clear()
        ngay_sinh.send_keys(row["Ngày sinh"])
        
        so_Dinhdanh =driver.find_element_by_name("so_dinh_danh")
        so_Dinhdanh.send_keys(row["Số định danh"])

        so_Hieuxacnhan = driver.find_element_by_name("so_hieu_giay_xac_nhan")
        so_Hieuxacnhan.send_keys(row["Số hiệu xác nhận"])

        gioi_Tinh = Select((driver.find_element_by_id('id_gioi_tinh')))
        gioi_Tinh.select_by_visible_text(row["Giới tính"])

        quoc_Tich = driver.find_element_by_name("quoc_tich")
        quoc_Tich.send_keys(row["Quốc tịch"])

        dan_Toc = Select((driver.find_element_by_id('id_dan_toc')))
        dan_Toc.select_by_visible_text(row["Dân tộc"])

        ton_Giao = driver.find_element_by_id("id_ton_giao")
        lst_Tongiao = ton_Giao.find_elements_by_tag_name("option")
        for opt_tongiao in lst_Tongiao:
            if opt_tongiao.text == row["Tôn giáo"]:
                opt_tongiao.click()
                break
            else:
                print("Trường ton_Giao chưa xác thực")
                continue

        nhom_Mau = driver.find_element_by_id("id_nhom_mau")
        lst_NhomMau = nhom_Mau.find_elements_by_tag_name("option")
        for opt_nhommau in lst_NhomMau:
            if str(opt_nhommau.text).split()[-1].upper() == row["Nhóm máu"]:
                opt_nhommau.click()
                break
            else:
                print("Trường nhom_Mau chưa xác thực")
                continue
        
        trinhdo_HocVan = driver.find_element_by_id("id_trinh_do")
        lst_hocvan = trinhdo_HocVan.find_elements_by_tag_name("option")
        for opt_hocvan in lst_hocvan:
            if str(opt_hocvan.text) == row["Trình độ học vấn"]:
                opt_hocvan.click()
                break
            else:
                print("Trường trinhdo_HocVan chưa xác thực")
                continue
       
        trinhdo_Chuyenmon = driver.find_element_by_xpath('//*[@id="id_chuyen_mon"]')
        lst_Chuyenmon = trinhdo_Chuyenmon.find_elements_by_tag_name("option")
        for opt_chuyenmon in lst_Chuyenmon:
            if str(opt_chuyenmon.text) == row["Trình độ chuyên môn"]:
                opt_chuyenmon.click()
                break
            else:
                print("Trường trinhdo_Chuyenmon chưa xác thực")
                continue       
        
        nghe_nghiep = driver.find_element_by_xpath('//*[@id="id_nghe_nghiep"]')
        lst_nghenhiep = nghe_nghiep.find_elements_by_tag_name("option")
        for opt_nghengiep in lst_nghenhiep:
            if str(opt_nghengiep.text) == row["Nghề nghiệp"]:
                opt_nghengiep.click()
                break
            else:
                print("Trường nghe_nghiep chưa xác thực")
                continue
        
        nan_nhanCDDC = driver.find_element_by_xpath('//*[@id="id_nan_nhan_da_cam"]')
        lst_CDDC = nan_nhanCDDC.find_elements_by_tag_name("option")
        for opt_CDDC in lst_CDDC:
            if str(opt_CDDC.text) == row["Nạn nhân CĐDC"]:
                opt_CDDC.click()
                break
            else:
                print("Trường nan_nhanCDDC chưa xác thực")
                continue             
                
        hon_nhan = driver.find_element_by_xpath('//*[@id="id_hon_nhan"]')
        lst_honnhan = hon_nhan.find_elements_by_tag_name("option")
        for opt_honnhan in lst_honnhan:
            if str(opt_honnhan.text) == row["Tình trạng hôn nhân"]:
                opt_honnhan.click()
                break
            else:
                print("Trường hon_nhan chưa xác thực")
                continue   
       
        btn_next = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/form/div[6]/div/button[2]')
        driver.execute_script("arguments[0].click()",btn_next)
        sleep(8)
        #---------------------
        
        #------Thông tin liên lạc NKT
        diachi_LL_NKT = driver.find_element_by_xpath('//*[@id="myForm"]/div[2]/div[1]/div/input')
        diachi_LL_NKT.send_keys(row["Địa chỉ liên lạc NKT"])

        so_DTLH =driver.find_element_by_xpath('//*[@id="myForm"]/div[2]/div[2]/div[1]/input')
        so_DTLH.send_keys(row["Số điện thoại"])
        sleep(2)
       
        ngay_Capnhat = driver.find_element_by_name('ngay_cap_nhat')
        ngay_Capnhat.clear()
        ngay_Capnhat.send_keys(row['Ngày cập nhật'])
        
        nguoi_Capnhat = driver.find_element_by_name('nguoi_cap_nhat')
        nguoi_Capnhat.send_keys(row['Người cập nhật'])
        
        btn_next = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/form/div[6]/div/button[2]')
        driver.execute_script("arguments[0].click()",btn_next)
        sleep(8)
        #Thông tin hộ gia đình
        

        btn_next = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/form/div[6]/div/button[2]')
        driver.execute_script("arguments[0].click()",btn_next)
        sleep(8)    
        #Thông tin người thân đại diện  
        ten_nguoidaidien = driver.find_element_by_xpath('//*[@id="myForm"]/div[3]/div[1]/div[1]/input')
        quanhe_NKT = driver.find_element_by_xpath('//*[@id="id_quan_he_voi_nkt"]')
        sdt_nguoidaidien = driver.find_element_by_xpath('//*[@id="myForm"]/div[4]/div[2]/div[2]/input')
        cmnd_nguoidaidien = driver.find_element_by_xpath('//*[@id="myForm"]/div[4]/div[3]/div[1]/input')
        dinhdanh_nguoidaidien = driver.find_element_by_xpath('//*[@id="myForm"]/div[4]/div[3]/div[2]/input')
        quoctich_nguoidaidien = driver.find_element_by_xpath('//*[@id="myForm"]/div[4]/div[3]/div[3]/input')
       
        btn_next = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/form/div[6]/div/button[2]')
        driver.execute_script("arguments[0].click()",btn_next) 
        sleep(8)
        
        #Thông tin người chăm sóc
        hoten_nguoichamsoc = driver.find_element_by_xpath('//*[@id="myForm"]/div[5]/div[1]/div[1]/input')
        cmnd_nguoichamsoc = driver.find_element_by_xpath('//*[@id="myForm"]/div[5]/div[1]/div[2]/input')
        dinhdanh_nguoichamsoc= driver.find_element_by_xpath('//*[@id="myForm"]/div[5]/div[2]/div[1]/input')
        quoctich_nguoichamsoc = driver.find_element_by_xpath('//*[@id="myForm"]/div[5]/div[2]/div[2]/input')
        quanhe_NCS_NKT = driver.find_element_by_xpath('//*[@id="id_quan_he_voi_nkt"]')
        sdt_nguoichamsoc = driver.find_element_by_xpath('//*[@id="myForm"]/div[5]/div[3]/div[2]/input')

        button_luuthongtin = driver.find_element_by_xpath('//*[@id="save_form"]')
        driver.execute_script("arguments[0].click()",button_luuthongtin)
        
     
        sleep(2)
       # button tiếp theo
    
        button_nextTab= driver.find_element_by_xpath('//*[@id="nhapTTKT"]')
        driver.execute_script("arguments[0].click()",button_nextTab)
        sleep(3)
    
            # button_thongbaoTonTai = driver.find_element_by_xpath('//*[@id="alertModal"]/div/div/div[3]/button')
            # driver.execute_script("arguments[0].click()",button_thongbaoTonTai)
            # print("Thông báo: Thông tin của bị trùng lặp")

    
        # # tab khuyết tật ----------------------------------------- ##
        check_box_vandong = driver.find_element_by_xpath('//*[@id="vandongform"]/div[4]/div[2]/input')
        driver.execute_script("arguments[0].click()",check_box_vandong)

        khokhan_vandongkhac = driver.find_element_by_xpath('//*[@id="vandongform"]/div[5]/div/input')
        
        button_nextVandong = driver.find_element_by_xpath('//*[@id="myForm1"]/div[6]/div/button[2]')
        driver.execute_script("arguments[0].click()",button_nextVandong)
        
        #nhìn
        nhin_khac = driver.find_element_by_xpath('//*[@id="nhinform"]/div[4]/div/input')
        button_nextVandong = driver.find_element_by_xpath('//*[@id="myForm1"]/div[6]/div/button[2]')
        driver.execute_script("arguments[0].click()",button_nextVandong)
        
        #nhận thức
        nhanthuc_khac = driver.find_element_by_xpath('//*[@id="nhanthucform"]/div[3]/div/input')
        
        button_nextVandong = driver.find_element_by_xpath('//*[@id="myForm1"]/div[6]/div/button[2]')
        driver.execute_script("arguments[0].click()",button_nextVandong)

        #khuyết tật khác
        button_nextVandong = driver.find_element_by_xpath('//*[@id="myForm1"]/div[6]/div/button[2]')
        driver.execute_script("arguments[0].click()",button_nextVandong)

        button_luuthongtin_khuyetat = driver.find_element_by_xpath('//*[@id="save_form_1"]')
        driver.execute_script("arguments[0].click()",button_luuthongtin_khuyetat)
        sleep(3)
       
        # Next Tab nhu cau ---------------------------------#
        driver.find_element_by_xpath('//*[@id="nhapNhuCau"]').click()
        sleep(2)
        
        
        # Y tế 
        button_nextNhucau = driver.find_element_by_xpath('//*[@id="myForm2"]/div[4]/div/button[2]')
        driver.execute_script("arguments[0].click()",button_nextNhucau)
        sleep(2)
        
        # Đời sống, kinh tế, hòa nhập xã hội 
        button_nextNhucau = driver.find_element_by_xpath('//*[@id="myForm2"]/div[4]/div/button[2]')
        driver.execute_script("arguments[0].click()",button_nextNhucau)
        sleep(2)
       
        #Giáo giục
        button_luuthongtin_giaoduc = driver.find_element_by_xpath('//*[@id="save_form_2"]')
        driver.execute_script("arguments[0].click()",button_luuthongtin_giaoduc)
        sleep(2)
        
        # Next Tab hỗ trợ đã nhận  -------------------------------#
        buton_hotroDaNhan = driver.find_element_by_id('nhapHoTroDaNhan')
        driver.execute_script("arguments[0].click()",buton_hotroDaNhan)
        sleep(2)
       
        #--------- Y tế
        button_next_hotrodaNhan= driver.find_element_by_xpath('//*[@id="myForm3"]/div[5]/div/button[2]')
        driver.execute_script("arguments[0].click()",button_next_hotrodaNhan)
        sleep(2)
        
        #-------------- Đời sống, kinh tế, hòa nhập xã hội
        button_next_hotrodaNhan= driver.find_element_by_xpath('//*[@id="myForm3"]/div[5]/div/button[2]')
        driver.execute_script("arguments[0].click()",button_next_hotrodaNhan)
        sleep(2)
        
        #-------------- Giáo dục
        button_next_hotrodaNhan= driver.find_element_by_xpath('//*[@id="myForm3"]/div[5]/div/button[2]')
        driver.execute_script("arguments[0].click()",button_next_hotrodaNhan)
        sleep(2)
        
        #--------------Chi tiết
        button_next_hotrodaNhan= driver.find_element_by_xpath('//*[@id="myForm3"]/div[5]/div/button[2]')
        driver.execute_script("arguments[0].click()",button_next_hotrodaNhan) 
        sleep(2)
        
        button_luuthongtin_hotro = driver.find_element_by_xpath('//*[@id="save_form_3"]')
        driver.execute_script("arguments[0].click()",button_luuthongtin_hotro) 
        
        sleep(2)
        alert = Wait.until((EC.alert_is_present()))
        alert= driver.switch_to.alert
        alert.accept()
        sleep(10)
        
        danhsach_Khuyettat = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[1]/div/h6')
        if danhsach_Khuyettat.text == "Danh sách chi tiết người khuyết tật":
            print("Đăng kí thành công")
        
        sleep(5)
    
    
    driver.quit()



if __name__ == "__main__":
    Main()