import os, inspect
from PIL import Image
from pdf2image import convert_from_path
import pytesseract

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_pdf = os.path.abspath(CurDir +"\\doc\\")

pdfFileObj = path_pdf+"\\BIDV_Account statement.pdf"

doc = convert_from_path(pdfFileObj)

path_1, fileName = os.path.split(pdfFileObj)
fileBaseName, fileExtension = os.path.splitext(fileName)

for page_number, page_data in enumerate(doc):
    txt = pytesseract.image_to_string(Image.fromarray(page_data)).encode("utf-8")
    print("Page # {} - {}".format(str(page_number),txt))