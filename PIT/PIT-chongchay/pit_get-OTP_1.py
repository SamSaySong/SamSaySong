
import os, sys, inspect
import time

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def get_file(file_name = "",mode_file="", encoding_file=""):
    " return str file"
    with open(file_name,mode= mode_file, encoding= encoding_file) as file:
        if str(mode_file).find('r'):
            str_file = file.read()
            file.close()
        if str(mode_file).find('w'):
            str_file = file.write()
            file.close()
    return str_file

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


name_Config = "config_pj-vpo_robot.json"
name_Logs = "logs_pj-vpo_robot.txt"
name_Config_port = "config_pj-vpo_port-name.json"

data_config = readJson(CurDir+"\\conf\\"+name_Config)


import logging
global LOG_INFO
global LOG_ERROR
logging.basicConfig(format='------------------ %(asctime)s >>>  %(message)s  <<<------------------', datefmt='%d/%m/%Y %H:%M:%S')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s",datefmt='%d/%m/%Y %H:%M:%S')
LOG_INFO = logging.warning
LOG_ERROR = logging.error
FileHandler = logging.FileHandler(CurDir+"\\"+ name_Logs, 'a+', 'utf-8')
FileHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(FileHandler)


# email cấu hình gửi
id_email_gui =data_config["id_email_gui"]
pass_email_gui =data_config["pass_email_gui"]

# email tb hoàn thành quy trình
email_nhan = data_config["email_nhan"]


def get_Text():
    "Request text messgase OTP"
    import re
    import requests
    import json
    import datetime
    try:
     
        ip_config = data_config["ip_otp"]
        str_textOTP = data_config["thu_muc_text_OTP"]
        email_nhan = data_config['email_nhan']
        lst_Port = ["1","2","3","4","5","6","7","8"]
        for name_port in lst_Port:

            with open(str_textOTP +"\\" +"request_OTP"+name_port+".txt",mode="r+" ,encoding="utf-8") as load_Len:
                lst_len = load_Len.read()
                load_Len.close()
            # print(len(lst_len))
            url = "http://"+str(ip_config)+"/API/QueryInfo"
            payload = json.dumps({"event": "newqueryrxsms", "port": ""+str(name_port)+""})
            
            headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic QXBpVXNlckFkbWluOlZicG8xMjM0NQ=='
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            load_text_OTP = json.loads(response.text,strict=False)['content']
            load_text = re.sub(";","\n",load_text_OTP)

            with open(str_textOTP +"\\" +"request_OTP"+name_port+".txt",mode="w+" ,encoding="utf-8") as load_Text:
                load_Text.write(load_text)
                load_Text.close()
            time.sleep(2)
            with open(str_textOTP +"\\" +"request_OTP"+name_port+".txt",mode="r+" ,encoding="utf-8") as load_Text:
                lst_Len_new =  load_Text.read()
                load_Text.close()
                
            # print(len(lst_Len_new))

            
            testdaytime = load_text_OTP.split("|E;")

            if len(lst_len) < len(lst_Len_new):
                lst_datime = []

                for i in  testdaytime:
                    if i.find("TongcucThue") != -1:
                        lst_datime.append(i)

                if len(lst_datime) > 0:
                    day_times_OTP = lst_datime[-1].split(":1(-1)")[0].split(" ")[0]
                    # day_times_OTP = re.findall(r'^\d{4}(?:-\d{1,2}){2}', lst_datime[-1])[0]
                    date_time = datetime.datetime.now()
                    str_date_now = date_time.strftime("%Y-%m-%d")
                    time.sleep(2)
                    
                    if str_date_now == day_times_OTP:
                        send_mail(header="File OTP", text="Port " +name_port+" có tin nhắn mới\n"+lst_datime[-1], file_dinhkem= str_textOTP +"\\" +"request_OTP"+name_port+".txt", to_email=email_nhan)
                        LOG_INFO("Gửi mail thành công port " + name_port)
                    else:
                        LOG_INFO("Port "+name_port+" không có tin nhắn mới của Cục Thuế trong ngày hôm nay")
                else:
                    LOG_INFO("Port "+name_port+" không tìm thấy thông tin SMS Cục Thuế")
            else:
                LOG_INFO("Không có tin nhắn mới")
            time.sleep(3)

    except Exception as e:
        LOG_ERROR('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, str(e))

def message(header="",text="", file_img='', file_dinhkem=""):
    from email.mime.text import MIMEText
    from email.mime.image import MIMEImage
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg.attach(MIMEText(text))

   
    with open(file_dinhkem, 'rb') as f:
        
        # Read in the attachment using MIMEApplication
        file = MIMEApplication(f.read(),name=os.path.basename(file_dinhkem))
        
    file['Content-Disposition'] = f'attachment;\filename="{os.path.basename(file_dinhkem)}"' 
    msg.attach(file)

    msg['Subject'] = "[PIT-OTP] "+header

    return msg

def send_mail(header="",text="",to_email ="", file_dinhkem = ""):
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
    msg = message(header=header, text=text, file_img = "", file_dinhkem = file_dinhkem)

    # to = ["1235@gmail.com"]
    smtp.sendmail(from_addr= id_email_gui, to_addrs = to_email, msg = msg.as_string())    
    smtp.quit()
def loading():
    import time
    import sys

    animation = "|/-\\"

    for i in range(101):
        time.sleep(0.1)
        sys.stdout.write("\r" + animation[i % len(animation)]+" loading... "+str(i)+"%")
        sys.stdout.flush()

    # print("Loading:")
    # animation = ["■□□□□□□□□□","■■□□□□□□□□", "■■■□□□□□□□", "■■■■□□□□□□", "■■■■■□□□□□", "■■■■■■□□□□", "■■■■■■■□□□", "■■■■■■■■□□", "■■■■■■■■■□", "■■■■■■■■■■"]

    # for i in range(len(animation)):
    #     time.sleep(0.3)
    #     sys.stdout.write("\r" + animation[i % len(animation)])
    #     sys.stdout.flush()

if __name__ == "__main__":
    "Bắt đầu lấy OTP"
    loading()

    while True:
        get_Text()