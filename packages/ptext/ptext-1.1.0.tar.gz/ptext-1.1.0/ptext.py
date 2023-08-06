#Printing text, by: TimoXBeR
#This module makes printing effect for print().
#Soon it will work with canvas from tkinter.

import time
from tkinter import *

def printing(text_, time_=0.1):
    #Makes printing effect in console
    for i in text_:
        time.sleep(time_)
        print(i, end='', flush=True)
