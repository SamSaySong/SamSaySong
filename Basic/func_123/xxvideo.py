
import time
import socket
import os, inspect, sys
import subprocess

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

path_file = r'D:\HuyNP\Basic\func_123\recordf'
name = 'video_test2022'

str_cmd = '"C:/Program Files/VideoLAN/VLC/vlc.exe" -I dummy screen:// --one-instance --extraintf rc --rc-quiet --rc-host 127.0.0.1:8082 --screen-fps=25 --quiet --sout "#transcode{vcodec=h264,vb072}:standard{access=file,mux=mp4,dst="D:/INFOR/vlc-output-terminal.mp4"}'
str_1 = '"C:/Program Files/VideoLAN/VLC/vlc.exe" screen:// --qt-start-minimized :screen-fps=25 :quiet :sout=#transcode{vcodec=h264,vb072}:standard{access=file,mux=mp4,dst="D:/INFOR/vlc-output-terminal.mp4"}'

'"C:\Program Files\VideoLAN\VLC/vlc.exe" -I dummy screen:// --one-instance --extraintf rc --rc-quiet --rc-host 127.0.0.1:8082 --screen-fps=25 --quiet --sout "#transcode{vcodec=h264,vb072}:standard{access=file,mux=mp4,dst="D:/INFOR/output-terminal.mp4"} vlc://quit'


def shutdown():
  
   
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 8082))
    s.sendall('quit'.encode())
    s.shutdown(socket.SHUT_WR)

# shutdown()




def star_123(path_record, name_record):
    import datetime

    date_time = datetime.datetime.now()
    str_date_time = date_time.strftime("%d%m%Y")
    time.sleep(1)
    subprocess.Popen('"C:/Program Files (x86)/VideoLAN/VLC/vlc.exe" -I dummy screen:// --one-instance --extraintf rc --rc-quiet --rc-host 127.0.0.1:8082 --screen-fps=25 --quiet --sout "#transcode{vcodec=h264,vb072}:standard{access=file,mux=mp4,dst="D:\HuyNP\Basic/func_123/recordf/'+str_date_time+"_"+name_record+'.avi"}', encoding = "utf-8")

    time.sleep(25)
    
    shutdown()
star_123(path_file,name)


