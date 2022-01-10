
import datetime
from pynput.keyboard import Key, Controller
from pynput import keyboard
import threading
import pyautogui
import cv2
import numpy as np
import time
# imaaporting the required packages




flag = False
def xvideo(path, file):
    import pyautogui
    import cv2
    import numpy as np

    # Specify resolution
    resolution = (1920, 1080)
    
    # Specify video codec
    codec = cv2.VideoWriter_fourcc(*"XVID")
    day_time = datetime.datetime.now()
    day_time = day_time.strftime('%Y%m%d')
    # Specify name of Output file
    filename = path + "/" +day_time+'_'+ file +".avi"
    
    # Specify frames rate. We can choose any 
    # value and experiment with it
    fps = 20.0
    
    
    # Creating a VideoWriter object
    out = cv2.VideoWriter(filename, codec, fps, resolution)
    
    # Create an Empty window
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    
    # Resize this window
    cv2.resizeWindow("Live", 480, 270)
    
    while True:
        # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()
    
        # Convert the screenshot to a numpy array
        frame = np.array(img)
    
        # Convert it from BGR(Blue, Green, Red) to
        # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # Write it to the output file
        out.write(frame)
        
        # Optional: Display the recording screen
        cv2.imshow('Live', frame)
        
        # Stop recording when we press 'q'
        
        # if cv2.waitKey(1) == ord('q'):
        if flag ==True:
            break
    
    # Release the Video writer
   
    out.release()
    # Destroy all windows
    cv2.destroyAllWindows()

def on_press():
    global flag
    flag=True
    print("stop monitor")
    return flag  


def run():
    path = r"D:\HuyNP\Basic\func_123\recordf"
    name = 'agi147'
    try:
        th=threading.Thread(target=xvideo, args=(path, name))
        th.start()
    except:
        pass
if __name__=='__main__':
    run()

    time.sleep(20)
    on_press()
    











