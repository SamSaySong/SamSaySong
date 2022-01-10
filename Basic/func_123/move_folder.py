import pandas as pd
from time import sleep
import os, inspect, sys
import re
import glob
from PIL import Image
import datetime
import shutil
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_folder_input = ""
path_oout = ""


def move_file(folder_company, path_oout, name_Port,folder_name, file_name):
    try:
        if not os.path.exists(path_oout+name_Port+"\\"+folder_name):
            os.makedirs(path_oout+name_Port+"\\"+folder_name)
        os.rename((folder_company+"\\"+file_name), path_oout+name_Port+"\\"+folder_name+"\\"+file_name)
    except Exception:
        print(Exception)


for path_Port in path_folder_input:
    name_Port = path_Port.split("\\")[-2]
    path_company = glob.glob(os.path.abspath(path_Port+"\\*\\"))
    print(name_Port)
    
    # ---- Duyet Folder Company -----
    for folder_company in path_company:
        folder_name = folder_company.split("\\")[-1]
        print(folder_name)
        path_file = glob.glob(os.path.abspath(folder_company+"\\*.txt"))

        for file in path_file:
            file_name = str(file).split("\\")[-1]
            print(file_name)
            move_file(folder_company, path_oout, name_Port,folder_name, file_name)

#  check data_frame


def check_df(df_input):

    df_input.astype(str)
    for idx, row in df_input.iterrows():
        if str(row).find("CT01") != -1 or str(row).find("Tình trạng") != -1:
            continue
        if str(df_input["Status"][idx]).lower() == "nan":
            return False
    return True



# 234
def remove_temp():
    """ Remove folder templ trong máy tính """
    appdata = os.environ['LOCALAPPDATA']+'\\Temp\\*'
    list_temp = glob.glob(appdata)
    for path in list_temp:
        try:
            os.remove(path)
        except Exception as E:
            pass
        try:
            shutil.rmtree(path, ignore_errors=True)
        except Exception as E:
            pass
    


def monthday():
    from calendar import monthrange
    num_days = monthrange(2022, 1)[1] # num_days = 28.
    print(num_days) # Prints 28.