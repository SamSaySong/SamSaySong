
from PIL import Image
import pytesseract
import sys
import os
from pdf2image import convert_from_path
import PyPDF2
import os, inspect
import pandas as pd
from pandas import ExcelWriter

import cv2
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_pdf = os.path.abspath(CurDir +"\\doc\\")
# Path of the pdf
pdfFileObj = open(path_pdf+"\\SMBC - Account statement.pdf", 'rb')

pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
output_img = os.path.abspath(CurDir +"\\output\\")
# pages = pdfReader.numPages

pdfFileObj = path_pdf+"\\BIDV_Account statement.pdf"
pages = convert_from_path(pdfFileObj, output_folder=output_img+"\\")

image_counter = 1

for i in range(len(pages)):
    # Save pages as images in the pdf
	pages[i].save(output_img+ '\\page_'+ str(i) +'.jpg', 'JPEG')

	# Increment the counter to update filename
	image_counter = image_counter + 1

# Variable to get count of total number of pages
filelimit = image_counter-1





lst_terst = []
for i in range(filelimit):
	
	filename = output_img+ "\\page_"+str(i)+".jpg"
	img_cv = cv2.imread(filename)
	img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

	pytesseract.pytesseract.tesseract_cmd = CurDir + "\\Tesseract-OCR\\tesseract.exe"
	text = pytesseract.image_to_string(img_rgb)
	text = text.replace(" ","").replace('-\n', '')	
	lst_terst.append(text)

	
	# df_output = pd.ExcelWriter(output_img+ "\\out_text.xlsx")
	# df_output_1.to_excel(df_output,"Sheet"+str(i), index= False)	
	

with ExcelWriter(output_img+ "\\out_text.xlsx", engine= "xlsxwriter")as writer:
	df_output_1 = pd.DataFrame(lst_terst)
	df_output_1.to_excel(writer,'sheet1' , index= False)
writer.save()
	
	# for n, df in enumerate(df_output_1):
	# 	df.to_excel(writer,'sheet%s' % n, index= False)
	# writer.save()



