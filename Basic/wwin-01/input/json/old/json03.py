import pandas as pd
import json
import re
data_df_1 = pd.read_excel(r'D:\Win\Train Python\wwin-01\input\IT_ChuyenQuyenThietBi.xlsx', sheet_name='Sheet 1',skiprows=4,header=1,engine="openpyxl")
list_header = data_df_1.columns.values
dic_Output = {"forms":[]}
str_Menu = ""
dic_Con = {
        "title": "",
        "editable": True,
        "children": []
        }

for i_dx,i_header in enumerate(list_header):      
    if i_dx == 0:
        continue
    
    str_Menu = re.sub("\n"," ",i_header)
    dic_Con["title"] = str_Menu
   
    dic_Output["forms"].append(dic_Con)
    dic_Con = {
        "title": "",
        "editable": True,
        "children": []
        }

print(dic_Output)