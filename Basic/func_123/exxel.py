# import datetime
# def convert_datetime_string(data_input,format_input='%Y-%m-%d',format_output='%d/%m/%Y'):
#     data_date = datetime.datetime.strptime(data_input, format_input)
#     data_date = data_date.strftime(format_output)
#     return data_date


# "Ban dang giao dich nop ho so khai thue. Ma xac thuc giao dich dien tu cua ban la:48575851"
# # "".split(';')[-1].split('|')[0].replace(' ','')

# a = str_tesst["content"].split(';')[-1].split("(-1)")
# load= a[0][:-2]

# convert = convert_datetime_string(load.split(" ")[0])


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




def get_Value(filename = "", row=None ,column= None):
    # row = idx+1,  cols = 20
    import openpyxl
    from xlcalculator import ModelCompiler
    from xlcalculator import Model
    from xlcalculator import Evaluator
    if row != None and column != None:
        work_book = openpyxl.load_workbook(filename)
        work_sheet = work_book["Declaration (EN)"]

        int_value = work_sheet.cell(row+2, column+1).value
        str_value = int_value.replace("=","")
        compiler = ModelCompiler()
        new_model = compiler.read_and_parse_archive(filename, ignore_sheets="1")
        evaluator = Evaluator(new_model)
        val1 = evaluator.evaluate(str_value)
        return str(val1)
    else:
        val1 = ""
        return val1



def demo_data():

    # a =os.path.abspath("Huy\\"+'local_filename.xlsx')
    path = r"D:\HuyNP\Huy\demo_pit_report_1640146582 (1).xlsx"
    import win32com.client as win32
    import os
    import win32com.client
 
    xlApp =win32com.client.dynamic.Dispatch("Excel.Application")
    xlApp.DisplayAlerts = False
    xlwb = xlApp.Workbooks.Open(path, True, False, None)
    # xlApp.DisplayAlerts = True
    xlSheet = xlwb.Worksheets('Declaration (EN)')
    print(int(xlSheet.cells(44,20).value))
    xlwb.Close(True)
    del xlApp




import pandas as pd
import re
path = r"D:\HuyNP\Huy\demo_pit_report_1641285136.xlsx"
def data_input():

    df_input = pd.read_excel(path,sheet_name="Declaration (EN)", engine='openpyxl',dtype=object)
    
    for idx, row in df_input.iterrows():
        
        if str(row).find('[01]') and str(row).find("Quarter") != -1:

            str_Quykekhai = (re.findall('(?<=\(Quarter\)\s)\d{1}',df_input.iloc[idx,1]))[0]
            str_Namkekhai = (re.findall('(?<=\(Year\)\s)\d{4}',df_input.iloc[idx,1]))[0]
            str_Thangkekhai = ""

        if str(row).find('[01]') and str(row).find("Month") != -1:
            str_Namkekhai = (re.findall('(?<=\(Year\)\s)\d{4}',df_input.iloc[idx,1]))[0]
            str_Thangkekhai = (re.findall('(?<=\(Month\)\s)\d{1,2}',df_input.iloc[idx,1]))[0]
            str_Quykekhai = ""
        if str(row).find('[02]') != -1:
            
            if str(row).find("Lần đầu (First time):     [ X ]") != -1:
                print(row)
                print("To khai chinh thuc")      
            else :
                print(row)
                print("To khai bo sung")
        if str(row).find('[05]') != -1:
            str_MST = str(df_input.iloc[idx,3])+ str(df_input.iloc[idx,4])+str(df_input.iloc[idx,5])+str(df_input.iloc[idx,6])+str(df_input.iloc[idx,7])+str(df_input.iloc[idx,8])+str(df_input.iloc[idx,9])+str(df_input.iloc[idx,10])+str(df_input.iloc[idx,11])+str(df_input.iloc[idx,12])+str(df_input.iloc[idx,13]).strip()+str(df_input.iloc[idx,14])+str(df_input.iloc[idx,15])+str(df_input.iloc[idx,16])
            str_MST = str_MST.split("nan")[0]
        
        if str(row).find('[21]') != -1:
            str_CT21 = mlem_execl(path, row= idx, column=19)

        if str(row).find('[22]') != -1:
            str_CT22 = mlem_execl(path, row= idx, column=19)

        # if str(row).find('[23]') != -1:
        #     str_CT23 = get_Value(r"D:\HuyNP\Huy\local_filename.xlsx", row= idx, column=19)
        
        if str(row).find('[24]') != -1:
            str_CT24 = mlem_execl(path, row= idx, column=19)

        if str(row).find('[25]') != -1:
            str_CT25 = mlem_execl(path, row= idx, column=19)

        if str(row).find('[26]') != -1:
            # str_26 = str(df_input.iloc[idx,19])
            str_CT26 = mlem_execl(path, row= idx, column=19)
            # print(str_26)

        if str(row).find('[27]') != -1:
            str_CT27 = mlem_execl(path, row= idx, column=19)
        if str(row).find('[28]') != -1:
            str_CT28 = mlem_execl(path, row= idx, column=19)

        if str(row).find('[29]') != -1:
            str_CT29 = mlem_execl(path, row= idx, column=19)
            
        if str(row).find('[30]') != -1:
            str_CT30 = mlem_execl(path, row= idx, column=19)

        if str(row).find('[31]') != -1:
            str_CT31 = mlem_execl(path, row= idx, column=19)
            # print(str_CT31)

        if str(row).find('[32]') != -1:
            str_CT32 = mlem_execl(path, row= idx, column=19)

        if str(row).find('[33]') != -1:
            str_CT33 = mlem_execl(path, row= idx, column=19)

        if str(row).find('[34]') != -1:
            str_CT34 = mlem_execl(path, row= idx, column=19)  
            print(str_CT34)




def mlem_execl(path,row , column):
    'https://gist.github.com/rdapaz/63590adb94a46039ca4a10994dff9dbe'
    'https://www.py4u.net/discuss/190532'
    'https://stackoverflow.com/questions/50127959/win32-dispatch-vs-win32-gencache-in-python-what-are-the-pros-and-cons/50163150'

    # path =r"D:\HuyNP\Huy\demo_pit_report_1640146582 (3).xlsx"

    try:
        import sys, os
        import re
        import shutil
        import win32com.client as win32

        xlApp =win32.dynamic.Dispatch("Excel.Application")
        xlApp.DisplayAlerts = False

        xlwb = xlApp.Workbooks.Open(path, True, False, None)
        xlSheet = xlwb.Worksheets('Declaration (EN)')
        value =  int(xlSheet.cells(row+2,column+1).value)
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
        value =  int(xlSheet.cells(row+2,column+1).value)

    
    xlwb.Close(True)
    del xlApp
    return str(value)

data_input()


