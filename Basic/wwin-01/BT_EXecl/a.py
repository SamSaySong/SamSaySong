
import os, inspect
from pandas import ExcelWriter
import pandas as pd
import glob
import re
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
list_df = []
int_count = 0
for i_file in glob.glob(CurDir + "\\Input\\*"):
    if (str(i_file).endswith('.xlsx') or str(i_file).endswith('.xls')) and  "~$" not in i_file:
        if str(i_file).endswith('.xlsb'):
            type_engine = 'pyxlsb'
        elif  str(i_file).endswith('.xls'):
            type_engine = 'xlrd'
        elif  str(i_file).endswith('.xlsx'):
            type_engine = 'openpyxl'
        xls = pd.ExcelFile(i_file, engine=type_engine)
        list_sheet_input = xls.sheet_names
        for i_shet in list_sheet_input:
            df_input = pd.read_excel(i_file, sheet_name = i_shet, engine=type_engine, dtype= object)   
            for index, row in df_input.iterrows():  
                if str(row).find('HỌ VÀ TÊN *') != -1 :
                   
                    df_input = pd.read_excel(i_file, sheet_name= i_shet, skiprows = index+1, engine=type_engine)
                    lst_colums = df_input.columns.values
                    
                    df_output = df_input[0:0]
                    for index, row_input in df_input.iterrows():
                        if "SỐ ĐIỆN THOẠI" in lst_colums[7]:   
                            df_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = df_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'].astype(str)
                            lst_sdt = re.findall(r"\d", str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)']))
                            row_input[lst_colums[7]] = "".join(lst_sdt)
                           
                            if row_input[lst_colums[7]][0:2] == "84" and len(row_input[lst_colums[7]])>10:
                                row_input[lst_colums[7]] = row_input[lst_colums[7]].replace("84","0",1)
                            elif len(row_input[lst_colums[7]]) == 9:
                                row_input[lst_colums[7]] = "0"+row_input[lst_colums[7]]


                            # df_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = df_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'].astype(str)
                            # row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)']).replace("(+84)","").replace(" ","").replace("DĐ","").replace("-","").replace(".","").replace("SĐT","").strip()
                            # if len(str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])) == 9:
                            #     row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = "0"+str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])
                            # if len(str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])) == 8:
                            #     row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = "00"+str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)']) 
                        
                        if "SĐT" in lst_colums[7]:   
                            df_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = df_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'].astype(str)
                            lst_sdt = re.findall(r"\d", str(row_input[lst_colums[7]]))
                            row_input[lst_colums[7]] = "".join(lst_sdt)
                           
                            if row_input[lst_colums[7]][0:2] == "84" and len(row_input[lst_colums[7]])>10:
                                row_input[lst_colums[7]] = row_input[lst_colums[7]].replace("84","0",1)
                            elif len(row_input[lst_colums[7]]) == 9:
                                row_input[lst_colums[7]] = "0"+row_input[lst_colums[7]]                         
                            # df_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = df_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'].astype(str)
                            # row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = str(row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)']).replace("(+84)","").replace(" ","").replace("DĐ","").replace("-","").replace(".","").replace("SĐT","").strip()
                            # if len(str(row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])) == 9:
                            #     row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = "0"+str(row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])
                            # if len(str(row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])) == 8:
                            #     row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = "00"+str(row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])
                
                        df_output = df_output.append(row_input)
          
                    list_df.append(df_output)
       
        i_file = i_file.replace('Input','Output') 
        with ExcelWriter(i_file, engine= "xlsxwriter") as writer:
            for n, df in enumerate(list_df):
                df.to_excel(writer,'sheet%s' % n, index= False)
                
            writer.save()
        i_file = i_file.replace('Output','Input') 
        list_df = []
           

