#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main menu and GUI components for the Math Day Score Keeper application.

This module contains all the GUI classes that handle the user interface,
including the main menu, setup menu, and competition management screens.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from functools import partial
from typing import Optional, List, Tuple, Any
from gui.dialogue_boxes import (
    SetupMenuRegisterSchool, SetupMenuNewSchool, SetupMenuModifyRegisterSchool,
    SetupMenuCompetitionName, SwissRoundNumberselector, SchoolKeySelector,
    SiteSelector, SchoolNameSelector
)
from core.structures import (
    PreviousSchoolList, RegisterSchoolList, RegisteredSchool,
    PreviousSchool, CompetitionSchoolList
)

class MainMenuBody:
    """
    Main menu interface for the Math Day Score Keeper application.
    
    This class handles the main menu screen, providing options to set up
    a new competition, run an existing competition, or exit the application.
    
    Attributes:
        master (tk.Frame): The parent frame for this menu
        root (tk.Tk): The root window of the application
        title_font (tk.font.Font): Font for main titles
        med_title_font (tk.font.Font): Font for medium titles
        body_font (tk.font.Font): Font for body text
        data_dir (str): Directory for storing competition data
    """
    
    def __init__(self,
                 master: tk.Frame,
                 root: tk.Tk,
                 title_font: tk.font.Font,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 data_dir: str = '../data/') -> None:
        """
        Initialize the main menu interface.
        
        Args:
            master: The parent frame for this menu
            root: The root window of the application
            title_font: Font for main titles
            med_title_font: Font for medium titles
            body_font: Font for body text
            data_dir: Directory for storing competition data
        """
        self.title_font = title_font
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.master = master
        self.root = root
        self.data_dir = data_dir

        # Create main frame
        main_frame = tk.Frame(self.master, height=10, width=10, bd=1)
        main_frame.grid(row=0, column=0)

        # Add title
        title_text = 'Math Day Score Keeper Program'
        tk.Label(main_frame, text=title_text, bd=4, font=self.title_font).grid(row=0, column=0)

        # Add menu buttons
        setup_button = tk.Button(
            main_frame,
            text="1. Set-Up Competition",
            font=self.body_font,
            width=32,
            command=self.goto_setup_menu
        )
        setup_button.grid(row=1, column=0)

        run_button = tk.Button(
            main_frame,
            text="2. Run Competition",
            font=self.body_font,
            width=32,
            command=self.goto_comp_main
        )
        run_button.grid(row=2, column=0)

        exit_button = tk.Button(
            main_frame,
            text="3. Exit",
            font=self.body_font,
            width=32,
            command=self.exit
        )
        exit_button.grid(row=3, column=0)

    def exit(self) -> None:
        """Close the application."""
        self.root.destroy()

    def clear_body(self) -> None:
        """Remove all widgets from the main frame."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def goto_setup_menu(self) -> None:
        """Navigate to the competition setup menu."""
        self.clear_body()
        SetupMenuBody(
            self.master,
            self.root,
            self.title_font,
            self.med_title_font,
            self.body_font,
            self.data_dir
        )

    def goto_comp_main(self) -> None:
        """Navigate to the competition main menu after loading a competition file."""
        file_name = filedialog.askopenfilename(
            initialdir=self.data_dir,
            title="Select Competition File",
            filetypes=(("Comma Separated Files", "*.csv"), ('All Files', '*'))
        )

        if file_name:
            self.clear_body()
            master_dir = self.data_dir + "master/"
            competition = CompetitionSchoolList(
                school_list=[],
                file=file_name,
                master_dir=master_dir,
                data_dir=self.data_dir
            )
            competition.read_from_file()
            CompMainMenuBody(
                self.master,
                self.root,
                self.title_font,
                self.med_title_font,
                self.body_font,
                competition
            )

class SetupMenuBody:
    """
    Competition setup menu interface.
    
    This class handles the competition setup screen, allowing users to:
    - Add new schools to the master list
    - Register schools for the competition
    - Modify registered schools
    - Remove schools from registration
    - Order schools by key
    - Save and exit setup
    
    Attributes:
        master (tk.Frame): The parent frame for this menu
        root (tk.Tk): The root window of the application
        title_font (tk.font.Font): Font for main titles
        med_title_font (tk.font.Font): Font for medium titles
        body_font (tk.font.Font): Font for body text
        data_dir (str): Directory for storing competition data
        master_dir (str): Directory for storing master files
        prev_list (PreviousSchoolList): List of schools from previous competitions
        registered (RegisterSchoolList): List of schools registered for this competition
        list_box1 (tk.Listbox): Listbox for displaying previous schools
        list_box2 (tk.Listbox): Listbox for displaying registered schools
    """
    
    def __init__(self,
                 master: tk.Frame,
                 root: tk.Tk,
                 title_font: tk.font.Font,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 data_dir: str) -> None:
        """
        Initialize the setup menu interface.
        
        Args:
            master: The parent frame for this menu
            root: The root window of the application
            title_font: Font for main titles
            med_title_font: Font for medium titles
            body_font: Font for body text
            data_dir: Directory for storing competition data
        """
        self.title_font = title_font
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.master = master
        self.root = root
        self.data_dir = data_dir
        self.master_dir = self.data_dir + "master/"

        # Initialize school lists
        self.prev_list = PreviousSchoolList(master_file=self.master_dir + "Schools.csv")
        self.prev_list.read_from_file()
        self.registered = RegisterSchoolList(school_list=[])

        # Create main frames
        title_frame = tk.Frame(master, bd=1)
        title_frame.grid(row=0, column=0)
        title_text = 'Competition Set-Up\n'
        tk.Label(title_frame, text=title_text, bd=1, font=self.title_font).grid(row=0, column=0)

        content_frame = tk.Frame(master, bd=1)
        content_frame.grid(row=1, column=0)

        button_frame = tk.Frame(master, bd=1)
        button_frame.grid(row=2, column=0)

        # Create subframes
        prev_schools_frame = tk.Frame(content_frame, bd=1)
        prev_schools_frame.grid(row=0, column=0)

        reg_schools_frame = tk.Frame(content_frame, bd=1)
        reg_schools_frame.grid(row=0, column=1)

        action_frame = tk.Frame(content_frame, bd=1)
        action_frame.grid(row=1, column=0)

        control_frame = tk.Frame(content_frame, bd=1)
        control_frame.grid(row=1, column=1)

        # Add action buttons
        tk.Button(
            action_frame,
            text="New",
            width=10,
            font=self.body_font,
            command=self.add_school_to_list
        ).grid(row=0, column=0)
        
        tk.Button(
            action_frame,
            text="Register",
            width=10,
            font=self.body_font,
            command=self.register_school
        ).grid(row=0, column=1)

        # Add control buttons
        tk.Button(
            control_frame,
            text="Modify",
            width=10,
            font=self.body_font,
            command=self.modify
        ).grid(row=0, column=0)
        
        tk.Button(
            control_frame,
            text="Remove",
            width=10,
            font=self.body_font,
            command=self.remove
        ).grid(row=0, column=1)
        
        tk.Button(
            control_frame,
            text="Order",
            width=10,
            font=self.body_font,
            command=self.order
        ).grid(row=0, column=2)
        
        tk.Button(
            control_frame,
            text="Done",
            width=10,
            font=self.body_font,
            command=self.done
        ).grid(row=0, column=3)
        
        tk.Button(
            control_frame,
            text="Back",
            width=10,
            font=self.body_font,
            command=self.goto_main_menu
        ).grid(row=1, column=3)

        # Add previous schools list
        tk.Label(
            prev_schools_frame,
            text="Previous School List",
            bd=1,
            font=self.med_title_font
        ).grid(row=0, column=0)

        self.list_box1 = tk.Listbox(prev_schools_frame, width=40, font=self.body_font)
        self.list_box1.grid(row=1, column=0)
        self.list_box1.bind('<Double-1>', self.register_school)

        scrollbar = tk.Scrollbar(prev_schools_frame, orient="vertical")
        scrollbar.config(command=self.list_box1.yview)
        scrollbar.grid(row=1, column=1)
        self.list_box1.config(yscrollcommand=scrollbar.set)

        # Populate previous schools list
        for i, school in enumerate(self.prev_list.school_list):
            self.list_box1.insert(i, school.name)

        # Add registered schools list
        tk.Label(
            reg_schools_frame,
            text="Registered School List",
            bd=1,
            font=self.med_title_font
        ).grid(row=0, column=0)
        
        self.list_box2 = tk.Listbox(reg_schools_frame, width=80, font=self.body_font)
        self.list_box2.grid(row=1, column=0)

        scrollbar = tk.Scrollbar(reg_schools_frame, orient="vertical")
        scrollbar.config(command=self.list_box2.yview)
        scrollbar.grid(row=1, column=1)
        self.list_box2.config(yscrollcommand=scrollbar.set)
        self.list_box2.bind('<Double-1>', self.modify)

        # Add header to registered schools list
        header_string = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key', 'School', 'Location', 'Z Score')
        self.list_box2.insert(1, header_string)

    def add_school_to_list(self) -> None:
        """Add a new school to the master list and register it."""
        add_school_dialog = SetupMenuNewSchool(
            self.root,
            self.med_title_font,
            self.body_font,
            self.registered,
            self.prev_list
        )

        sel_key = add_school_dialog.sel_key
        school_name = add_school_dialog.new_school_name
        school_location = add_school_dialog.new_school_location

        if sel_key is not None:
            # Create and add new school
            school_hist = PreviousSchool(school_name, school_location, 0.0)
            school_reg = school_hist.register(sel_key)

            self.prev_list.add_to_list(school_hist)
            self.prev_list.sort_list()
            self.prev_list.write_to_file()

            self.registered.add_to_list(school_reg)

            # Update previous schools list
            self.list_box1.delete(0, tk.END)
            for i, school in enumerate(self.prev_list.school_list):
                self.list_box1.insert(i, school.name)

            # Add to registered schools list
            num_string = "{:2.3f}".format(0)
            school_string = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                school_reg.key, school_reg.name, school_reg.location, num_string
            )
            self.list_box2.insert(1 + len(self.registered.school_list), school_string)

    def register_school(self, event: Optional[tk.Event] = None) -> None:
        """
        Register a school from the previous schools list.
        
        Args:
            event: Optional event that triggered this method
        """
        item = self.list_box1.get('active')  # get clicked item
        school = self.prev_list.find_name(item)

        school_dialog = SetupMenuRegisterSchool(
            self.root,
            school,
            self.med_title_font,
            self.body_font,
            self.registered
        )
        sel_key = school_dialog.sel_key

        if sel_key is not None:
            reg_school = school.register(sel_key)
            num_string = "{:2.3f}".format(reg_school.hist_z_score)
            school_string = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                reg_school.key, reg_school.name, reg_school.location, num_string
            )
            self.list_box2.insert(2 + len(self.registered.school_list), school_string)
            self.registered.add_to_list(reg_school)

    def modify(self, event: Optional[tk.Event] = None) -> None:
        """
        Modify a registered school's information.
        
        Args:
            event: Optional event that triggered this method
        """
        selected_item = self.list_box2.get('active')
        selected_item_key = selected_item.split()[0]

        if selected_item_key != 'Key':
            school = self.registered.find_key(selected_item_key)
            self.registered.remove_from_list(school)

            # Modify school
            modify_school_dialog = SetupMenuModifyRegisterSchool(
                self.root,
                school,
                self.registered,
                self.med_title_font,
                self.body_font
            )
            sel_key = modify_school_dialog.sel_key

            if sel_key is not None:
                # Update school with new key
                school.key = sel_key
                self.registered.add_to_list(school)

                # Update registered schools list
                self.list_box2.delete(0, tk.END)
                header_string = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key', 'School', 'Location', 'Z Score')
                self.list_box2.insert(0, header_string)

                for i, school in enumerate(self.registered.school_list):
                    num_string = "{:2.3f}".format(school.hist_z_score)
                    school_string = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                        school.key, school.name, school.location, num_string
                    )
                    self.list_box2.insert(i + 1, school_string)

    def remove(self) -> None:
        """Remove a school from the registered list."""
        selected_item = self.list_box2.get('active')
        selected_item_key = selected_item.split()[0]

        if selected_item_key != 'Key':
            school = self.registered.find_key(selected_item_key)
            self.registered.remove_from_list(school)

            # Update registered schools list
            self.list_box2.delete(0, tk.END)
            header_string = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key', 'School', 'Location', 'Z Score')
            self.list_box2.insert(0, header_string)

            for i, school in enumerate(self.registered.school_list):
                num_string = "{:2.3f}".format(school.hist_z_score)
                school_string = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                    school.key, school.name, school.location, num_string
                )
                self.list_box2.insert(i + 1, school_string)

    def order(self) -> None:
        """Sort the registered schools list by key."""
        self.registered.sort_list()

        # Update registered schools list
        self.list_box2.delete(0, tk.END)
        header_string = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key', 'School', 'Location', 'Z Score')
        self.list_box2.insert(0, header_string)

        for i, school in enumerate(self.registered.school_list):
            num_string = "{:2.3f}".format(school.hist_z_score)
            school_string = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                school.key, school.name, school.location, num_string
            )
            self.list_box2.insert(i + 1, school_string)

    def done(self) -> None:
        """Save the competition setup and proceed to competition name dialog."""
        if not self.registered.valid_key_order():
            messagebox.showerror(
                "Error",
                "All keys must be valid (one letter followed by one number)."
            )
            return

        competition_dialog = SetupMenuCompetitionName(
            self.root,
            self.med_title_font,
            self.body_font,
            self.registered,
            self.data_dir
        )

        if competition_dialog.competition_name:
            self.goto_main_menu()

    def clear_body(self) -> None:
        """Remove all widgets from the main frame."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def goto_main_menu(self) -> None:
        """Return to the main menu."""
        self.clear_body()
        MainMenuBody(
            self.master,
            self.root,
            self.title_font,
            self.med_title_font,
            self.body_font,
            self.data_dir
        )

