#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for the Math Day Score Keeper application.

This module initializes the main application window and sets up the GUI components.
Created on May 2025
@author: Vishnu Mangalath
"""

import tkinter as tk
from tkinter import font as tkfont
from gui.menu import load_main_menu


def main() -> None:
    """
    Initialize and run the main application window.
    
    Creates the root window, sets up fonts, and loads the main menu.
    """
    root = tk.Tk()
    root.title("Math Day Score Keeper")

    # Create fonts
    large_title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
    med_title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
    body_font = tkfont.Font(family="Helvetica", size=12)

    # Load main menu
    load_main_menu(root, large_title_font, med_title_font, body_font)

    # Start main loop
    root.mainloop()


if __name__ == "__main__":
    main()