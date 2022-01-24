import time
from django.urls import clear_script_prefix
import pandas as pd
from time import sleep
import os, inspect, sys
import re
import glob
from PIL import Image
import datetime
import shutil
CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# import logging
# import os, inspect, sys
# from time import sleep

# global LOG_info
# """ Ghi log """
# logging.basicConfig(format=' %(asctime)s [%(levelname)s] >>> ------  %(message)s  <<<------------------', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)
# logFormatter = logging.Formatter(' %(asctime)s [%(levelname)s] >>> ------  %(message)s  <<<------------------', datefmt='%d/%m/%Y %H:%M:%S')
# LOG_info = logging.info
# LOG_warn = logging.warning
# FileHandler = logging.FileHandler(CurDir + "\\log.txt", 'a+', 'utf-8')
# FileHandler.setFormatter(logFormatter)
# logging.getLogger().addHandler(FileHandler)


# try:
#     for i in range(1,10):
#         if i > "5":
#             print(i)
# except Exception as e:
#     LOG_info('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(Exception).__name__, str(e))

# script mode

# import time
# import sys

# animation = "|/-\\"

# for i in range(101):
#     time.sleep(0.05)
#     sys.stdout.write("\r" + animation[i % len(animation)]+" loading... "+str(i)+"%")
#     sys.stdout.flush()

from calendar import monthrange
num_days = monthrange(2021, 7)[1] # num_days = 28.
print(num_days) # Prints 28.