class CompMainMenuBody:
    """
    Competition main menu interface.
    
    This class handles the main competition screen, providing options to:
    - Enter Group Contest scores
    - Enter Swiss Contest scores
    - Enter Cross Contest scores
    - Enter Relay Contest scores
    - Generate reports
    - Return to main menu
    
    Attributes:
        master (tk.Frame): The parent frame for this menu
        root (tk.Tk): The root window of the application
        title_font (tk.font.Font): Font for main titles
        med_title_font (tk.font.Font): Font for medium titles
        body_font (tk.font.Font): Font for body text
        competition (CompetitionSchoolList): The current competition data
    """
    
    def __init__(self,
                 master: tk.Frame,
                 root: tk.Tk,
                 title_font: tk.font.Font,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 competition: CompetitionSchoolList) -> None:
        """
        Initialize the competition main menu interface.
        
        Args:
            master: The parent frame for this menu
            root: The root window of the application
            title_font: Font for main titles
            med_title_font: Font for medium titles
            body_font: Font for body text
            competition: The current competition data
        """
        self.title_font = title_font
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.master = master
        self.root = root
        self.competition = competition

        # Create main frame
        main_frame = tk.Frame(master, bd=1)
        main_frame.grid(row=0, column=0)

        # Add title
        title_text = 'Competition Main Menu\n'
        tk.Label(main_frame, text=title_text, bd=1, font=self.title_font).grid(row=0, column=0)

        # Add menu buttons
        group_button = tk.Button(
            main_frame,
            text="1. Group Contest",
            font=self.body_font,
            width=32,
            command=self.goto_group_menu
        )
        group_button.grid(row=1, column=0)

        swiss_button = tk.Button(
            main_frame,
            text="2. Swiss Contest",
            font=self.body_font,
            width=32,
            command=self.goto_swiss_menu
        )
        swiss_button.grid(row=2, column=0)

        cross_button = tk.Button(
            main_frame,
            text="3. Cross Contest",
            font=self.body_font,
            width=32,
            command=self.goto_cross_menu
        )
        cross_button.grid(row=3, column=0)

        relay_button = tk.Button(
            main_frame,
            text="4. Relay Contest",
            font=self.body_font,
            width=32,
            command=self.goto_relay_menu
        )
        relay_button.grid(row=4, column=0)

        report_button = tk.Button(
            main_frame,
            text="5. Run Report",
            font=self.body_font,
            width=32,
            command=self.run_report
        )
        report_button.grid(row=5, column=0)

        back_button = tk.Button(
            main_frame,
            text="6. Back to Main Menu",
            font=self.body_font,
            width=32,
            command=self.goto_main_menu
        )
        back_button.grid(row=6, column=0)

    def goto_group_menu(self) -> None:
        """Navigate to the Group Contest menu after selecting a school."""
        school_dialog = SchoolKeySelector(self.root, self.med_title_font, self.body_font, self.competition)
        school_key = school_dialog.sel_key

        if school_key:
            self.clear_body()
            SingleSchoolContestBody(
                self.master,
                self.root,
                self.title_font,
                self.med_title_font,
                self.body_font,
                self.competition,
                school_key,
                'Group',
                10 # Pass the number of questions, not a list
            )

    def goto_swiss_menu(self) -> None:
        """Navigate to the Swiss Contest menu after selecting a round and site."""
        round_dialog = SwissRoundNumberselector(self.root, self.med_title_font, self.body_font)
        round_num = round_dialog.sel_key

        if round_num:
            site_dialog = SiteSelector(self.root, self.med_title_font, self.body_font, self.competition)
            site = site_dialog.sel_key

            if site:
                self.clear_body()
                SwissContestBody(
                    self.master,
                    self.root,
                    self.title_font,
                    self.med_title_font,
                    self.body_font,
                    self.competition,
                    round_num,
                    site
                )

    def goto_cross_menu(self) -> None:
        """Navigate to the Cross Contest menu after selecting a school."""
        school_dialog = SchoolKeySelector(self.root, self.med_title_font, self.body_font, self.competition)
        school_key = school_dialog.sel_key

        if school_key:
            self.clear_body()
            SingleSchoolContestBody(
                self.master,
                self.root,
                self.title_font,
                self.med_title_font,
                self.body_font,
                self.competition,
                school_key,
                'Cross',
                10 # Pass the number of questions, not a list
            )

    def goto_relay_menu(self) -> None:
        """Navigate to the Relay Contest menu after selecting a school."""
        school_dialog = SchoolKeySelector(self.root, self.med_title_font, self.body_font, self.competition)
        school_key = school_dialog.sel_key

        if school_key:
            self.clear_body()
            SingleSchoolContestBody(
                self.master,
                self.root,
                self.title_font,
                self.med_title_font,
                self.body_font,
                self.competition,
                school_key,
                'Relay',
                5 # Pass the number of questions, not a list
            )

    def run_report(self) -> None:
        """Navigate to the Report menu."""
        self.clear_body()
        ReportMenu(
            self.master,
            self.root,
            self.title_font,
            self.med_title_font,
            self.body_font,
            self.competition
        )

    def clear_body(self) -> None:
        """Remove all widgets from the main frame."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def goto_main_menu(self) -> None:
        """Return to the main menu."""
        self.clear_body()
        MainMenuBody(
            self.master,
            self.root,
            self.title_font,
            self.med_title_font,
            self.body_font,
            self.data_dir
        )

class SingleSchoolContestBody:
    """
    Interface for managing individual school contest scores.
    
    This class provides a GUI for entering and managing scores for a single school
    in various contests (Group, Cross, Relay). It allows users to:
    - View and edit scores for each question
    - Navigate between schools
    - Validate and save score entries
    - Return to the competition main menu
    
    Attributes:
        master (tk.Frame): The parent frame for this menu
        root (tk.Tk): The root window of the application
        title_font (tk.font.Font): Font for main titles
        med_title_font (tk.font.Font): Font for medium titles
        body_font (tk.font.Font): Font for body text
        competition (CompetitionSchoolList): The current competition data
        school_key (str): The key identifier for the current school
        contest_name (str): The name of the current contest (Group/Cross/Relay)
        question_grouping (int): Number of questions in the contest
        school (CompetitionSchool): The current school being scored
    """
    
    def __init__(self,
                 master: tk.Frame,
                 root: tk.Tk,
                 title_font: tk.font.Font,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 competition: CompetitionSchoolList,
                 school_key: str,
                 contest_name: str,
                 question_grouping: int) -> None:
        """
        Initialize the single school contest interface.
        
        Args:
            master: The parent frame for this menu
            root: The root window of the application
            title_font: Font for main titles
            med_title_font: Font for medium titles
            body_font: Font for body text
            competition: The current competition data
            school_key: The key identifier for the current school
            contest_name: The name of the current contest (Group/Cross/Relay)
            question_grouping: Number of questions in the contest
        """
        self.title_font = title_font
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.master = master
        self.root = root
        self.competition = competition
        self.school_key = school_key
        self.contest_name = contest_name
        self.question_grouping = question_grouping
        self.school = competition.find_key(school_key)

        # Create main frame
        main_frame = tk.Frame(master, bd=1)
        main_frame.grid(row=0, column=0)

        # Add title
        title_text = f'{contest_name} Contest\n'
        tk.Label(main_frame, text=title_text, bd=1, font=self.title_font).grid(row=0, column=0)

        # Create content frame
        content_frame = tk.Frame(master, bd=1)
        content_frame.grid(row=1, column=0)

        # Create school info frame
        school_info_frame = tk.Frame(content_frame, bd=1)
        school_info_frame.grid(row=0, column=0)

        # Create key info frame
        key_info_frame = tk.Frame(content_frame, bd=1)
        key_info_frame.grid(row=0, column=1)

        # Create navigation frame
        nav_frame = tk.Frame(content_frame, bd=1)
        nav_frame.grid(row=1, column=0)

        # Create score entry frame
        score_frame = tk.Frame(content_frame, bd=1)
        score_frame.grid(row=1, column=1)

        # Add school info
        tk.Label(school_info_frame, text="School", bd=1, font=self.med_title_font).grid(row=0, column=0)
        self.school_name = tk.Label(school_info_frame, text=self.school.name, bd=1, font=self.body_font)
        self.school_name.grid(row=1, column=0)
        self.school_name.bind('<Button-1>', self.choose_school_name)

        # Add key info
        tk.Label(key_info_frame, text="Key", bd=1, font=self.med_title_font).grid(row=0, column=0)
        self.school_key_label = tk.Label(key_info_frame, text=self.school.key, bd=1, font=self.body_font)
        self.school_key_label.grid(row=1, column=0)
        self.school_key_label.bind('<Button-1>', self.choose_school_key)

        # Add navigation buttons
        tk.Button(nav_frame, text="Next School", width=10, font=self.body_font, 
                 command=self.next_school).grid(row=0, column=0)
        tk.Button(nav_frame, text="Back", width=10, font=self.body_font, 
                 command=self.goto_comp_main).grid(row=0, column=1)

        # Add score entry fields
        score_entry_frame = tk.Frame(score_frame, bd=1)
        score_entry_frame.grid(row=0, column=0)

        for i in range(question_grouping):
            # Add question label
            tk.Label(score_entry_frame, text=f"Q{i+1}", bd=1, 
                    font=self.body_font).grid(row=0, column=i)
            
            # Add score entry field
            entry = tk.Entry(score_entry_frame, width=5, font=self.body_font)
            entry.grid(row=1, column=i)
            
            # Add event bindings
            entry.bind('<FocusOut>', partial(self.validate_focus_left, i))
            entry.bind('<Return>', partial(self.next_entry, i, question_grouping))
            entry.bind('<BackSpace>', partial(self.clear_text, i))
            
            # Set initial value
            if contest_name == 'Group':
                entry.insert(0, str(self.school.group_scores[i]))
            elif contest_name == 'Cross':
                entry.insert(0, str(self.school.cross_scores[i]))
            elif contest_name == 'Relay':
                entry.insert(0, str(self.school.relay_scores[i]))

    def sum_entry_vals(self, start_index: int, end_index: int) -> int:
        """
        Calculate the sum of entry values between the given indices.
        
        Args:
            start_index: The starting index (inclusive)
            end_index: The ending index (exclusive)
            
        Returns:
            The sum of all valid integer entries in the range
        """
        total = 0
        for i in range(start_index, end_index):
            try:
                total += int(self.master.winfo_children()[1].winfo_children()[1]
                           .winfo_children()[0].winfo_children()[i].get())
            except ValueError:
                pass
        return total

    def validate_focus_left(self, i: int, event=None) -> None:
        """
        Validate the entry when focus leaves the field.
        
        Args:
            i: The index of the entry field
            event: The event that triggered this method
        """
        try:
            val = int(self.master.winfo_children()[1].winfo_children()[1]
                     .winfo_children()[0].winfo_children()[i].get())
            if val < 0:
                self.invalid_response(i)
            else:
                self.validate_ind(i)
        except ValueError:
            self.invalid_response(i)

    def next_entry(self, i: int, n: int, event=None) -> None:
        """
        Move focus to the next entry field.
        
        Args:
            i: The current entry index
            n: The total number of entries
            event: The event that triggered this method
        """
        if i < n - 1:
            self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i + 1].focus_set()
        else:
            self.validate()

    def clear_text(self, i: int, event=None) -> None:
        """
        Clear the text in the specified entry field.
        
        Args:
            i: The index of the entry field
            event: The event that triggered this method
        """
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].delete(0, tk.END)

    def invalid_response(self, i: int) -> None:
        """
        Handle invalid entry by resetting to zero.
        
        Args:
            i: The index of the entry field
        """
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].delete(0, tk.END)
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].insert(0, "0")

    def validate_ind(self, i: int, event=None) -> None:
        """
        Validate and save a single entry.
        
        Args:
            i: The index of the entry field
            event: The event that triggered this method
        """
        try:
            val = int(self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].get())
            if val < 0:
                self.invalid_response(i)
            else:
                if self.contest_name == 'Group':
                    self.school.group_scores[i] = val
                elif self.contest_name == 'Cross':
                    self.school.cross_scores[i] = val
                elif self.contest_name == 'Relay':
                    self.school.relay_scores[i] = val
        except ValueError:
            self.invalid_response(i)

    def validate(self) -> None:
        """Validate all entries and save the results."""
        for i in range(self.question_grouping):
            self.validate_ind(i)
        self.competition.write_to_file()
        self.competition.update_totals_school()
        self.reload_screen()

    def choose_school_name(self, event=None) -> None:
        """
        Open dialog to select a school by name.
        
        Args:
            event: The event that triggered this method
        """
        school_dialog = SchoolNameSelector(self.root, self.med_title_font, self.body_font, self.competition)
        school_key = school_dialog.sel_key
        if school_key is not None:
            self.school_key = school_key
            self.school = self.competition.find_key(school_key)
            self.reload_screen()

    def choose_school_key(self, event=None) -> None:
        """
        Open dialog to select a school by key.
        
        Args:
            event: The event that triggered this method
        """
        school_dialog = SchoolKeySelector(self.root, self.med_title_font, self.body_font, self.competition)
        school_key = school_dialog.sel_key
        if school_key is not None:
            self.school_key = school_key
            self.school = self.competition.find_key(school_key)
            self.reload_screen()

    def reload_screen(self) -> None:
        """Reload the screen with updated data."""
        self.clear_body()
        SingleSchoolContestBody(
            self.master,
            self.root,
            self.title_font,
            self.med_title_font,
            self.body_font,
            self.competition,
            self.school_key,
            self.contest_name,
            self.question_grouping
        )

    def next_school(self) -> None:
        """Open dialog to select the next school."""
        school_dialog = SchoolNameSelector(self.root, self.med_title_font, self.body_font, self.competition)
        school_key = school_dialog.sel_key
        if school_key is not None:
            self.school_key = school_key
            self.school = self.competition.find_key(school_key)
            self.reload_screen()

    def clear_body(self) -> None:
        """Remove all widgets from the main frame."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def goto_comp_main(self) -> None:
        """Return to the competition main menu."""
        self.clear_body()
        CompMainMenuBody(
            self.master,
            self.root,
            self.title_font,
            self.med_title_font,
            self.body_font,
            self.competition
        )

