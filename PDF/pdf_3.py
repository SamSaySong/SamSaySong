
import sys
import os
import PyPDF2
import pdftables_api
import os, inspect
import pandas as pd
from pandas import ExcelWriter


CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_pdf = os.path.abspath(CurDir +"\\doc\\")

pdfFileObj = open(path_pdf+"\\BIDV_Account statement.pdf", 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pageObj = pdfReader.getPage(0)
print(pageObj.extractText())

# Path of the pdf

# pdfFileObj = path_pdf+"\\SMBC - Account statement.pdf"

# output_img = os.path.abspath(CurDir +"\\output\\")
# conversion = pdftables_api.Client ('klyqe4a8jhyy', timeout =(120 , 3600)) #,timeout =(60 , 3600)

# c.xml(pdfFileObj,output_img + "\\out_text_2.xml")

# conversion.xlsx_single(pdfFileObj, output_img + "\\out_text_3.xlsx") 