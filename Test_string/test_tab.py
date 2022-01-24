# import datetime
# def convert_datetime_string(data_input,format_input='%Y-%m-%d',format_output='%d/%m/%Y'):
#     data_date = datetime.datetime.strptime(data_input, format_input)
#     data_date = data_date.strftime(format_output)
#     return data_date

import shutil, os
file_input = r"D:\HuyNP\Project_PIT_Terra\pj-vpo_terra\input\vs026_pit_report_1642734352.xlsx"

path_Move_input = r"D:\\HuyNP\\Project_PIT_Terra\\pj-vpo_terra\\output"
file_name = "1074ed35-eb23-4003-a5b1-1fd8d9e3e459"
def move_file(file_input, path_Move_input, file_name):
    "move output"
    try:
        if not os.path.exists(path_Move_input+"\\"):
            os.makedirs(path_Move_input+"\\")

        shutil.move(file_input, path_Move_input+"\\" + file_name+".xlsx")
        return True
    except Exception as e :
        return False
move_file(file_input, path_Move_input, file_name)

# "Ban dang giao dich nop ho so khai thue. Ma xac thuc giao dich dien tu cua ban la:48575851"
# # "".split(';')[-1].split('|')[0].replace(' ','')

# a = str_tesst["content"].split(';')[-1].split("(-1)")
# load= a[0][:-2]

# convert = convert_datetime_string(load.split(" ")[0])


# print(load)
# asd = "04/11/2021 10:26:59"

# ghgh = asd.split(" ")[0].strip()
# # b = a[1].split('|')[0].split(":")[-1]


# import logging
# import os, inspect, sys
# from time import sleep
# CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# def logging_rpa():
#     """ Ghi log """
#     logging.basicConfig(format=' %(asctime)s [%(levelname)s] >>> ------  %(message)s  <<<------------------', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
#     logFormatter = logging.Formatter(' %(asctime)s [%(levelname)s] >>> ------  %(message)s  <<<------------------', datefmt='%d/%m/%Y %H:%M:%S')
#     LOG_info = logging.info
#     LOG_warn = logging.warning
#     FileHandler = logging.FileHandler(CurDir + "\\log.txt", 'a+', 'utf-8')
#     FileHandler.setFormatter(logFormatter)
#     logging.getLogger().addHandler(FileHandler)
#     return LOG_info,LOG_warn

# x = 99
# while True:
#     loggg = logging_rpa()
#     log_info = loggg[0]
#     log_warn = loggg[1]
#     if x < 100:
#         log_info("Đăng nhập thành công" +str(x))
#         sleep(1)
#     else:
#         log_warn("asdffg" +str(x))
#         sleep(1)
#         x=1
#     x+=1
# str = "D:\\HuyNP\\PIT\\test capcha\\main\\Move_Input\\VS026\\"
# folder_name = str.split("\\")[-2]
# print(folder_name)
# import re
# str_tesst= "total:18;2021-10-22 15:14:59:1(-1) (-1):84394741700:Hi|E;2021-10-22 15:27:26:1(-1) (-1):84902275712:Chao|E;2021-10-22 17:31:30:1(-1) (-1):84374057111:ronv aaaa|E;2021-10-28 09:41:08:1(-1) (-1):VNM_TB:TK goc cua QK hien con duoi 1.000d, vui long nap the de duy tri lien lac. Nap the online, truy cap https://www.vietnamobile.com.vn chon NAP TIEN. LH 789 (0d).|E;2021-11-01 08:28:52:1(-1) (-1):092:QUA TANG TRI AN! Chuc mung Quy khach da nhan duoc 2GB data toc do cao & 30 phut goi noi mang MIEN PHI (han su dung 2 ngay) tu Vietnamobile. Vui long bam *101# de kiem tra tai khoan. Tran trong!|E;2021-11-04 09:11:16:1(-1) (+84935109193):84902275712:Jejhe|E;2021-11-04 09:12:24:1(-1) (+84935109193):TongcucThue:Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la:03364103|E;2021-11-04 09:52:53:1(-1) (+84935109193):TongcucThue:Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la:44357908|E;2021-11-04 09:57:49:1(-1) (+84935109193):TongcucThue:Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la:03475269|E;2021-11-04 10:04:52:1(-1) (+84935109193):TongcucThue:Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la:77355585|E;2021-11-04 10:10:19:1(-1) (+84935109193):TongcucThue:Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la:52450476|E;2021-11-04 10:26:30:1(-1) (+84935109193):TongcucThue:Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la:36445619|E;2021-11-04 10:26:58:1(-1) (+84935109193):TongcucThue:CQT tiep nhan ho so khai thue dien tu voi ma giao dich 11020210002679097. Ket qua xu ly ho so duoc gui toi nguoi nop thue trong vong 01 ngay lam viec.|E;2021-11-04 11:58:31:1(-1) (+84935109193):999:Bấm CF50 gửi 999, MobiFone tặng TB 935109193: 2,5GB DATA TỐC ĐỘ CAO, 100 phút gọi và 100 SMS nội mạng, 35 phút gọi và 20 SMS ngoại mạng. Đặc biệt, FREE hoàn toàn cước 3G/4G truy cập ClipTV và xem phim chiếu rạp siêu HOT tại https://cliptv.vn/phim . MIỄN PHÍ KHÔNG GIỚI HẠN các cuộc gọi nội nhóm tối đa 10 thành viên. Giá cước 50.000đ/thuê bao chính/30 ngày và 15.000đ/thành viên/30 ngày. Liên hệ 9090. Từ chối tư vấn CSKH của MobiFone, soạn TC gửi 9241|E;2021-11-04 14:33:16:1(-1) (+84935109193):TongcucThue:Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la:54446003|E;2021-11-04 14:52:03:1(-1) (+84935109193):TongcucThue:Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la:54434429|E;2021-11-04 14:52:18:1(-1) (+84935109193):TongcucThue:CQT tiep nhan ho so khai thue dien tu voi ma giao dich 11020210002679950. Ket qua xu ly ho so duoc gui toi nguoi nop thue trong vong 01 ngay lam viec.|E;2021-11-05 07:40:02:1(-1) (-1):092:QUA TANG TRI AN! Chuc mung Quy khach da nhan duoc 4GB data toc do cao & 30 phut goi noi mang MIEN PHI (han su dung 2 ngay) tu Vietnamobile. Vui long bam *101# de kiem tra tai khoan. Tran trong!|E"