class SwissContestBody:
    """
    Interface for managing Swiss contest scores and pairings.
    
    This class provides a GUI for managing Swiss contest rounds, allowing users to:
    - View and edit scores for schools in a specific round and site
    - Generate new round pairings
    - Print round information
    - Navigate between sites
    - Return to the competition main menu
    
    Attributes:
        master (tk.Frame): The parent frame for this menu
        root (tk.Tk): The root window of the application
        title_font (tk.font.Font): Font for main titles
        med_title_font (tk.font.Font): Font for medium titles
        body_font (tk.font.Font): Font for body text
        competition (CompetitionSchoolList): The current competition data
        round_num (str): The current round number
        site (str): The current site identifier
    """
    
    def __init__(self,
                 master: tk.Frame,
                 root: tk.Tk,
                 title_font: tk.font.Font,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 competition: CompetitionSchoolList,
                 round_num: str,
                 site: str) -> None:
        """
        Initialize the Swiss contest interface.
        
        Args:
            master: The parent frame for this menu
            root: The root window of the application
            title_font: Font for main titles
            med_title_font: Font for medium titles
            body_font: Font for body text
            competition: The current competition data
            round_num: The current round number
            site: The current site identifier
        """
        self.title_font = title_font
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.master = master
        self.root = root
        self.competition = competition
        self.round_num = round_num
        self.site = site

        # Create main frame
        main_frame = tk.Frame(master, bd=1)
        main_frame.grid(row=0, column=0)

        # Add title
        title_text = f'Swiss Contest Round {round_num}\n'
        tk.Label(main_frame, text=title_text, bd=1, font=self.title_font).grid(row=0, column=0)

        # Create content frame
        content_frame = tk.Frame(master, bd=1)
        content_frame.grid(row=1, column=0)

        # Create round info frame
        round_info_frame = tk.Frame(content_frame, bd=1)
        round_info_frame.grid(row=0, column=0)

        # Create site info frame
        site_info_frame = tk.Frame(content_frame, bd=1)
        site_info_frame.grid(row=0, column=1)

        # Create navigation frame
        nav_frame = tk.Frame(content_frame, bd=1)
        nav_frame.grid(row=1, column=0)

        # Create score entry frame
        score_frame = tk.Frame(content_frame, bd=1)
        score_frame.grid(row=1, column=1)

        # Add round info
        tk.Label(round_info_frame, text="Round", bd=1, font=self.med_title_font).grid(row=0, column=0)
        self.round_label = tk.Label(round_info_frame, text=round_num, bd=1, font=self.body_font)
        self.round_label.grid(row=1, column=0)
        self.round_label.bind('<Button-1>', self.choose_round)

        # Add site info
        tk.Label(site_info_frame, text="Site", bd=1, font=self.med_title_font).grid(row=0, column=0)
        self.site_label = tk.Label(site_info_frame, text=site, bd=1, font=self.body_font)
        self.site_label.grid(row=1, column=0)
        self.site_label.bind('<Button-1>', self.choose_site)

        # Add navigation buttons
        tk.Button(nav_frame, text="Generate Round", width=10, font=self.body_font,
                 command=self.generate_round).grid(row=0, column=0)
        tk.Button(nav_frame, text="Print Round", width=10, font=self.body_font,
                 command=self.print_round).grid(row=0, column=1)
        tk.Button(nav_frame, text="Next Site", width=10, font=self.body_font,
                 command=self.next_site).grid(row=0, column=2)
        tk.Button(nav_frame, text="Back", width=10, font=self.body_font,
                 command=self.goto_comp_main).grid(row=0, column=3)

        # Add score entry fields
        score_entry_frame = tk.Frame(score_frame, bd=1)
        score_entry_frame.grid(row=0, column=0)

        schools = self.competition.find_swiss_site(round_num, site)
        for i, school in enumerate(schools):
            # Add school key label
            tk.Label(score_entry_frame, text=school.key, bd=1,
                    font=self.body_font).grid(row=0, column=i)
            
            # Add score entry field
            entry = tk.Entry(score_entry_frame, width=5, font=self.body_font)
            entry.grid(row=1, column=i)
            
            # Add event bindings
            entry.bind('<FocusOut>', partial(self.validate_focus_left, i))
            entry.bind('<Return>', partial(self.next_entry, i, len(schools)))
            entry.bind('<BackSpace>', partial(self.clear_text, i))
            
            # Set initial value
            entry.insert(0, str(school.swiss_scores[int(round_num) - 1]))

    def validate_focus_left(self, i: int, event=None) -> None:
        """
        Validate the entry when focus leaves the field.
        
        Args:
            i: The index of the entry field
            event: The event that triggered this method
        """
        try:
            val = int(self.master.winfo_children()[1].winfo_children()[1]
                     .winfo_children()[0].winfo_children()[i].get())
            if val < 0:
                self.invalid_response(i)
            else:
                self.validate_ind(i)
        except ValueError:
            self.invalid_response(i)

    def next_entry(self, i: int, n: int, event=None) -> None:
        """
        Move focus to the next entry field.
        
        Args:
            i: The current entry index
            n: The total number of entries
            event: The event that triggered this method
        """
        if i < n - 1:
            self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i + 1].focus_set()
        else:
            self.validate()

    def clear_text(self, i: int, event=None) -> None:
        """
        Clear the text in the specified entry field.
        
        Args:
            i: The index of the entry field
            event: The event that triggered this method
        """
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].delete(0, tk.END)

    def invalid_response(self, i: int) -> None:
        """
        Handle invalid entry by resetting to zero.
        
        Args:
            i: The index of the entry field
        """
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].delete(0, tk.END)
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].insert(0, "0")

    def validate_ind(self, i: int, event=None) -> None:
        """
        Validate and save a single entry.
        
        Args:
            i: The index of the entry field
            event: The event that triggered this method
        """
        try:
            val = int(self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].get())
            if val < 0:
                self.invalid_response(i)
            else:
                schools = self.competition.find_swiss_site(self.round_num, self.site)
                schools[i].swiss_scores[int(self.round_num) - 1] = val
        except ValueError:
            self.invalid_response(i)

    def validate(self) -> None:
        """Validate all entries and save the results."""
        schools = self.competition.find_swiss_site(self.round_num, self.site)
        for i in range(len(schools)):
            self.validate_ind(i)
        self.competition.write_to_file()
        self.competition.update_totals_school()
        self.reload_screen()

    def next_site(self) -> None:
        """Open dialog to select the next site."""
        site_dialog = SiteSelector(self.root, self.med_title_font, self.body_font, self.competition)
        site = site_dialog.sel_key
        if site is not None:
            self.site = site
            self.reload_screen()

    def choose_site(self, event=None) -> None:
        """
        Open dialog to select a site.
        
        Args:
            event: The event that triggered this method
        """
        site_dialog = SiteSelector(self.root, self.med_title_font, self.body_font, self.competition)
        site = site_dialog.sel_key
        if site is not None:
            self.site = site
            self.reload_screen()

    def reload_screen(self) -> None:
        """Reload the screen with updated data."""
        self.clear_body()
        SwissContestBody(
            self.master,
            self.root,
            self.title_font,
            self.med_title_font,
            self.body_font,
            self.competition,
            self.round_num,
            self.site
        )

    def choose_round(self, event=None) -> None:
        """
        Open dialog to select a round.
        
        Args:
            event: The event that triggered this method
        """
        round_dialog = SwissRoundNumberselector(self.root, self.med_title_font, self.body_font)
        round_num = round_dialog.sel_key
        if round_num is not None:
            self.round_num = round_num
            self.reload_screen()

    def generate_round(self) -> None:
        """Generate new pairings for the current round."""
        # Check if previous round scores are missing
        if int(self.round_num) > 1:
            missing_scores = False
            for school in self.competition.school_list:
                if school.swiss_scores[int(self.round_num) - 2] == 0:
                    missing_scores = True
                    break
            
            if missing_scores:
                if not messagebox.askyesno(
                    "Warning",
                    f"Scores for round {int(self.round_num)-1} have not been entered for all schools. "
                    "Generating new pairings without these scores may result in unfair matches. "
                    "Do you want to continue?"
                ):
                    return

        self.competition.generate_swiss_partners(self.round_num)
        self.competition.write_to_file()
        self.reload_screen()

    def print_round(self) -> None:
        """Print the current round's pairings."""
        self.competition.print_swiss_partners_csv(self.round_num)
        self.competition.print_swiss_partners(self.round_num)

    def clear_body(self) -> None:
        """Remove all widgets from the main frame."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def goto_comp_main(self) -> None:
        """Return to the competition main menu."""
        self.clear_body()
        CompMainMenuBody(
            self.master,
            self.root,
            self.title_font,
            self.med_title_font,
            self.body_font,
            self.competition
        )

class ReportMenu:
    """
    Interface for managing competition reports.
    
    This class provides a GUI for generating and managing competition reports,
    allowing users to:
    - Generate final competition reports
    - Update the master file with competition results
    - Return to the competition main menu
    
    Attributes:
        master (tk.Frame): The parent frame for this menu
        root (tk.Tk): The root window of the application
        title_font (tk.font.Font): Font for main titles
        med_title_font (tk.font.Font): Font for medium titles
        body_font (tk.font.Font): Font for body text
        competition (CompetitionSchoolList): The current competition data
    """
    
    def __init__(self,
                 master: tk.Frame,
                 root: tk.Tk,
                 title_font: tk.font.Font,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 competition: CompetitionSchoolList) -> None:
        """
        Initialize the report menu interface.
        
        Args:
            master: The parent frame for this menu
            root: The root window of the application
            title_font: Font for main titles
            med_title_font: Font for medium titles
            body_font: Font for body text
            competition: The current competition data
        """
        self.title_font = title_font
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.master = master
        self.root = root
        self.competition = competition

        # Create main frame
        main_frame = tk.Frame(master, bd=1)
        main_frame.grid(row=0, column=0)

        # Add title
        title_text = 'Report Menu\n'
        tk.Label(main_frame, text=title_text, bd=1, font=self.title_font).grid(row=0, column=0)

        # Create button frame
        button_frame = tk.Frame(master, bd=1)
        button_frame.grid(row=1, column=0)

        # Add menu buttons
        run_report_button = tk.Button(
            button_frame,
            text="1. Run Report",
            font=self.body_font,
            width=32,
            command=self.run_report
        )
        run_report_button.grid(row=0, column=0)

        update_master_button = tk.Button(
            button_frame,
            text="2. Update Master File",
            font=self.body_font,
            width=32,
            command=self.update_master_file
        )
        update_master_button.grid(row=1, column=0)

        back_button = tk.Button(
            button_frame,
            text="3. Back",
            font=self.body_font,
            width=32,
            command=self.goto_comp_main
        )
        back_button.grid(row=2, column=0)

    def goto_comp_main(self) -> None:
        """Return to the competition main menu."""
        self.clear_body()
        CompMainMenuBody(
            self.master,
            self.root,
            self.title_font,
            self.med_title_font,
            self.body_font,
            self.competition
        )

    def run_report(self) -> None:
        """Generate final competition reports."""
        self.competition.print_final()
        self.competition.print_overall()

    def update_master_file(self) -> None:
        """Update the master file with competition results."""
        self.competition.update_master_file()

    def clear_body(self) -> None:
        """Remove all widgets from the main frame."""
        for widget in self.master.winfo_children():
            widget.destroy()

def load_main_menu(root: tk.Tk,
                   large_title_font: tk.font.Font,
                   med_title_font: tk.font.Font,
                   body_font: tk.font.Font) -> MainMenuBody:
    """
    Create and return a new main menu instance.
    
    Args:
        root: The root window of the application
        large_title_font: Font for main titles
        med_title_font: Font for medium titles
        body_font: Font for body text
        
    Returns:
        A new MainMenuBody instance
    """
    return MainMenuBody(root, root, large_title_font, med_title_font, body_font) 