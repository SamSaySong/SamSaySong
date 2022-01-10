import tabula
import os, inspect
import pandas as pd
from pandas import ExcelWriter

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_pdf = os.path.abspath(CurDir +"\\doc\\")
pdfFileObj = path_pdf+"\\BIDV_Account statement.pdf"

output_img = os.path.abspath(CurDir +"\\Out_put\\")
# list_df= tabula.io.read_pdf(pdfFileObj, pages='all') 

df = tabula.read_pdf(pdfFileObj, pages='all', encoding="utf-8", stream=True)
# convert PDF into CSV
# tabula.io.convert_into(pdfFileObj, output_img+ "\\234.csv", output_format="csv", pages='all')


list_df_out = []
for item in df:
   df = pd.DataFrame(item)
   list_df_out.append(df)

with ExcelWriter(output_img+ "\\234.xlsx", engine= "xlsxwriter")as writer:  
   for n, df in enumerate(list_df_out):
      df.to_excel(writer,f'sheet{n}' , index= False,encoding='utf-8')
   writer.save()

# with ExcelWriter(output_img+ "\\234.xlsx", engine= "xlsxwriter")as writer:
   
#    for n, df in enumerate(list_df_out):
#       df.to_excel(writer,'sheet%s' % n, index= False)
#    writer.save()
