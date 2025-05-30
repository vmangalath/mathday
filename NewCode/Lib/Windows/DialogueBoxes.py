import tkinter as tk
from tkinter import messagebox

class SetupMenuRegisterSchool:
    def __init__(self, master, School, MedTitleFont, BodyFont, Registered):
        self.master = master
        self.School = School
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.Registered = Registered
        self.SelKey = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Register School")
        self.dialog.transient(master)
        self.dialog.grab_set()

        F1 = tk.Frame(self.dialog, bd=1)
        F1.grid(row=0, column=0)

        tk.Label(F1, text="School Name", bd=1, font=self.MedTitleFont).grid(row=0, column=0)
        tk.Label(F1, text=School.Name, bd=1, font=self.BodyFont).grid(row=1, column=0)

        tk.Label(F1, text="School Location", bd=1, font=self.MedTitleFont).grid(row=2, column=0)
        tk.Label(F1, text=School.Location, bd=1, font=self.BodyFont).grid(row=3, column=0)

        tk.Label(F1, text="School Key", bd=1, font=self.MedTitleFont).grid(row=4, column=0)
        self.KeyEntry = tk.Entry(F1, width=5, font=self.BodyFont)
        self.KeyEntry.grid(row=5, column=0)
        self.KeyEntry.bind('<Return>', self.Validate)

        tk.Button(F1, text="Register", width=10, font=self.BodyFont, command=self.Validate).grid(row=6, column=0)
        tk.Button(F1, text="Cancel", width=10, font=self.BodyFont, command=self.Cancel).grid(row=7, column=0)

        self.dialog.wait_window()

    def Validate(self, event=None):
        Key = self.KeyEntry.get()
        if not Key:
            messagebox.showerror("Error", "Please enter a key")
            return

        if not self.Registered.ValidKey(Key):
            messagebox.showerror("Error", "Key must be in the form of a letter followed by a number (e.g. A1, A2, B1, B2, etc.)")
            return

        if self.Registered.FindKey(Key) is not None:
            messagebox.showerror("Error", "Key already exists")
            return

        self.SelKey = Key
        self.dialog.destroy()

    def Cancel(self):
        self.dialog.destroy()

class SetupMenuNewSchool:
    def __init__(self, master, MedTitleFont, BodyFont, Registered, PrevList):
        self.master = master
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.Registered = Registered
        self.PrevList = PrevList
        self.SelKey = None
        self.NewSchoolName = None
        self.NewSchoolLocation = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("New School")
        self.dialog.transient(master)
        self.dialog.grab_set()

        F1 = tk.Frame(self.dialog, bd=1)
        F1.grid(row=0, column=0)

        tk.Label(F1, text="School Name", bd=1, font=self.MedTitleFont).grid(row=0, column=0)
        self.NameEntry = tk.Entry(F1, width=40, font=self.BodyFont)
        self.NameEntry.grid(row=1, column=0)
        self.NameEntry.bind('<Return>', lambda e: self.LocationEntry.focus_set())

        tk.Label(F1, text="School Location", bd=1, font=self.MedTitleFont).grid(row=2, column=0)
        self.LocationEntry = tk.Entry(F1, width=40, font=self.BodyFont)
        self.LocationEntry.grid(row=3, column=0)
        self.LocationEntry.bind('<Return>', lambda e: self.KeyEntry.focus_set())

        tk.Label(F1, text="School Key", bd=1, font=self.MedTitleFont).grid(row=4, column=0)
        self.KeyEntry = tk.Entry(F1, width=5, font=self.BodyFont)
        self.KeyEntry.grid(row=5, column=0)
        self.KeyEntry.bind('<Return>', self.Validate)

        tk.Button(F1, text="Register", width=10, font=self.BodyFont, command=self.Validate).grid(row=6, column=0)
        tk.Button(F1, text="Cancel", width=10, font=self.BodyFont, command=self.Cancel).grid(row=7, column=0)

        self.dialog.wait_window()

    def Validate(self, event=None):
        Name = self.NameEntry.get()
        Location = self.LocationEntry.get()
        Key = self.KeyEntry.get()

        if not Name or not Location or not Key:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if not self.Registered.ValidKey(Key):
            messagebox.showerror("Error", "Key must be in the form of a letter followed by a number (e.g. A1, A2, B1, B2, etc.)")
            return

        if self.Registered.FindKey(Key) is not None:
            messagebox.showerror("Error", "Key already exists")
            return

        if self.PrevList.FindName(Name) is not None:
            messagebox.showerror("Error", "School name already exists")
            return

        self.SelKey = Key
        self.NewSchoolName = Name
        self.NewSchoolLocation = Location
        self.dialog.destroy()

    def Cancel(self):
        self.dialog.destroy()

