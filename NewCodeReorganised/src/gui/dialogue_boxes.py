import tkinter as tk
from tkinter import messagebox
from typing import Optional, List
from core.structures import RegisteredSchool, PreviousSchool, CompetitionSchoolList

class SetupMenuRegisterSchool:
    """
    Dialog for registering a school with a key.

    Allows the user to input a unique key for a school being registered
    for the current competition.

    Attributes:
        master (tk.Tk): The root window of the application.
        school (PreviousSchool): The school being registered.
        med_title_font (tk.font.Font): Font for medium titles.
        body_font (tk.font.Font): Font for body text.
        registered (RegisteredSchoolList): List of already registered schools.
        sel_key (Optional[str]): The selected key after validation, or None.
        dialog (tk.Toplevel): The dialog window.
        key_entry (tk.Entry): Entry widget for the school key.
    """
    def __init__(self,
                 master: tk.Tk,
                 school: PreviousSchool,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 registered: 'RegisterSchoolList') -> None:
        """
        Initialize the SetupMenuRegisterSchool dialog.

        Args:
            master: The root window of the application.
            school: The school being registered.
            med_title_font: Font for medium titles.
            body_font: Font for body text.
            registered: List of already registered schools.
        """
        self.master = master
        self.school = school
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.registered = registered
        self.sel_key: Optional[str] = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Register School")
        self.dialog.transient(master)
        self.dialog.grab_set()

        main_frame = tk.Frame(self.dialog, bd=1)
        main_frame.grid(row=0, column=0)

        tk.Label(main_frame, text="School Name", bd=1, font=self.med_title_font).grid(row=0, column=0)
        tk.Label(main_frame, text=self.school.name, bd=1, font=self.body_font).grid(row=1, column=0)

        tk.Label(main_frame, text="School Location", bd=1, font=self.med_title_font).grid(row=2, column=0)
        tk.Label(main_frame, text=self.school.location, bd=1, font=self.body_font).grid(row=3, column=0)

        tk.Label(main_frame, text="School Key", bd=1, font=self.med_title_font).grid(row=4, column=0)
        self.key_entry = tk.Entry(main_frame, width=5, font=self.body_font)
        self.key_entry.grid(row=5, column=0)
        self.key_entry.bind('<Return>', self.validate_key)

        tk.Button(main_frame, text="Register", width=10, font=self.body_font, command=self.validate_key).grid(row=6, column=0)
        tk.Button(main_frame, text="Cancel", width=10, font=self.body_font, command=self.cancel).grid(row=7, column=0)

        self.dialog.wait_window()

    def validate_key(self, event: Optional[tk.Event] = None) -> None:
        """
        Validate the entered school key.

        Checks if the key is valid and unique before setting sel_key.

        Args:
            event: Optional event that triggered this method.
        """
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Error", "Please enter a key")
            return

        if not self.registered.valid_key(key):
            messagebox.showerror("Error", "Key must be in the form of a letter followed by a number (e.g. A1, A2, B1, B2, etc.)")
            return

        if self.registered.find_key(key) is not None:
            messagebox.showerror("Error", "Key already exists")
            return

        self.sel_key = key
        self.dialog.destroy()

    def cancel(self) -> None:
        """
        Close the dialog without selecting a key.
        """
        self.dialog.destroy()

