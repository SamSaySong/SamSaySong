import inspect, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import re
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
def open_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    chrome_options.add_argument("--no-sandbox") 
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path= r"D:\Win\Train Python\wwin-01\selenium02\chromedriver.exe",chrome_options=chrome_options)
    return driver

def open_input():
    df_input = pd.read_excel(CurDir+"\\Input.xlsx", "Sheet1", engine="openpyxl")      
    return df_input

def Main_fun():
    
    df_input_1 = open_input()
    driver = open_driver()
    lst_Tencty = []
    lst_url_cty = []
    lst_MST = []
    lst_TinhThanh = []
    lst_Thanhlap = []
    lst_DC = []
    lst_Phuong = []
    lst_Quan = []
    
    driver.get("https://thongtindoanhnghiep.co/")
    for idx, row in df_input_1.iterrows():
        element_1 = driver.find_element_by_id("TinhThanhIDValue")
        lst_option_1 = element_1.find_elements_by_tag_name("option")
        for option in lst_option_1:
            if option.text == "Đà Nẵng":
                option.click()
                break
        time.sleep(3)
        element_2 = driver.find_element_by_id("QuanHuyenIDValue")
        lst_option_2 = element_2.find_elements_by_tag_name("option")
        for option_2 in lst_option_2:
            if (option_2.text) == row[1]:
                option_2.click()
                break
        time.sleep(3)
        # btn_sub = driver.find_element_by_xpath('//*[@id="fulltextSearch"]/div/section[4]/button')
        # btn_sub.click() 
        btn_submit = driver.find_element_by_xpath('//*[@id="fulltextSearch"]/div/section[4]/button')
        btn_submit = driver.execute_script("arguments[0].click()", btn_submit)
        time.sleep(3)
       
        url_now = driver.current_url
        for a in range(1,2):
            driver_1 = open_driver()
            driver_1.get(url_now+"&p="+ str(a))

            elmt_TenCTy = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[4]/div[1]/div[*]/div[*]/h2/a')       
            elemt_MST = driver.find_elements_by_xpath('//*[@class="news-v3 bg-color-white"]/div/div/div/h3/strong')
            elemt_TinhThanh = driver.find_elements_by_xpath('//*[@class="news-v3 bg-color-white"]/div/div/div/p/a/strong')
            elemt_Thanhlap = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div[4]/div[1]/div[*]/div/div/div[3]/p')
            elemt_DC = driver.find_elements_by_xpath('//*[@class="news-v3 bg-color-white"]/div/p/strong')
            
            for i in range(len(elmt_TenCTy)):
                lst_Tencty.append(elmt_TenCTy[i].text)
                lst_url_cty.append(elmt_TenCTy[i].get_attribute('href'))               
                lst_MST.append(elemt_MST[i].text)
                str_TP = str(re.findall((r"[A-ZĐ]"),elemt_TinhThanh[i].text)).split()
                lst_TinhThanh.append("".join(str_TP))
                    
                lst_Thanhlap.append(re.findall((r"(?<=Ngày thành lập:\s)\w.+"),elemt_Thanhlap[i].text))
                lst_DC.append(re.findall(r"\w.*(?=\sPhường)", elemt_DC[i].text))
                lst_Phuong.append(re.findall(r"(?<=)[P]\w.+(?=\,\sQuận)", elemt_DC[i].text))
                lst_Quan.append(re.findall(r"(?<=\s)Quận.*(?=\,\sThành)",elemt_DC[i].text))
                
            driver_1.close() 
    df_data = {
            "Tên công ty": lst_Tencty,
            "Mã số thuế":lst_MST,
            "Ngày thành lập":lst_Thanhlap,
            "Địa chỉ": lst_DC,
            "Phường": lst_Phuong,
            "Quận": lst_Quan,
            "Tỉnh/Thành phố": lst_TinhThanh,
            "Đường dẫn": lst_url_cty
            }
    df_data = pd.DataFrame(df_data)
    
    lst_STT = []
    for idx, i_row in df_data.iterrows():
        lst_STT.append(idx)
    df_data.insert(loc=0, column="STT", value=lst_STT)       
    
    writer = pd.ExcelWriter(CurDir+"\\Output_1.xlsx", sheet_name ="Sheet1",engine='openpyxl')
    df_data.to_excel(writer,"Sheet1",index=False,engine="openpyxl")
    writer.save()   
    driver.close()     

if __name__ == "__main__":
    print("bat dau")   
    Main_fun()
    print("hoan thanh")