class SetupMenuModifyRegisterSchool:
    def __init__(self, master, School, Registered, MedTitleFont, BodyFont):
        self.master = master
        self.School = School
        self.Registered = Registered
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.SelKey = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Modify School")
        self.dialog.transient(master)
        self.dialog.grab_set()

        F1 = tk.Frame(self.dialog, bd=1)
        F1.grid(row=0, column=0)

        tk.Label(F1, text="School Name", bd=1, font=self.MedTitleFont).grid(row=0, column=0)
        tk.Label(F1, text=School.Name, bd=1, font=self.BodyFont).grid(row=1, column=0)

        tk.Label(F1, text="School Location", bd=1, font=self.MedTitleFont).grid(row=2, column=0)
        tk.Label(F1, text=School.Location, bd=1, font=self.BodyFont).grid(row=3, column=0)

        tk.Label(F1, text="School Key", bd=1, font=self.MedTitleFont).grid(row=4, column=0)
        self.KeyEntry = tk.Entry(F1, width=5, font=self.BodyFont)
        self.KeyEntry.grid(row=5, column=0)
        self.KeyEntry.insert(0, School.Key)
        self.KeyEntry.bind('<Return>', self.Validate)

        tk.Button(F1, text="Modify", width=10, font=self.BodyFont, command=self.Validate).grid(row=6, column=0)
        tk.Button(F1, text="Cancel", width=10, font=self.BodyFont, command=self.Cancel).grid(row=7, column=0)

        self.dialog.wait_window()

    def Validate(self, event=None):
        Key = self.KeyEntry.get()
        if not Key:
            messagebox.showerror("Error", "Please enter a key")
            return

        if not self.Registered.ValidKey(Key):
            messagebox.showerror("Error", "Key must be in the form of a letter followed by a number (e.g. A1, A2, B1, B2, etc.)")
            return

        if Key != self.School.Key and self.Registered.FindKey(Key) is not None:
            messagebox.showerror("Error", "Key already exists")
            return

        self.SelKey = Key
        self.dialog.destroy()

    def Cancel(self):
        self.dialog.destroy()

class SetupMenuCompetitionName:
    def __init__(self, master, MedTitleFont, BodyFont):
        self.master = master
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.CompetitionName = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Competition Name")
        self.dialog.transient(master)
        self.dialog.grab_set()

        F1 = tk.Frame(self.dialog, bd=1)
        F1.grid(row=0, column=0)

        tk.Label(F1, text="Competition Name", bd=1, font=self.MedTitleFont).grid(row=0, column=0)
        self.NameEntry = tk.Entry(F1, width=40, font=self.BodyFont)
        self.NameEntry.grid(row=1, column=0)
        self.NameEntry.bind('<Return>', self.Validate)

        tk.Button(F1, text="Create", width=10, font=self.BodyFont, command=self.Validate).grid(row=2, column=0)
        tk.Button(F1, text="Cancel", width=10, font=self.BodyFont, command=self.Cancel).grid(row=3, column=0)

        self.dialog.wait_window()

    def Validate(self, event=None):
        Name = self.NameEntry.get()
        if not Name:
            messagebox.showerror("Error", "Please enter a competition name")
            return

        self.CompetitionName = Name
        self.dialog.destroy()

    def Cancel(self):
        self.dialog.destroy()

class SwissRoundNumberselector:
    def __init__(self, master, MedTitleFont, BodyFont):
        self.master = master
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.SelKey = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Swiss Round Number")
        self.dialog.transient(master)
        self.dialog.grab_set()

        F1 = tk.Frame(self.dialog, bd=1)
        F1.grid(row=0, column=0)

        tk.Label(F1, text="Round Number", bd=1, font=self.MedTitleFont).grid(row=0, column=0)
        self.RoundEntry = tk.Entry(F1, width=5, font=self.BodyFont)
        self.RoundEntry.grid(row=1, column=0)
        self.RoundEntry.bind('<Return>', self.Validate)

        tk.Button(F1, text="Select", width=10, font=self.BodyFont, command=self.Validate).grid(row=2, column=0)
        tk.Button(F1, text="Cancel", width=10, font=self.BodyFont, command=self.Cancel).grid(row=3, column=0)

        self.dialog.wait_window()

    def Validate(self, event=None):
        try:
            RoundNum = int(self.RoundEntry.get())
            if RoundNum < 1:
                messagebox.showerror("Error", "Round number must be positive")
                return
            self.SelKey = str(RoundNum)
            self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid round number")

    def Cancel(self):
        self.dialog.destroy()

