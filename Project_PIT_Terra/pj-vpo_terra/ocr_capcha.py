import pytesseract
import os, inspect
import cv2
from PIL import Image

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def Get_Captcha1(CurDir, image):     
    img_cv = cv2.imread(image)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    pytesseract.pytesseract.tesseract_cmd = CurDir + "\\Tesseract-OCR\\tesseract.exe"
    g= pytesseract.image_to_string(img_rgb, config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    # g = pytesseract.image_to_string(Image.open(img_rgb).convert("L"),config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")  # config="-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    captchaResponce= g.replace(" ","").replace("\n","")
   
    return str(captchaResponce)

    # img_array = np.asarray(bg, dtype=np.uint8)
    # gray_image = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(gray_image,180,255,1)
    # img_out2 = cv2.bitwise_not(thresh)

    # cv2.imshow("2", img_out2)						
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
  
# print(Get_Captcha1(CurDir,r"D:\HuyNP\PIT\test capcha\main\capcha\2.jpg")) 
    