class SetupMenuNewSchool:
    """
    Dialog for adding and registering a new school.

    Allows the user to enter details for a new school and assign a unique key.

    Attributes:
        master (tk.Tk): The root window of the application.
        med_title_font (tk.font.Font): Font for medium titles.
        body_font (tk.font.Font): Font for body text.
        registered (RegisteredSchoolList): List of already registered schools.
        prev_list (PreviousSchoolList): List of schools from previous competitions.
        sel_key (Optional[str]): The selected key after validation, or None.
        new_school_name (Optional[str]): The entered school name after validation, or None.
        new_school_location (Optional[str]): The entered school location after validation, or None.
        dialog (tk.Toplevel): The dialog window.
        name_entry (tk.Entry): Entry widget for the school name.
        location_entry (tk.Entry): Entry widget for the school location.
        key_entry (tk.Entry): Entry widget for the school key.
    """
    def __init__(self,
                 master: tk.Tk,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 registered: 'RegisterSchoolList',
                 prev_list: 'PreviousSchoolList') -> None:
        """
        Initialize the SetupMenuNewSchool dialog.

        Args:
            master: The root window of the application.
            med_title_font: Font for medium titles.
            body_font: Font for body text.
            registered: List of already registered schools.
            prev_list: List of schools from previous competitions.
        """
        self.master = master
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.registered = registered
        self.prev_list = prev_list
        self.sel_key: Optional[str] = None
        self.new_school_name: Optional[str] = None
        self.new_school_location: Optional[str] = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("New School")
        self.dialog.transient(master)
        self.dialog.grab_set()

        main_frame = tk.Frame(self.dialog, bd=1)
        main_frame.grid(row=0, column=0)

        tk.Label(main_frame, text="School Name", bd=1, font=self.med_title_font).grid(row=0, column=0)
        self.name_entry = tk.Entry(main_frame, width=40, font=self.body_font)
        self.name_entry.grid(row=1, column=0)
        self.name_entry.bind('<Return>', lambda e: self.location_entry.focus_set())

        tk.Label(main_frame, text="School Location", bd=1, font=self.med_title_font).grid(row=2, column=0)
        self.location_entry = tk.Entry(main_frame, width=40, font=self.body_font)
        self.location_entry.grid(row=3, column=0)
        self.location_entry.bind('<Return>', lambda e: self.key_entry.focus_set())

        tk.Label(main_frame, text="School Key", bd=1, font=self.med_title_font).grid(row=4, column=0)
        self.key_entry = tk.Entry(main_frame, width=5, font=self.body_font)
        self.key_entry.grid(row=5, column=0)
        self.key_entry.bind('<Return>', self.validate_inputs)

        tk.Button(main_frame, text="Register", width=10, font=self.body_font, command=self.validate_inputs).grid(row=6, column=0)
        tk.Button(main_frame, text="Cancel", width=10, font=self.body_font, command=self.cancel).grid(row=7, column=0)

        self.dialog.wait_window()

    def validate_inputs(self, event: Optional[tk.Event] = None) -> None:
        """
        Validate the entered school details and key.

        Checks if all fields are filled, key is valid and unique, and name is unique.

        Args:
            event: Optional event that triggered this method.
        """
        name = self.name_entry.get()
        location = self.location_entry.get()
        key = self.key_entry.get()

        if not name or not location or not key:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if not self.registered.valid_key(key):
            messagebox.showerror("Error", "Key must be in the form of a letter followed by a number (e.g. A1, A2, B1, B2, etc.)")
            return

        if self.registered.find_key(key) is not None:
            messagebox.showerror("Error", "Key already exists")
            return

        if self.prev_list.find_name(name) is not None:
            messagebox.showerror("Error", "School name already exists")
            return

        self.sel_key = key
        self.new_school_name = name
        self.new_school_location = location
        self.dialog.destroy()

    def cancel(self) -> None:
        """
        Close the dialog without saving.
        """
        self.dialog.destroy()

class SetupMenuModifyRegisterSchool:
    """
    Dialog for modifying a registered school's key.

    Allows the user to update the unique key assigned to a registered school.

    Attributes:
        master (tk.Tk): The root window of the application.
        school (RegisteredSchool): The registered school being modified.
        registered (RegisteredSchoolList): List of all registered schools.
        med_title_font (tk.font.Font): Font for medium titles.
        body_font (tk.font.Font): Font for body text.
        sel_key (Optional[str]): The selected key after validation, or None.
        dialog (tk.Toplevel): The dialog window.
        key_entry (tk.Entry): Entry widget for the school key.
    """
    def __init__(self,
                 master: tk.Tk,
                 school: RegisteredSchool,
                 registered: 'RegisterSchoolList',
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font) -> None:
        """
        Initialize the SetupMenuModifyRegisterSchool dialog.

        Args:
            master: The root window of the application.
            school: The registered school being modified.
            registered: List of all registered schools.
            med_title_font: Font for medium titles.
            body_font: Font for body text.
        """
        self.master = master
        self.school = school
        self.registered = registered
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.sel_key: Optional[str] = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Modify School")
        self.dialog.transient(master)
        self.dialog.grab_set()

        main_frame = tk.Frame(self.dialog, bd=1)
        main_frame.grid(row=0, column=0)

        tk.Label(main_frame, text="School Name", bd=1, font=self.med_title_font).grid(row=0, column=0)
        tk.Label(main_frame, text=self.school.name, bd=1, font=self.body_font).grid(row=1, column=0)

        tk.Label(main_frame, text="School Location", bd=1, font=self.med_title_font).grid(row=2, column=0)
        tk.Label(main_frame, text=self.school.location, bd=1, font=self.body_font).grid(row=3, column=0)

        tk.Label(main_frame, text="School Key", bd=1, font=self.med_title_font).grid(row=4, column=0)
        self.key_entry = tk.Entry(main_frame, width=5, font=self.body_font)
        self.key_entry.grid(row=5, column=0)
        self.key_entry.insert(0, self.school.key)
        self.key_entry.bind('<Return>', self.validate_key)

        tk.Button(main_frame, text="Modify", width=10, font=self.body_font, command=self.validate_key).grid(row=6, column=0)
        tk.Button(main_frame, text="Cancel", width=10, font=self.body_font, command=self.cancel).grid(row=7, column=0)

        self.dialog.wait_window()

    def validate_key(self, event: Optional[tk.Event] = None) -> None:
        """
        Validate the entered school key.

        Checks if the key is valid and unique before setting sel_key.

        Args:
            event: Optional event that triggered this method.
        """
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Error", "Please enter a key")
            return

        if not self.registered.valid_key(key):
            messagebox.showerror("Error", "Key must be in the form of a letter followed by a number (e.g. A1, A2, B1, B2, etc.)")
            return

        if key != self.school.key and self.registered.find_key(key) is not None:
            messagebox.showerror("Error", "Key already exists")
            return

        self.sel_key = key
        self.dialog.destroy()

    def cancel(self) -> None:
        """
        Close the dialog without saving.
        """
        self.dialog.destroy()

