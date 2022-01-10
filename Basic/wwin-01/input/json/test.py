import pandas as pd
import os
import glob
import re
import json
path =  os.path.abspath('input')
csv_files = glob.glob(os.path.join(path, "*.xlsx"))

str_Menu = ""
int_Count = 0

for f in csv_files:
    df = pd.read_excel(f,header=1,skiprows=3,engine="openpyxl")
    drop_df = df.dropna()
    list_header = drop_df.columns.values
    dic_Output = {"forms":[]}
    dic_Con = {
        "title": "",
        "editable": True,
        "children": []
        }
    if "Unnamed" not in list_header[1] and "(" not in list_header[1]:

        for idx, row in drop_df.iterrows():
            for idx_header ,i_header in enumerate(list_header):   
            
                if idx_header == 0:
                    continue
                
                if "Unnamed" not in i_header: 
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
                
                if "Unnamed" not in list_header[idx_header+1]:
                    dic_Output["forms"].append(dic_Con)
                    dic_Con = {
                    "title": "",
                    "editable": True,
                    "children": []
                    }     
            break
          
    elif "(" or "Unnamed" in list_header[1] :
        for idx, row in drop_df.iterrows():
            for i_dx, i_header in enumerate(list_header):      
                if i_dx == 0:
                    continue
                
                str_Menu = re.sub("\n"," ",row[i_header])
                dic_Con["title"] = str_Menu
                
                dic_Output["forms"].append(dic_Con)
                dic_Con = {
                    "title": "",
                    "editable": True,
                    "children": []
                    }                  
            break
                 
    int_Count+=1  
    with open(path + "\\"+str(int_Count)+".json", 'w+', encoding="utf-8") as json_file:
        json.dump(dic_Output,json_file,indent= 4,ensure_ascii=None)    
              
    
      