class SchoolKeySelector:
    def __init__(self, master, MedTitleFont, BodyFont, Competition):
        self.master = master
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.Competition = Competition
        self.SelKey = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Select School")
        self.dialog.transient(master)
        self.dialog.grab_set()

        F1 = tk.Frame(self.dialog, bd=1)
        F1.grid(row=0, column=0)

        tk.Label(F1, text="Select School", bd=1, font=self.MedTitleFont).grid(row=0, column=0)

        self.ListBox = tk.Listbox(F1, width=80, font=self.BodyFont)
        self.ListBox.grid(row=1, column=0)
        self.ListBox.bind('<Double-1>', self.Validate)

        scrollbar = tk.Scrollbar(F1, orient="vertical")
        scrollbar.config(command=self.ListBox.yview)
        scrollbar.grid(row=1, column=1)
        self.ListBox.config(yscrollcommand=scrollbar.set)

        HeaderString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key', 'School', 'Location', 'Z Score')
        self.ListBox.insert(1, HeaderString)

        for i, School in enumerate(self.Competition.SchoolList):
            NumString = "{:2.3f}".format(School.HistZScore)
            SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                School.Key, School.Name, School.Location, NumString
            )
            self.ListBox.insert(1 + i, SchoolString)

        tk.Button(F1, text="Select", width=10, font=self.BodyFont, command=self.Validate).grid(row=2, column=0)
        tk.Button(F1, text="Cancel", width=10, font=self.BodyFont, command=self.Cancel).grid(row=3, column=0)

        self.dialog.wait_window()

    def Validate(self, event=None):
        SelectedItem = self.ListBox.get('active')
        SelectedItemKey = SelectedItem.split()[0]

        if SelectedItemKey != 'Key':
            self.SelKey = SelectedItemKey
            self.dialog.destroy()

    def Cancel(self):
        self.dialog.destroy()

class SiteSelector:
    def __init__(self, master, MedTitleFont, BodyFont, Competition):
        self.master = master
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.Competition = Competition
        self.SelKey = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Select Site")
        self.dialog.transient(master)
        self.dialog.grab_set()

        F1 = tk.Frame(self.dialog, bd=1)
        F1.grid(row=0, column=0)

        tk.Label(F1, text="Select Site", bd=1, font=self.MedTitleFont).grid(row=0, column=0)

        self.ListBox = tk.Listbox(F1, width=40, font=self.BodyFont)
        self.ListBox.grid(row=1, column=0)
        self.ListBox.bind('<Double-1>', self.Validate)

        scrollbar = tk.Scrollbar(F1, orient="vertical")
        scrollbar.config(command=self.ListBox.yview)
        scrollbar.grid(row=1, column=1)
        self.ListBox.config(yscrollcommand=scrollbar.set)

        Sites = self.Competition.GetSites()
        for i, Site in enumerate(Sites):
            self.ListBox.insert(i, Site)

        tk.Button(F1, text="Select", width=10, font=self.BodyFont, command=self.Validate).grid(row=2, column=0)
        tk.Button(F1, text="Cancel", width=10, font=self.BodyFont, command=self.Cancel).grid(row=3, column=0)

        self.dialog.wait_window()

    def Validate(self, event=None):
        SelectedItem = self.ListBox.get('active')
        if SelectedItem:
            self.SelKey = SelectedItem
            self.dialog.destroy()

    def Cancel(self):
        self.dialog.destroy()

class SchoolNameSelector:
    def __init__(self, master, MedTitleFont, BodyFont, Competition):
        self.master = master
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.Competition = Competition
        self.SelKey = None

        self.dialog = tk.Toplevel(master)
        self.dialog.title("Select School")
        self.dialog.transient(master)
        self.dialog.grab_set()

        F1 = tk.Frame(self.dialog, bd=1)
        F1.grid(row=0, column=0)

        tk.Label(F1, text="Select School", bd=1, font=self.MedTitleFont).grid(row=0, column=0)

        self.ListBox = tk.Listbox(F1, width=80, font=self.BodyFont)
        self.ListBox.grid(row=1, column=0)
        self.ListBox.bind('<Double-1>', self.Validate)

        scrollbar = tk.Scrollbar(F1, orient="vertical")
        scrollbar.config(command=self.ListBox.yview)
        scrollbar.grid(row=1, column=1)
        self.ListBox.config(yscrollcommand=scrollbar.set)

        HeaderString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key', 'School', 'Location', 'Z Score')
        self.ListBox.insert(1, HeaderString)

        for i, School in enumerate(self.Competition.SchoolList):
            NumString = "{:2.3f}".format(School.HistZScore)
            SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                School.Key, School.Name, School.Location, NumString
            )
            self.ListBox.insert(1 + i, SchoolString)

        tk.Button(F1, text="Select", width=10, font=self.BodyFont, command=self.Validate).grid(row=2, column=0)
        tk.Button(F1, text="Cancel", width=10, font=self.BodyFont, command=self.Cancel).grid(row=3, column=0)

        self.dialog.wait_window()

    def Validate(self, event=None):
        SelectedItem = self.ListBox.get('active')
        SelectedItemKey = SelectedItem.split()[0]

        if SelectedItemKey != 'Key':
            self.SelKey = SelectedItemKey
            self.dialog.destroy()

    def Cancel(self):
        self.dialog.destroy() 