class SetupMenuCompetitionName:
    """
    Dialog for entering the competition name.

    Allows the user to specify a name for the new competition file.

    Attributes:
        master (tk.Tk): The root window of the application.
        med_title_font (tk.font.Font): Font for medium titles.
        body_font (tk.font.Font): Font for body text.
        competition_name (Optional[str]): The entered competition name, or None.
        dialog (tk.Toplevel): The dialog window.
        name_entry (tk.Entry): Entry widget for the competition name.
    """
    def __init__(self,
                 master: tk.Tk,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 registered_schools: 'RegisterSchoolList',
                 data_dir: str) -> None:
        """
        Initialize the SetupMenuCompetitionName dialog.

        Args:
            master: The root window of the application.
            med_title_font: Font for medium titles.
            body_font: Font for body text.
            registered_schools: List of registered schools.
            data_dir: Directory for storing competition data.
        """
        self.master = master
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.registered_schools = registered_schools
        self.data_dir = data_dir
        self.competition_name: Optional[str] = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Competition Name")
        self.dialog.transient(master)
        self.dialog.grab_set()

        main_frame = tk.Frame(self.dialog, bd=1)
        main_frame.grid(row=0, column=0)

        tk.Label(main_frame, text="Competition Name", bd=1, font=self.med_title_font).grid(row=0, column=0)
        self.name_entry = tk.Entry(main_frame, width=40, font=self.body_font)
        self.name_entry.grid(row=1, column=0)
        self.name_entry.bind('<Return>', self.validate_name)

        tk.Button(main_frame, text="Create", width=10, font=self.body_font, command=self.validate_name).grid(row=2, column=0)
        tk.Button(main_frame, text="Cancel", width=10, font=self.body_font, command=self.cancel).grid(row=3, column=0)

        self.dialog.wait_window()

    def validate_name(self, event: Optional[tk.Event] = None) -> None:
        """
        Validate the entered competition name.

        Checks if a name is entered and saves the competition file.

        Args:
            event: Optional event that triggered this method.
        """
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter a competition name")
            return

        try:
            # Create an empty CompetitionSchoolList
            competition = CompetitionSchoolList()
            # Populate it with CompetitionSchool instances from registered schools
            competition.compete_registered(self.registered_schools)
            
            competition.file = f"{self.data_dir}{name}.csv"
            competition.write_to_file()
            self.competition_name = name
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save competition file: {e}")

    def cancel(self) -> None:
        """
        Close the dialog without creating a competition file.
        """
        self.dialog.destroy()

