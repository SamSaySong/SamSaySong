from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib
import os, inspect
import ssl
import glob

# CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# path_img = os.path.abspath(CurDir +"\\image")
# file_img = glob.glob(path_img + "\\*.jpg")

# file_txt = glob.glob(os.path.abspath(CurDir +"\\input") + "\\*.txt")

def message(header="",text="", file_img=None, file_dinhkem=None):

  msg = MIMEMultipart()
  msg.attach(MIMEText(text))
  
  if file_img is not None:
    # Check whether we have the
    # lists of images or not!

    # if type(img) is not list:
    #     # if it isn't a list, make it one
    #     img = [img]  

    for one_img in file_img:
      img_data = open(one_img, 'rb').read()
      msg.attach(MIMEImage(img_data, name=os.path.basename(one_img)))

  if file_dinhkem is not None:

    for one_file_dinhkem in file_dinhkem:
    
      with open(one_file_dinhkem, 'rb') as f:
          
        # Read in the attachment using MIMEApplication
        file = MIMEApplication(f.read(),name=os.path.basename(one_file_dinhkem))
          
      file['Content-Disposition'] = f'attachment;\filename="{os.path.basename(one_file_dinhkem)}"'
        
      # At last, Add the attachment to our message object
      msg.attach(file)

  msg['Subject'] = header

  return msg

def send_mail():

  smtp = smtplib.SMTP('smtp.gmail.com', 587)
  smtp.ehlo()
  context = ssl.create_default_context()

  # bật quyền truy cập
  smtp.starttls(context= context)
  smtp.login('email@gmail.com', 'passsword')

  msg = message(header="Nhắn gửi yêu thương", text="435345345345texxt", file_img = file_img, file_dinhkem = file_txt)

  to = ["1235@gmail.com"]
  smtp.sendmail(from_addr="email@gmail.com", to_addrs = to, msg = msg.as_string())    
  smtp.quit()

# if __name__ == "__main__":   
  
#   import time
#   import schedule
  
#   schedule.every(2).seconds.do(send_mail)
#   # schedule.every(10).minutes.do(send_mail)
#   # schedule.every().hour.do(send_mail)
#   # schedule.every().day.at("10:30").do(send_mail)
#   # schedule.every(5).to(10).minutes.do(send_mail)
#   # schedule.every().monday.do(send_mail)
#   # schedule.every().wednesday.at("13:15").do(send_mail)
#   # schedule.every().minute.at(":17").do(send_mail)
  
#   while True:
#     schedule.run_pending()
#     time.sleep(1)


msg = MIMEMultipart()
msg['From'] = 'home.mie.2021@gmail.com'
msg['To'] = 'bobo.pro.dn@gmail.com'
msg['Subject'] = 'simple email in python'
message = 'here is the email'
msg.attach(MIMEText(message))

mailserver = smtplib.SMTP('smtp.gmail.com',587)
# identify ourselves to smtp gmail client
mailserver.ehlo()
# secure our email with tls encryption
mailserver.starttls()
# re-identify ourselves as an encrypted connection
mailserver.ehlo()
mailserver.login('home.mie.2021@gmail.com', 'Huy@123456')

mailserver.sendmail('home.mie.2021@gmail.com','bobo.pro.dn@gmail.com',msg.as_string())

mailserver.quit()
