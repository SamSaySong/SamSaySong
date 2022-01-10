# from typing import Optional
# import openpyxl
# import pandas as pd
# import base64
# import xlwings as xw
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# sheet = pyexcel.get_book(file_name=path)
# sheet_1 = sheet[0][23, 4]
# print(sheet_1)

# from xlrd import open_workbook
# from xlutils.filter import XLRDReader
# rb = open_workbook(path)
# r = XLRDReader(rb, 'D:\HuyNP\Huy/rgfg.xlsx')
# a = r.get_workbooks()[0]
# print(a)

# with open(path, 'rb') as f:
#   text = f.read()
# print(text)


# str_decode = text.decode("utf-8")
# def load_values(path):
#     workbook = openpyxl.load_workbook(path,data_only= True, read_only= True)
#     ws = workbook["Declaration (EN)"]
#     load_location= ws.cell(row=41,column=20).value
#     str_CT21 =load_location
#     print(str_CT21)


# df = pd.read_excel(path,sheet_name=1,dtype=object,engine="openpyxl")
# print(df)
path = r'D:\HuyNP\Huy/demo_pit_report_1641281550.xlsx'

# import xlwings as xw
# import win32com.client
# xlApp = win32com.client.DispatchEx('Excel.Application')
# wb = xlApp.Workbooks.Open(path)
# xlApp.Run('Declaration (EN)')
# wb.Save()
# xlApp.Quit()

# wbk = xw.Book(path)
# ws = wbk.sheets[1]
# print(ws.cells(41,20).value)
# print(ws.cells(1,1).formula)

# import gspread

# gc = gspread.service_account(filename=r"pit-terra-a894f149d8f5.json")


# sht1 = gc.open_by_key('1ZQdA7Tjs6mBL0VlH6mD-eyzXEJnhGKSZOozIyx5zx-0')


# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()

# drive = GoogleDrive(gauth)
# import calendar

# from calendar import  monthrange
# num_days = monthrange(2022, 1)[1] # num_days = 28.
# print(num_days) # Prints 28.
# print(calendar.prcal(2022, 1,1,1))