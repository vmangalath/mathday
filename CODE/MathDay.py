# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 10:52:09 2019
 
@author: jp
"""

import Tkinter as tk
import tkFont
import csv
import os
from Lib.Windows.Menu import LoadMainMenu

root = tk.Tk()

LargeTitleFont = tkFont.Font(family='Courier', size=24, weight='bold')
MedTitleFont = tkFont.Font(family='Courier', size=18)
BodyFont = tkFont.Font(family='Courier', size=12) 


Menu1 = LoadMainMenu(root,LargeTitleFont,MedTitleFont,BodyFont)
root.mainloop()