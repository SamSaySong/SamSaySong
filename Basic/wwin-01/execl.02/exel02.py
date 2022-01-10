import pandas as pd
import os
import inspect

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

df_input = pd.read_excel(CurDir + "\\input\\Input.xlsx", sheet_name= 0 , header= 1,engine= "openpyxl")
df_master = pd.read_excel(CurDir + "\\Master.xlsx", sheet_name= 0 ,engine = "openpyxl")

for i in range (len(df_input)):
    dt_temp = df_master.loc[df_master["Mã số thuế"] == df_input.loc[i,"MST đơn vị mua hàng"]]
    
    if len(dt_temp) > 0:
        df_input.loc[i,'Họ tên người mua hàng'] = str(dt_temp.iloc[0]['Tên khách hàng (*)'])
    
countSheet = 0
countLenHD = 0
countSoHD =0
df_Output = df_input[0:0]
writer = pd.ExcelWriter(CurDir + '\\output\\Output_1.xlsx')
for i in range (len(df_input)-1):
    df_Output.loc[i] = df_input.loc[i]   
    df_Output.to_excel(writer, sheet_name='Sheet'+str(countSheet), index=False, engine='openpyxl')    
    
    if df_input.loc[i,'Số HĐ'] != df_input.loc[i+1,'Số HĐ']:
        countSoHD +=1
    if countSoHD%3==0 and countSoHD !=0:        
        countSoHD =0
        countSheet+=1
        df_Output = df_input[0:0]
    countLenHD+=1

if df_input.loc[countLenHD-1,'Số HĐ'] != df_input.loc[countLenHD,'Số HĐ'] and countSoHD < 3 :
    df_Output.loc[countLenHD] = df_input.loc[countLenHD]
    df_Output.to_excel(writer, sheet_name='Sheet'+str(countSheet) , index=False, engine='openpyxl')

elif df_input.loc[countLenHD-1,'Số HĐ'] == df_input.loc[countLenHD,'Số HĐ'] and countSoHD >=3 :
    df_Output = df_input[0:0]
    df_Output.to_excel(writer, sheet_name='Sheet'+str(countSheet)+str(1), index=False, engine='openpyxl')
    df_Output.loc[countLenHD] = df_input.loc[countLenHD]
    
writer.save()
writer.close()




















# df_input = df_input.dropna(axis=0, subset=['MST đơn vị mua hàng'])

# lst_TenKhachHang = df_master["Tên khách hàng (*)"].values
# lst_MST = df_master["Mã số thuế"].values
# lst_TenKH = []
# for idx, row in df_input.iterrows():
#     for i_idx, i_row in enumerate(lst_MST):
#         if row["MST đơn vị mua hàng"] == i_row:
#             lst_TenKH.append(lst_TenKhachHang[i_idx])
#             break



# df_input.insert(loc = 1, column="Họ tên người mua hàng", value= lst_TenKH )

# print(df_input)
# df_output = pd.ExcelFile(CurDir + "\\output\\Output_1.xlsx", engine= "openpyxl")
# df_input.to_excel(df_output, sheet_name=0 ,index=False)
# df_output.close()