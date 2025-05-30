#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 2025
 
@author: Vishnu Mangalath
"""

import tkinter as tk
from tkinter import font as tkfont
from Lib.Windows.Menu import LoadMainMenu

def main():
    root = tk.Tk()
    root.title("Math Day Score Keeper")

    # Create fonts
    LargeTitleFont = tkfont.Font(family="Helvetica", size=24, weight="bold")
    MedTitleFont = tkfont.Font(family="Helvetica", size=16, weight="bold")
    BodyFont = tkfont.Font(family="Helvetica", size=12)

    # Load main menu
    LoadMainMenu(root, LargeTitleFont, MedTitleFont, BodyFont)

    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    main() 