import requests
import pandas as pd
import json
import os, inspect
import pytesseract
import cv2
from PIL import Image
from selenium import webdriver
import logging
from bs4 import BeautifulSoup
import re


def api_otp(ip, name_port):
    "api post OTP cho sim"
    url = "http://" + str(ip) + "/API/QueryInfo"

    payload = "{\"event\":\"newqueryrxsms\",\"port\":\""+str(name_port)+"\"}"
    headers = {
        'content-type': "application/json",
        'authorization': "Basic QXBpVXNlckFkbWluOlZicG8xMjM0NQ==",
        }
    response = requests.request("POST", url, data=payload, headers=headers)

    load_opt = json.loads(response.text,strict=False)['content']
    
    str_Opt = re.findall(r"(?<=TongcucThue:Ban dang giao dich nop ho so khai thue\.Ma xac thuc giao dich dien tu cua ban la:)\d+",load_opt)[-1]

    testdaytime = load_opt.split("|E;")
    lst_datime = []
    for i in  testdaytime:
        if i.find("Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la") != -1:
            lst_datime.append(i)
    day_times = lst_datime[-1].split(":1(-1)")[0]
    
    return day_times, str_Opt

# if __name__ == '__main__':
  
#     day_time ,code_otp = api_otp("171.244.236.149:1555",1)
#     day_time = day_time.split(" ")[0]

#     print(day_time, code_otp)