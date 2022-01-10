import os, inspect
from pandas import ExcelWriter
import pandas as pd
import glob
import re
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
excel_files = glob.glob(CurDir + "\\Input\\*")
list_df = []
for jfile,i_file in enumerate(excel_files):
    
    xls = pd.ExcelFile(i_file, engine='openpyxl')
    list_sheet_input = xls.sheet_names
    for i_shet in list_sheet_input:
        df_input = pd.read_excel(i_file, sheet_name = i_shet, engine='openpyxl', dtype= object)   
        for index, row in df_input.iterrows():  
            if str(row).find('HỌ VÀ TÊN *') != -1 :
                df_input = pd.read_excel(i_file, sheet_name= i_shet, skiprows = index+1, engine='openpyxl')
                lst_colums = df_input.columns.values
                
                df_output = df_input[0:0]
                for index, row_input in df_input.iterrows():
                    if "SỐ ĐIỆN THOẠI" in lst_colums[7]:   
                        df_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = df_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'].astype(str)
                        row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)']).replace("(+84)","").replace(" ","").replace("DĐ","").replace("-","").replace(".","").replace("SĐT","").strip()
                        if len(str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])) == 9:
                            row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = "0"+str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])
                        if len(str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])) == 8:
                            row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = "00"+str(row_input['SỐ ĐIỆN THOẠI *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)']) 
                    
                    if "SĐT" in lst_colums[7]:   
                        df_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = df_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'].astype(str)
                        row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = str(row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)']).replace("(+84)","").replace(" ","").replace("DĐ","").replace("-","").replace(".","").replace("SĐT","").strip()
                        if len(str(row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])) == 9:
                            row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = "0"+str(row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])
                        if len(str(row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])) == 8:
                            row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'] = "00"+str(row_input['SĐT *\n(10 ký tự bao gồm số 0 đầu, ko có khoảng trống)'])
            
                    df_output = df_output.append(row_input)
        
                list_df.append(df_output)

 
   # i_file = i_file.replace('Input','Output') 
    with ExcelWriter(r"D:\Win\Train Python\wwin-01\BT_EXecl\output"+"\\"+str(jfile)+".xlsx", engine= "xlsxwriter")as writer:
        for n, df in enumerate(list_df):
            df.to_excel(writer,'sheet%s' % n, index= False)
        writer.save()
    list_df = []
   # i_file = i_file.replace('Output','Input') 
   
    # i_file = i_file.replace('Input','Output_1') 
    # with ExcelWriter(i_file, engine= "xlsxwriter")as writer:
    #     for m, df in enumerate(list_df):
    #         lst_col = df.columns.values
    #         new_df = df[[lst_col[1],lst_col[7]]]
    #         new_df.to_excel(writer,'sheet%s' % m, index= False)
    #     writer.save()
    # i_file = i_file.replace('Input','Output_1')  








      
     
       
        
                               
                         
                    
                  
            