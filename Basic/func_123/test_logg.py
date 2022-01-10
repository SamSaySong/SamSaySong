import time
import pandas as pd
from time import sleep
import os, inspect, sys
import re
import glob
from PIL import Image
import datetime
import shutil
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# import logging
# import os, inspect, sys
# from time import sleep

# global LOG_info
# """ Ghi log """
# logging.basicConfig(format=' %(asctime)s [%(levelname)s] >>> ------  %(message)s  <<<------------------', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
# logFormatter = logging.Formatter(' %(asctime)s [%(levelname)s] >>> ------  %(message)s  <<<------------------', datefmt='%d/%m/%Y %H:%M:%S')
# LOG_info = logging.info
# LOG_warn = logging.warning
# FileHandler = logging.FileHandler(CurDir + "\\log.txt", 'a+', 'utf-8')
# FileHandler.setFormatter(logFormatter)
# logging.getLogger().addHandler(FileHandler)


# try:
#     for i in range(1,10):
#         if i > "5":
#             print(i)
# except Exception as e:
#     LOG_info('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))
path_Download = CurDir+"\\Input_kekhai"

str_link= 'https://media-dev.vina-payroll.com/media/ReportPit/941/vs026_pit_report_1638502860.xlsx?X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=gDJyyFZPgWhLWP9suF1m%2F20211207%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20211207T062135Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Signature=6acf75dfd7c1d4cd65094efd6b6a08cf42ade603d329e297ff38be94f6e5d476'

def get_link_request(str_link):
    "Get link file request"
    str_link = str_link.split('/')[-1].split('?')[0]

    lst_link_download = []
    path_to_download_folder = glob.glob(os.path.join(path_Download)+"\\*")
    for file_dowload in path_to_download_folder:
        # get MST file
        file_name = file_dowload.split("\\")[-1].split(' ')[0]
        if file_name == "Unconfirmed":
            lst_link_download.append(file_dowload)
        time.sleep(1)

    for i_link_dowload in lst_link_download:
        i_file_name = i_link_dowload.split("\\")[-1]

        # get date_time
        f = os.path.getmtime(i_link_dowload)
        date_time = datetime.datetime.fromtimestamp(f)
        str_date = date_time.strftime("%Y-%m-%d %H:%M:%S")
        time_max = get_time_file_request(lst_link_download)
        time.sleep(1)
        if str_date == time_max:
            link_dowload_rename = path_Download + "\\"+ str_link
            try:
                if os.path.exists(link_dowload_rename) == True:
                    link_dowload_rename = path_Download +"\\"+str_date.split(' ')[0]+"_"+ str_link
                    os.rename(path_Download + "\\"+ i_file_name,  link_dowload_rename)
                else:
                    os.rename(path_Download + "\\"+ i_file_name, link_dowload_rename)
                print(link_dowload_rename)
            except Exception:
                print(Exception)
        # return link_dowload_rename, str_date
def get_time_file_request(lst_link):
    # get date_time max list lst_link
    import os, datetime
    lst_date = []
    for file in lst_link:
        f = os.path.getmtime(file)
        date_time = datetime.datetime.fromtimestamp(f)
        str_date = date_time.strftime("%Y-%m-%d %H:%M:%S")
        lst_date.append(str_date)
    time.sleep(1)
    time_max = max(lst_date)
    return time_max


get_link_request(str_link)