# lst_otp = re.findall(r"(?<=TongcucThue:Ban dang giao dich nop ho so khai thue\.Ma xac thuc giao dich dien tu cua ban la:)\d{8}",str_tesst)
# # lst_daytime = re.findall(r"(?<=\|E;)\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}(?!:TongcucThue:Ban dang giao dich nop ho so khai thue)",str_tesst)
# testdaytime = str_tesst.split("|E;")
# lst_datime = []
# for i in  testdaytime:
#     if i.find("Ban dang giao dich nop ho so khai thue.Ma xac thuc giao dich dien tu cua ban la") != -1:
#         lst_datime.append(i)
# a = lst_datime[-1].split(":1(-1)")[0]
# print(a)

# lst = [lambda i=i: i + i for i in range(1, 6)]

# print(lst)
# for f in lst:
#     print(f())

# import operator
# import functools

# # print("The concatenated product is : ", end="")
# # print(functools.reduce(operator.concat, ["geeks", "for", "geeks"]))
# # lis = [1,7,5,10,5,20,30,10]
# # print(functools.reduce(lambda a, b: a if a > b else b, lis))
# numbers = (1, 2, 3, 4)
# result = map(lambda x: x+x, numbers)
# print(list(result))
import regex

str_test = [' 120\n 121\n 122\n ', '22/10/2021\n 15:00:04\n 22/10/2021\n 15:00:06\n 22/10/2021\n 15:00:06\n ', '1482\n 8217\n 8217\n ', '69\n 39,820,000.0\n 70\n 13,200,000.00\n 22,000.00\n ', '0.00\n 0.00\n 0.00\n ', '4,514,393,229.00 4,501,193,229.00 4,501,171,229.00 ', '80412279\n 2183721\n 2183721\n ', '990CTLN\n Н2\n 990EBAN\n 990EBAN\n ', '762\n 762\n 762\n ', ':205162069, tai ACB. ND\n YOSHINO GYPŞUM VN thanh\n toan chi phi in an va thict ke\n theo Inv.270-Inv.271\n YOSHINO GYPSUM\n CTLNHIDO00000147084164\n 0-12-PMT-002\n REM\n VN thanh loan tien mua thict\n bi dien theo Inv.7426\n REM\n VN thanh toan tien mua thict\n bi dien theo Inv.7426\n REM\n YOSHINO GYPSUM\n FIBK-TKThe\n \n ']




list_Test = regex.findall(r'\s\d{1,3}\s',str_test[0])
# print(list_Test)


def mlem_execl():
    'https://gist.github.com/rdapaz/63590adb94a46039ca4a10994dff9dbe'
    'https://www.py4u.net/discuss/190532'
    'https://stackoverflow.com/questions/50127959/win32-dispatch-vs-win32-gencache-in-python-what-are-the-pros-and-cons/50163150'

    path =r"C:\Users\VBPO\Downloads\vs026_pit_report_1642734813.xlsx"

    try:
        import sys, os
        import re
        import shutil
        import win32com.client as win32

        xlApp =win32.dynamic.Dispatch("Excel.Application")
        xlApp.DisplayAlerts = False

        xlwb = xlApp.Workbooks.Open(path, True, False, None)
        xlSheet = xlwb.Worksheets('Declaration (EN)')
        value =  int(xlSheet.cells(44,20).value)
    except:   
        MODULE_LIST = [m.__name__ for m in sys.modules.values()]
        for module in MODULE_LIST:
            if re.match(r'win32com\.gen_py\..+', module):
                del sys.modules[module]

        shutil.rmtree(os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp', 'gen_py'))
        
        xlApp =win32.dynamic.Dispatch("Excel.Application")
        xlApp.DisplayAlerts = False

        xlwb = xlApp.Workbooks.Open(path, True, False, None)
        xlSheet = xlwb.Worksheets('Declaration (EN)')
        value =  int(xlSheet.cells(44,20).value)

    print(value)
    xlwb.Close(True)
    del xlApp

mlem_execl()

