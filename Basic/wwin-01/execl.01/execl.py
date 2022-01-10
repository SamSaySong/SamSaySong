
import pandas as pd
import os
import inspect
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

df_input_1 = pd.read_excel(CurDir+"\\NhanVien_1.xlsx",skipfooter= 2 ,skiprows= 5 ,engine="openpyxl")
df_input_2 = pd.read_excel(CurDir+"\\thongtinnhanvien.xlsx",skipfooter= 6, skiprows= 3 ,engine="openpyxl")

lst_Ten = df_input_1["Tên"].values
lst_MSNV = df_input_2["MSNV"].values

lst_TTNV = []

for idx, row in df_input_1.iterrows():
    for i_idx, i_row in enumerate(lst_MSNV):
        if row["MSNV"] == i_row:
            lst_TTNV.append(lst_Ten[i_idx])
            break
    
print(lst_TTNV)
df_input_2.insert(loc= 1, column="Họ và Tên", value= lst_TTNV)
df_output = pd.ExcelWriter(CurDir + "\\thongtinnhanvien_1.xlsx",datetime_format='dd/mm/yyyy',engine="openpyxl")
df_input_2.to_excel(df_output, sheet_name="SVTT",index=False)
df_output.save()



# file_input_2 = file_input_2.drop(["Unnamed: 12","Unnamed: 13"], axis = 1)
# temp = file_input_1["Tên"]
# file_input_2.insert(0,"Tên",temp) 

# df1 = pd.DataFrame(file_input_2[0:200])
# file_output = pd.ExcelWriter(r"D:\Win\Train Python\wwin-01\execl01\thongtinnhanvien_1.xlsx",datetime_format='dd mm yyyy')
# df1.to_excel(file_output, sheet_name="SVTT", index= False ,startcol=0, startrow = 3)
# file_output.save()