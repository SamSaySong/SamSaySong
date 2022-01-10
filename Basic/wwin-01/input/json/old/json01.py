import pandas as pd
import json
import re
data_df_1 = pd.read_excel(r'D:\Win\Train Python\wwin-01\input\ISMS_DangKyLamViecTuXa.xlsx', sheet_name='Sheet 1',skiprows=3,skipfooter=10,header=1,engine="openpyxl")
list_header = data_df_1.columns.values
dic_Output = {"forms":[]}
str_Menu = ""
int_Count = 0

dic_Con = {
        "title": "",
        "editable": True,
        "children": []
        }

if len(data_df_1) == 0:
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
    
else:
    for idx, row in data_df_1.iterrows():
        for idx_header ,i_header in enumerate(list_header):   
        
            if idx_header == 0:
                continue
            
            if "Phần dành" in i_header:
                
                str_Menu = i_header
                dic_Con["title"] = str_Menu

            dic_Con['children'].append({
                        "title": row[i_header],
                        "required": True if "*" in row[i_header] else False,
                        "editable": True
                    })

            if len(list_header)-1 == idx_header:
                dic_Output["forms"].append(dic_Con)
                break
            
            if "Phần dành" in list_header[idx_header+1]:
                dic_Output["forms"].append(dic_Con)
                dic_Con = {
                "title": "",
                "editable": True,
                "children": []
                }     
        break

print(dic_Output)


# with open(r'D:\Win\Train Python\wwin-01\input\data.json', 'w+', encoding="utf-8") as json_file:
#     json.dump(dic_Output,json_file,indent= 4,ensure_ascii=None)