class SwissRoundNumberselector:
    """
    Dialog for selecting a Swiss round number.

    Allows the user to input the number for the desired Swiss round.

    Attributes:
        master (tk.Tk): The root window of the application.
        med_title_font (tk.font.Font): Font for medium titles.
        body_font (tk.font.Font): Font for body text.
        sel_key (Optional[str]): The selected round number as a string, or None.
        dialog (tk.Toplevel): The dialog window.
        round_entry (tk.Entry): Entry widget for the round number.
    """
    def __init__(self,
                 master: tk.Tk,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font) -> None:
        """
        Initialize the SwissRoundNumberselector dialog.

        Args:
            master: The root window of the application.
            med_title_font: Font for medium titles.
            body_font: Font for body text.
        """
        self.master = master
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.sel_key: Optional[str] = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Swiss Round Number")
        self.dialog.transient(master)
        self.dialog.grab_set()

        main_frame = tk.Frame(self.dialog, bd=1)
        main_frame.grid(row=0, column=0)

        tk.Label(main_frame, text="Round Number", bd=1, font=self.med_title_font).grid(row=0, column=0)
        self.round_entry = tk.Entry(main_frame, width=5, font=self.body_font)
        self.round_entry.grid(row=1, column=0)
        self.round_entry.bind('<Return>', self.validate)

        tk.Button(main_frame, text="Select", width=10, font=self.body_font, command=self.validate).grid(row=2, column=0)
        tk.Button(main_frame, text="Cancel", width=10, font=self.body_font, command=self.cancel).grid(row=3, column=0)

        self.dialog.wait_window()

    def validate(self, event: Optional[tk.Event] = None) -> None:
        """
        Validate the entered round number.

        Checks if the round number is valid and sets sel_key.

        Args:
            event: Optional event that triggered this method.
        """
        try:
            round_num = int(self.round_entry.get())
            if round_num < 1:
                messagebox.showerror("Error", "Round number must be positive")
                return
            self.sel_key = str(round_num)
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid round number")

    def cancel(self) -> None:
        """
        Close the dialog without selecting a round number.
        """
        self.dialog.destroy()

class SchoolKeySelector:
    """
    Dialog for selecting a school by key.

    Allows the user to choose an existing school by entering its unique key.

    Attributes:
        master (tk.Tk): The root window of the application.
        med_title_font (tk.font.Font): Font for medium titles.
        body_font (tk.font.Font): Font for body text.
        competition (CompetitionSchoolList): The current competition data.
        sel_key (Optional[str]): The selected school key after validation, or None.
        dialog (tk.Toplevel): The dialog window.
        key_entry (tk.Entry): Entry widget for the school key.
    """
    def __init__(self,
                 master: tk.Tk,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 competition: 'CompetitionSchoolList') -> None:
        """
        Initialize the SchoolKeySelector dialog.

        Args:
            master: The root window of the application.
            med_title_font: Font for medium titles.
            body_font: Font for body text.
            competition: The current competition data.
        """
        self.master = master
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.competition = competition
        self.sel_key: Optional[str] = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Select School by Key")
        self.dialog.transient(master)
        self.dialog.grab_set()

        main_frame = tk.Frame(self.dialog, bd=1)
        main_frame.grid(row=0, column=0)

        tk.Label(main_frame, text="Enter School Key", bd=1, font=self.med_title_font).grid(row=0, column=0)
        self.key_entry = tk.Entry(main_frame, width=5, font=self.body_font)
        self.key_entry.grid(row=1, column=0)
        self.key_entry.bind('<Return>', self.validate_key)

        tk.Button(main_frame, text="Select", width=10, font=self.body_font, command=self.validate_key).grid(row=2, column=0)
        tk.Button(main_frame, text="Cancel", width=10, font=self.body_font, command=self.cancel).grid(row=3, column=0)

        self.dialog.wait_window()

    def validate_key(self, event: Optional[tk.Event] = None) -> None:
        """
        Validate the entered school key.

        Checks if the key exists in the competition and sets sel_key.

        Args:
            event: Optional event that triggered this method.
        """
        key = self.key_entry.get()
        if not key:
            messagebox.showerror("Error", "Please enter a key")
            return

        if self.competition.find_key(key) is None:
            messagebox.showerror("Error", "Key not found")
            return

        self.sel_key = key
        self.dialog.destroy()

    def cancel(self) -> None:
        """
        Close the dialog without selecting a key.
        """
        self.dialog.destroy()

