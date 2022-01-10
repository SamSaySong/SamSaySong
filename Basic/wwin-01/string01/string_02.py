
from datetime import datetime
import re
from unidecode import unidecode
file_Input = open("D:\Win\Train Python\wwin-01\Exercise_01\Input.txt", "r", encoding="utf-8")
output_file = file_Input.read()
file_Input_1 = open("D:\Win\Train Python\wwin-01\Exercise_01\Input.txt", "r", encoding="utf-8")
output_file_1 = file_Input_1.readlines()
# i = 1
lst_1 = re.findall("(?<=Mã số thuế:\s)\d{1,}", output_file)
# lst_masothue = []
# while i <= len(lst_1):  
#     lst_masothue.append(str(i) + "-" + lst_1[i-1])   
#     i += 1
# file_Output_1 = open("D:\Win\Train Python\wwin-01\Output_MASOTHUE.txt", "w", encoding="utf-8")
# file_Output_1.writelines("\n".join(lst_masothue))
# file_Output_1.close()
# #######################

y = output_file.replace("Quận", "Q.").replace("Huyện", "H.").replace("Thành phố", "TP.")  
lst_2 = re.findall(r"(?<=Địa chỉ:\s).+", y)
# lst_diachi = []  
# x = 1
# while x <= len(lst_2):
#     str_x = str(lst_2[x-1]).upper()     
#     lst_diachi.append(str(x) + "-" + str_x + ".\n")
#     x+=1
# file_Output_2 = open("D:\Win\Train Python\wwin-01\Output_DIACHI.txt", "w", encoding="utf-8")
# file_Output_2.writelines(lst_diachi)
# file_Output_2.close()
# #######################

lst_3 = re.findall(r"(?<=Tỉnh/Thành phố:\s)\w.*", str(output_file))
# lst_Tinh_Thanh = []
# j = 1
# while j <= len(lst_3):
#    str_j = str(lst_3[j-1]).upper()
#    lst_Tinh_Thanh.append(str(i) + "-" + str_j + ".\n")
#    j+=1
# file_Output_3 = open("D:\Win\Train Python\wwin-01\Output_TINH_THANH.txt", "w", encoding="utf-8")
# file_Output_3.writelines(lst_Tinh_Thanh)
# file_Output_3.close()    
# ######################

lst_4 = re.findall(r"(?<=Ngày thành lập:\s)\d{1,}\-.*", output_file)
# lst_Ngaythanhlap = []
# k = 1
# while k <= len(lst_4):
#     x = datetime.strptime(lst_4[k-1], "%d-%m-%Y").date()
#     lst_Ngaythanhlap.append(str(k) + "-" + datetime.strftime(x, "%y%m%d") + "\n")
#     k +=1
# file_Output_4 = open("D:\Win\Train Python\wwin-01\Output_NGAYTHANHLAP.txt", "w", encoding="utf-8")
# file_Output_4.writelines(lst_Ngaythanhlap)
# file_Output_4.close()
# # ######################

lst_5 = re.findall(r"(?<=Ngành nghề chính).*", output_file)
lst_NganhNgheChinh = []
a = 1
while a <= len(lst_5):
    lst_NganhNgheChinh.append(str(a) + "-" + re.sub(":", "", lst_5[a-1]) + ".\n")
    a+=1
file_Output_5 = open("D:\Win\Train Python\wwin-01\Output_NGANHNGHECHINH.txt", "w", encoding="utf-8")
file_Output_5.writelines(lst_NganhNgheChinh)
file_Output_5.close()
# #########################

lst_6 = re.findall(r"(?<=Cập nhật:\s).*", output_file)
lst_CapNhat = []
c = 1
while c <= len(lst_6):
    lst_CapNhat.append(str(c) + "-" + lst_6[c-1] + "\n")
    c += 1
file_Output_6 = open("D:\Win\Train Python\wwin-01\Output_CAPNHAT.txt", "w", encoding="utf-8")
file_Output_6.writelines(lst_CapNhat)
file_Output_6.close()
#########################

h = 1
int_count = 1
lst_Tencongty = []
while h <= len(output_file_1):
    lst_Tencongty.append(str(int_count) + "-" + output_file_1[h-1])   
    h += 7
    int_count += 1
file_Output_7 = open("D:\Win\Train Python\wwin-01\Output_TENCONGTY.txt", "w", encoding="utf-8")
file_Output_7.writelines(lst_Tencongty)
file_Output_7.close() 

##lst_Tencongty = [unidecode(i) for i in lst_Tencongty]

#########################

lst_Ouput_1dong = []
z = 1
while z <= len(lst_Tencongty):
    x = datetime.strptime(lst_4[z-1], "%d-%m-%Y").date()
    y = datetime.strftime(x, "%Y")
    lst_Ouput_1dong.append(re.sub("\n","",lst_Tencongty[z-1]) + "|" + lst_1[z-1] + "|" +lst_2[z-1] + "|" + y + "|"+ lst_3[z-1] +"|"+ lst_6[z-1] +"|"+ re.sub(":", "", lst_5[z-1])) 
    z +=1

lst_Ouput_1dong = [unidecode(h) for h in lst_Ouput_1dong]
file_Output_1dong = open("D:\Win\Train Python\wwin-01\Output_1dong.txt", "w", encoding="utf-8")
file_Output_1dong.writelines("\n".join(lst_Ouput_1dong))
file_Output_1dong.close()