class SiteSelector:
    """
    Dialog for selecting a Swiss site.

    Allows the user to choose an existing site for a Swiss round.

    Attributes:
        master (tk.Tk): The root window of the application.
        med_title_font (tk.font.Font): Font for medium titles.
        body_font (tk.font.Font): Font for body text.
        competition (CompetitionSchoolList): The current competition data.
        sel_key (Optional[str]): The selected site after validation, or None.
        dialog (tk.Toplevel): The dialog window.
        site_entry (tk.Entry): Entry widget for the site.
    """
    def __init__(self,
                 master: tk.Tk,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 competition: 'CompetitionSchoolList') -> None:
        """
        Initialize the SiteSelector dialog.

        Args:
            master: The root window of the application.
            med_title_font: Font for medium titles.
            body_font: Font for body text.
            competition: The current competition data.
        """
        self.master = master
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.competition = competition
        self.sel_key: Optional[str] = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Select Site")
        self.dialog.transient(master)
        self.dialog.grab_set()

        main_frame = tk.Frame(self.dialog, bd=1)
        main_frame.grid(row=0, column=0)

        tk.Label(main_frame, text="Enter Site", bd=1, font=self.med_title_font).grid(row=0, column=0)
        self.site_entry = tk.Entry(main_frame, width=5, font=self.body_font)
        self.site_entry.grid(row=1, column=0)
        self.site_entry.bind('<Return>', self.validate_site)

        tk.Button(main_frame, text="Select", width=10, font=self.body_font, command=self.validate_site).grid(row=2, column=0)
        tk.Button(main_frame, text="Cancel", width=10, font=self.body_font, command=self.cancel).grid(row=3, column=0)

        self.dialog.wait_window()

    def validate_site(self, event: Optional[tk.Event] = None) -> None:
        """
        Validate the entered site.

        Checks if the site is valid and sets sel_key.

        Args:
            event: Optional event that triggered this method.
        """
        site = self.site_entry.get()
        if not site:
            messagebox.showerror("Error", "Please enter a site")
            return

        # Assuming site validation logic here if any specific format is required
        # For now, just check if it's not empty
        # if not is_valid_site(site): # Example validation
        #     messagebox.showerror("Error", "Invalid site format")
        #     return

        self.sel_key = site
        self.dialog.destroy()

    def cancel(self) -> None:
        """
        Close the dialog without selecting a site.
        """
        self.dialog.destroy()

class SchoolNameSelector:
    """
    Dialog for selecting a school by name.

    Allows the user to choose an existing school from a list by name.

    Attributes:
        master (tk.Tk): The root window of the application.
        med_title_font (tk.font.Font): Font for medium titles.
        body_font (tk.font.Font): Font for body text.
        competition (CompetitionSchoolList): The current competition data.
        sel_key (Optional[str]): The key of the selected school after validation, or None.
        dialog (tk.Toplevel): The dialog window.
        name_listbox (tk.Listbox): Listbox displaying school names.
        scrollbar (tk.Scrollbar): Scrollbar for the listbox.
    """
    def __init__(self,
                 master: tk.Tk,
                 med_title_font: tk.font.Font,
                 body_font: tk.font.Font,
                 competition: 'CompetitionSchoolList') -> None:
        """
        Initialize the SchoolNameSelector dialog.

        Args:
            master: The root window of the application.
            med_title_font: Font for medium titles.
            body_font: Font for body text.
            competition: The current competition data.
        """
        self.master = master
        self.med_title_font = med_title_font
        self.body_font = body_font
        self.competition = competition
        self.sel_key: Optional[str] = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Select School by Name")
        self.dialog.transient(master)
        self.dialog.grab_set()

        main_frame = tk.Frame(self.dialog, bd=1)
        main_frame.grid(row=0, column=0)

        tk.Label(main_frame, text="Select School", bd=1, font=self.med_title_font).grid(row=0, column=0)

        listbox_frame = tk.Frame(main_frame)
        listbox_frame.grid(row=1, column=0)

        self.name_listbox = tk.Listbox(listbox_frame, width=40, font=self.body_font)
        self.name_listbox.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
        self.scrollbar.config(command=self.name_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.name_listbox.config(yscrollcommand=self.scrollbar.set)

        # Populate listbox with school names
        for school in self.competition.school_list:
            self.name_listbox.insert(tk.END, school.name)

        self.name_listbox.bind('<Double-1>', self.validate_selection)

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=2, column=0)

        tk.Button(button_frame, text="Select", width=10, font=self.body_font, command=self.validate_selection).grid(row=0, column=0)
        tk.Button(button_frame, text="Cancel", width=10, font=self.body_font, command=self.cancel).grid(row=0, column=1)

        self.dialog.wait_window()

    def validate_selection(self, event: Optional[tk.Event] = None) -> None:
        """
        Validate the selected school name.

        Gets the key of the selected school and sets sel_key.

        Args:
            event: Optional event that triggered this method.
        """
        selected_index = self.name_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a school")
            return

        selected_name = self.name_listbox.get(selected_index[0])
        school = self.competition.find_name(selected_name)

        if school:
            self.sel_key = school.key
            self.dialog.destroy()
        else:
            messagebox.showerror("Error", "Selected school not found in competition data.") # Should not happen if list is populated correctly

    def cancel(self) -> None:
        """
        Close the dialog without selecting a school.
        """
        self.dialog.destroy() 