import tkinter as tk
from tkinter import filedialog, messagebox
from functools import partial
from .DialogueBoxes import (
    SetupMenuRegisterSchool, SetupMenuNewSchool, SetupMenuModifyRegisterSchool,
    SetupMenuCompetitionName, SwissRoundNumberselector, SchoolKeySelector,
    SiteSelector, SchoolNameSelector
)
from ..Structures.Structs import (
    PreviousSchoolList, RegisterSchoolList, RegisteredSchool,
    PreviousSchool, CompetitionSchoolList
)

class MainMenuBody:
    def __init__(self, master, root, TitleFont, MedTitleFont, BodyFont, DataDir='./Data/'):
        self.TitleFont = TitleFont
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.master = master
        self.root = root
        self.DataDir = DataDir

        F1 = tk.Frame(self.master, height=10, width=10, bd=1)
        F1.grid(row=0, column=0)

        Str1 = 'Math Day Score Keeper Program'
        tk.Label(F1, text=Str1, bd=4, font=self.TitleFont).grid(row=0, column=0)

        a1 = tk.Button(F1, text="1. Set-Up Competition", font=self.BodyFont, width=32, command=self.GotoSetupMenu)
        a1.grid(row=1, column=0)

        b1 = tk.Button(F1, text="2. Run Competition", font=self.BodyFont, width=32, command=self.GotoCompMain)
        b1.grid(row=2, column=0)

        c1 = tk.Button(F1, text="3. Exit", font=self.BodyFont, width=32, command=self.Exit)
        c1.grid(row=3, column=0)

    def Exit(self):
        self.root.destroy()

    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def GotoSetupMenu(self):
        self.ClearBody()
        SetupMenuBody(self.master, self.root, self.TitleFont, self.MedTitleFont, self.BodyFont, self.DataDir)

    def GotoCompMain(self):
        FileName = filedialog.askopenfilename(
            initialdir=self.DataDir,
            title="Select Competition File",
            filetypes=(("Comma Separated Files", "*.csv"), ('All Files', '*'))
        )

        if FileName:
            self.ClearBody()
            MasterDir = self.DataDir + "Master/"
            Competition = CompetitionSchoolList(
                SchoolList=[],
                File=FileName,
                MasterDir=MasterDir,
                DataDir=self.DataDir
            )
            Competition.ReadFromFile()
            CompMainMenuBody(self.master, self.root, self.TitleFont, self.MedTitleFont, self.BodyFont, Competition)

class SetupMenuBody:
    def __init__(self, master, root, TitleFont, MedTitleFont, BodyFont, DataDir):
        self.TitleFont = TitleFont
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.master = master
        self.root = root
        self.DataDir = DataDir
        self.MasterDir = self.DataDir + "Master/"
        self.ContestNameInitScores = []

        self.PrevList = PreviousSchoolList(MasterFile=self.MasterDir + "Schools.csv")
        self.PrevList.ReadFromFile()

        self.Registered = RegisterSchoolList(SchoolList=[])

        F1 = tk.Frame(master, bd=1)
        F1.grid(row=0, column=0)
        Str1 = 'Competition Set-Up\n'
        tk.Label(F1, text=Str1, bd=1, font=self.TitleFont).grid(row=0, column=0)

        F2 = tk.Frame(master, bd=1)
        F2.grid(row=1, column=0)

        F3 = tk.Frame(master, bd=1)
        F3.grid(row=2, column=0)

        F4 = tk.Frame(F2, bd=1)
        F4.grid(row=0, column=0)

        F5 = tk.Frame(F2, bd=1)
        F5.grid(row=0, column=1)

        F6 = tk.Frame(F2, bd=1)
        F6.grid(row=1, column=0)

        F7 = tk.Frame(F2, bd=1)
        F7.grid(row=1, column=1)

        tk.Button(F6, text="New", width=10, font=self.BodyFont, command=self.AddSchoolToList).grid(row=0, column=0)
        tk.Button(F6, text="Register", width=10, font=self.BodyFont, command=self.RegisterSchool).grid(row=0, column=1)

        tk.Button(F7, text="Modify", width=10, font=self.BodyFont, command=self.Modify).grid(row=0, column=0)
        tk.Button(F7, text="Remove", width=10, font=self.BodyFont, command=self.Remove).grid(row=0, column=1)
        tk.Button(F7, text="Order", width=10, font=self.BodyFont, command=self.Order).grid(row=0, column=2)
        tk.Button(F7, text="Done", width=10, font=self.BodyFont, command=self.Done).grid(row=0, column=3)
        tk.Button(F7, text="Back", width=10, font=self.BodyFont, command=self.GotoMainMenu).grid(row=1, column=3)

        tk.Label(F4, text="Previous School List", bd=1, font=self.MedTitleFont).grid(row=0, column=0)

        self.ListBox1 = tk.Listbox(F4, width=40, font=self.BodyFont)
        self.ListBox1.grid(row=1, column=0)
        self.ListBox1.bind('<Double-1>', self.RegisterSchool)

        scrollbar = tk.Scrollbar(F4, orient="vertical")
        scrollbar.config(command=self.ListBox1.yview)
        scrollbar.grid(row=1, column=1)
        self.ListBox1.config(yscrollcommand=scrollbar.set)

        for i, School in enumerate(self.PrevList.SchoolList):
            self.ListBox1.insert(i, School.Name)

        tk.Label(F5, text="Registered School List", bd=1, font=self.MedTitleFont).grid(row=0, column=0)
        self.ListBox2 = tk.Listbox(F5, width=80, font=self.BodyFont)
        self.ListBox2.grid(row=1, column=0)

        scrollbar = tk.Scrollbar(F5, orient="vertical")
        scrollbar.config(command=self.ListBox2.yview)
        scrollbar.grid(row=1, column=1)
        self.ListBox2.config(yscrollcommand=scrollbar.set)
        self.ListBox2.bind('<Double-1>', self.Modify)

        HeaderString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key', 'School', 'Location', 'Z Score')
        self.ListBox2.insert(1, HeaderString)

    def AddSchoolToList(self):
        AddSchoolDialog = SetupMenuNewSchool(self.root, self.MedTitleFont, self.BodyFont, self.Registered, self.PrevList)

        SelKey = AddSchoolDialog.SelKey
        SchoolName = AddSchoolDialog.NewSchoolName
        SchoolLocation = AddSchoolDialog.NewSchoolLocation

        if SelKey is not None:
            SchoolHist = PreviousSchool(SchoolName, SchoolLocation, 0.0)
            SchoolReg = SchoolHist.Register(SelKey)

            self.PrevList.AddToList(SchoolHist)
            self.PrevList.SortList()
            self.PrevList.WriteToFile()

            self.Registered.AddToList(SchoolReg)

            self.ListBox1.delete(0, tk.END)
            for i, School in enumerate(self.PrevList.SchoolList):
                self.ListBox1.insert(i, School.Name)

            NumString = "{:2.3f}".format(0)
            SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                SchoolReg.Key, SchoolReg.Name, SchoolReg.Location, NumString
            )
            self.ListBox2.insert(1 + len(self.Registered.SchoolList), SchoolString)

    def RegisterSchool(self, event=None):
        item = self.ListBox1.get('active')  # get clicked item
        School = self.PrevList.FindName(item)

        SchoolDialog = SetupMenuRegisterSchool(self.root, School, self.MedTitleFont, self.BodyFont, self.Registered)
        SelKey = SchoolDialog.SelKey

        if SelKey is not None:
            RegSchool = School.Register(SelKey)
            NumString = "{:2.3f}".format(RegSchool.HistZScore)
            SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                RegSchool.Key, RegSchool.Name, RegSchool.Location, NumString
            )
            self.ListBox2.insert(2 + len(self.Registered.SchoolList), SchoolString)
            self.Registered.AddToList(RegSchool)

    def Modify(self, event=None):
        SelectedItem = self.ListBox2.get('active')
        SelectedItemKey = SelectedItem.split()[0]

        if SelectedItemKey != 'Key':
            School = self.Registered.FindKey(SelectedItemKey)
            self.Registered.RemoveFromList(School)

            # Modify
            ModifySchoolDialog = SetupMenuModifyRegisterSchool(
                self.root, School, self.Registered, self.MedTitleFont, self.BodyFont
            )
            SelKey = ModifySchoolDialog.SelKey

            if SelKey is not None:
                School.Key = SelKey
                self.Registered.AddToList(School)
            else:
                self.Registered.AddToList(School)

            self.Registered.SortList()
            # Update ListBox
            self.ListBox2.delete(0, tk.END)
            HeaderString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key', 'School', 'Location', 'Z Score')
            self.ListBox2.insert(1, HeaderString)
            for i, School in enumerate(self.Registered.SchoolList):
                NumString = "{:2.3f}".format(School.HistZScore)
                SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                    School.Key, School.Name, School.Location, NumString
                )
                self.ListBox2.insert(1 + i, SchoolString)

    def Remove(self):
        SelectedItem = self.ListBox2.get('active')
        SelectedItemKey = SelectedItem.split()[0]

        if SelectedItemKey != 'Key':
            self.Registered.RemoveFromListKey(SelectedItemKey)
            self.Registered.SortList()
            self.ListBox2.delete(0, tk.END)
            HeaderString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key', 'School', 'Location', 'Z Score')
            self.ListBox2.insert(1, HeaderString)
            for i, School in enumerate(self.Registered.SchoolList):
                NumString = "{:2.3f}".format(School.HistZScore)
                SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                    School.Key, School.Name, School.Location, NumString
                )
                self.ListBox2.insert(1 + i, SchoolString)

    def Order(self):
        if not self.Registered.ValidKeyOrder():
            messagebox.showerror("Error", "Keys must be in the form of a letter followed by a number (e.g. A1, A2, B1, B2, etc.)")
            return

        self.Registered.SortList()
        self.ListBox2.delete(0, tk.END)
        HeaderString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key', 'School', 'Location', 'Z Score')
        self.ListBox2.insert(1, HeaderString)
        for i, School in enumerate(self.Registered.SchoolList):
            NumString = "{:2.3f}".format(School.HistZScore)
            SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(
                School.Key, School.Name, School.Location, NumString
            )
            self.ListBox2.insert(1 + i, SchoolString)

    def Done(self):
        if not self.Registered.ValidKeyOrder():
            messagebox.showerror("Error", "Keys must be in the form of a letter followed by a number (e.g. A1, A2, B1, B2, etc.)")
            return

        CompetitionDialog = SetupMenuCompetitionName(self.root, self.MedTitleFont, self.BodyFont)
        CompetitionName = CompetitionDialog.CompetitionName

        if CompetitionName is not None:
            FileName = self.DataDir + CompetitionName + ".csv"
            Competition = CompetitionSchoolList(
                SchoolList=[],
                File=FileName,
                MasterDir=self.MasterDir,
                DataDir=self.DataDir
            )
            Competition.CompeteRegistered(self.Registered)
            Competition.WriteToFile()
            self.GotoMainMenu()

    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def GotoMainMenu(self):
        self.ClearBody()
        MainMenuBody(self.master, self.root, self.TitleFont, self.MedTitleFont, self.BodyFont, self.DataDir)

class CompMainMenuBody:
    def __init__(self, master, root, TitleFont, MedTitleFont, BodyFont, Competition):
        self.TitleFont = TitleFont
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.master = master
        self.root = root
        self.Competition = Competition

        F1 = tk.Frame(master, bd=1)
        F1.grid(row=0, column=0)
        Str1 = 'Competition Menu\n'
        tk.Label(F1, text=Str1, bd=1, font=self.TitleFont).grid(row=0, column=0)

        F2 = tk.Frame(master, bd=1)
        F2.grid(row=1, column=0)

        a1 = tk.Button(F2, text="1. Group Contest", font=self.BodyFont, width=32, command=self.GotoGroupMenu)
        a1.grid(row=0, column=0)

        b1 = tk.Button(F2, text="2. Swiss Contest", font=self.BodyFont, width=32, command=self.GotoSwissMenu)
        b1.grid(row=1, column=0)

        c1 = tk.Button(F2, text="3. Cross Contest", font=self.BodyFont, width=32, command=self.GotoCrossMenu)
        c1.grid(row=2, column=0)

        d1 = tk.Button(F2, text="4. Relay Contest", font=self.BodyFont, width=32, command=self.GotoRelayMenu)
        d1.grid(row=3, column=0)

        e1 = tk.Button(F2, text="5. Run Report", font=self.BodyFont, width=32, command=self.RunReport)
        e1.grid(row=4, column=0)

        f1 = tk.Button(F2, text="6. Back", font=self.BodyFont, width=32, command=self.GotoMainMenu)
        f1.grid(row=5, column=0)

    def GotoGroupMenu(self):
        self.ClearBody()
        SchoolDialog = SchoolNameSelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
        SchoolKey = SchoolDialog.SelKey
        if SchoolKey is not None:
            SingleSchoolContestBody(
                self.master, self.root, self.TitleFont, self.MedTitleFont,
                self.BodyFont, self.Competition, SchoolKey, 'Group', 10
            )

    def GotoSwissMenu(self):
        self.ClearBody()
        RoundDialog = SwissRoundNumberselector(self.root, self.MedTitleFont, self.BodyFont)
        RoundNum = RoundDialog.SelKey
        if RoundNum is not None:
            SiteDialog = SiteSelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
            Site = SiteDialog.SelKey
            if Site is not None:
                SwissContestBody(
                    self.master, self.root, self.TitleFont, self.MedTitleFont,
                    self.BodyFont, self.Competition, RoundNum, Site
                )

    def GotoCrossMenu(self):
        self.ClearBody()
        SchoolDialog = SchoolNameSelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
        SchoolKey = SchoolDialog.SelKey
        if SchoolKey is not None:
            SingleSchoolContestBody(
                self.master, self.root, self.TitleFont, self.MedTitleFont,
                self.BodyFont, self.Competition, SchoolKey, 'Cross', 10
            )

    def GotoRelayMenu(self):
        self.ClearBody()
        SchoolDialog = SchoolNameSelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
        SchoolKey = SchoolDialog.SelKey
        if SchoolKey is not None:
            SingleSchoolContestBody(
                self.master, self.root, self.TitleFont, self.MedTitleFont,
                self.BodyFont, self.Competition, SchoolKey, 'Relay', 5
            )

    def RunReport(self):
        self.ClearBody()
        ReportMenu(self.master, self.root, self.TitleFont, self.MedTitleFont, self.BodyFont, self.Competition)

    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def GotoMainMenu(self):
        self.ClearBody()
        MainMenuBody(self.master, self.root, self.TitleFont, self.MedTitleFont, self.BodyFont, self.Competition.DataDir)

class SingleSchoolContestBody:
    def __init__(self, master, root, TitleFont, MedTitleFont, BodyFont, Competition, SchoolKey, ContestName, QuestionGrouping):
        self.TitleFont = TitleFont
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.master = master
        self.root = root
        self.Competition = Competition
        self.SchoolKey = SchoolKey
        self.ContestName = ContestName
        self.QuestionGrouping = QuestionGrouping

        self.School = Competition.FindKey(SchoolKey)

        F1 = tk.Frame(master, bd=1)
        F1.grid(row=0, column=0)
        Str1 = f'{ContestName} Contest\n'
        tk.Label(F1, text=Str1, bd=1, font=self.TitleFont).grid(row=0, column=0)

        F2 = tk.Frame(master, bd=1)
        F2.grid(row=1, column=0)

        F3 = tk.Frame(F2, bd=1)
        F3.grid(row=0, column=0)

        F4 = tk.Frame(F2, bd=1)
        F4.grid(row=0, column=1)

        F5 = tk.Frame(F2, bd=1)
        F5.grid(row=1, column=0)

        F6 = tk.Frame(F2, bd=1)
        F6.grid(row=1, column=1)

        tk.Label(F3, text="School", bd=1, font=self.MedTitleFont).grid(row=0, column=0)
        self.SchoolName = tk.Label(F3, text=self.School.Name, bd=1, font=self.BodyFont)
        self.SchoolName.grid(row=1, column=0)
        self.SchoolName.bind('<Button-1>', self.ChooseSchoolName)

        tk.Label(F4, text="Key", bd=1, font=self.MedTitleFont).grid(row=0, column=0)
        self.SchoolKeyLabel = tk.Label(F4, text=self.School.Key, bd=1, font=self.BodyFont)
        self.SchoolKeyLabel.grid(row=1, column=0)
        self.SchoolKeyLabel.bind('<Button-1>', self.ChooseSchoolKey)

        tk.Button(F5, text="Next School", width=10, font=self.BodyFont, command=self.NextSchool).grid(row=0, column=0)
        tk.Button(F5, text="Back", width=10, font=self.BodyFont, command=self.GotoCompMain).grid(row=0, column=1)

        F7 = tk.Frame(F6, bd=1)
        F7.grid(row=0, column=0)

        for i in range(QuestionGrouping):
            tk.Label(F7, text=f"Q{i+1}", bd=1, font=self.BodyFont).grid(row=0, column=i)
            Entry = tk.Entry(F7, width=5, font=self.BodyFont)
            Entry.grid(row=1, column=i)
            Entry.bind('<FocusOut>', partial(self.ValidateFocusLeft, i))
            Entry.bind('<Return>', partial(self.NextEntry, i, QuestionGrouping))
            Entry.bind('<BackSpace>', partial(self.ClearText, i))
            if ContestName == 'Group':
                Entry.insert(0, str(self.School.GroupScores[i]))
            elif ContestName == 'Cross':
                Entry.insert(0, str(self.School.CrossScores[i]))
            elif ContestName == 'Relay':
                Entry.insert(0, str(self.School.RelayScores[i]))

    def SumEntryVals(self, startindex, endindex):
        Sum = 0
        for i in range(startindex, endindex):
            try:
                Sum += int(self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].get())
            except ValueError:
                pass
        return Sum

    def ValidateFocusLeft(self, i, event=None):
        try:
            Val = int(self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].get())
            if Val < 0:
                self.InvalidResponse(i)
            else:
                self.ValidateInd(i)
        except ValueError:
            self.InvalidResponse(i)

    def NextEntry(self, i, n, event=None):
        if i < n - 1:
            self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i + 1].focus_set()
        else:
            self.Validate()

    def ClearText(self, i, event=None):
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].delete(0, tk.END)

    def InvalidResponse(self, i):
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].delete(0, tk.END)
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].insert(0, "0")

    def ValidateInd(self, i, Event=None):
        try:
            Val = int(self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].get())
            if Val < 0:
                self.InvalidResponse(i)
            else:
                if self.ContestName == 'Group':
                    self.School.GroupScores[i] = Val
                elif self.ContestName == 'Cross':
                    self.School.CrossScores[i] = Val
                elif self.ContestName == 'Relay':
                    self.School.RelayScores[i] = Val
        except ValueError:
            self.InvalidResponse(i)

    def Validate(self):
        for i in range(self.QuestionGrouping):
            self.ValidateInd(i)
        self.Competition.WriteToFile()
        self.Competition.UpdateTotalsSchool()
        self.ReloadScreen()

    def ChooseSchoolName(self, event=None):
        SchoolDialog = SchoolNameSelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
        SchoolKey = SchoolDialog.SelKey
        if SchoolKey is not None:
            self.SchoolKey = SchoolKey
            self.School = self.Competition.FindKey(SchoolKey)
            self.ReloadScreen()

    def ChooseSchoolKey(self, event=None):
        SchoolDialog = SchoolKeySelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
        SchoolKey = SchoolDialog.SelKey
        if SchoolKey is not None:
            self.SchoolKey = SchoolKey
            self.School = self.Competition.FindKey(SchoolKey)
            self.ReloadScreen()

    def ReloadScreen(self):
        self.ClearBody()
        SingleSchoolContestBody(
            self.master, self.root, self.TitleFont, self.MedTitleFont,
            self.BodyFont, self.Competition, self.SchoolKey,
            self.ContestName, self.QuestionGrouping
        )

    def NextSchool(self):
        SchoolDialog = SchoolNameSelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
        SchoolKey = SchoolDialog.SelKey
        if SchoolKey is not None:
            self.SchoolKey = SchoolKey
            self.School = self.Competition.FindKey(SchoolKey)
            self.ReloadScreen()

    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def GotoCompMain(self):
        self.ClearBody()
        CompMainMenuBody(self.master, self.root, self.TitleFont, self.MedTitleFont, self.BodyFont, self.Competition)

class SwissContestBody:
    def __init__(self, master, root, TitleFont, MedTitleFont, BodyFont, Competition, RoundNum, Site):
        self.TitleFont = TitleFont
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.master = master
        self.root = root
        self.Competition = Competition
        self.RoundNum = RoundNum
        self.Site = Site

        F1 = tk.Frame(master, bd=1)
        F1.grid(row=0, column=0)
        Str1 = f'Swiss Contest Round {RoundNum}\n'
        tk.Label(F1, text=Str1, bd=1, font=self.TitleFont).grid(row=0, column=0)

        F2 = tk.Frame(master, bd=1)
        F2.grid(row=1, column=0)

        F3 = tk.Frame(F2, bd=1)
        F3.grid(row=0, column=0)

        F4 = tk.Frame(F2, bd=1)
        F4.grid(row=0, column=1)

        F5 = tk.Frame(F2, bd=1)
        F5.grid(row=1, column=0)

        F6 = tk.Frame(F2, bd=1)
        F6.grid(row=1, column=1)

        tk.Label(F3, text="Round", bd=1, font=self.MedTitleFont).grid(row=0, column=0)
        self.RoundLabel = tk.Label(F3, text=RoundNum, bd=1, font=self.BodyFont)
        self.RoundLabel.grid(row=1, column=0)
        self.RoundLabel.bind('<Button-1>', self.ChooseRound)

        tk.Label(F4, text="Site", bd=1, font=self.MedTitleFont).grid(row=0, column=0)
        self.SiteLabel = tk.Label(F4, text=Site, bd=1, font=self.BodyFont)
        self.SiteLabel.grid(row=1, column=0)
        self.SiteLabel.bind('<Button-1>', self.ChooseSite)

        tk.Button(F5, text="Generate Round", width=10, font=self.BodyFont, command=self.GenerateRound).grid(row=0, column=0)
        tk.Button(F5, text="Print Round", width=10, font=self.BodyFont, command=self.PrintRound).grid(row=0, column=1)
        tk.Button(F5, text="Next Site", width=10, font=self.BodyFont, command=self.NextSite).grid(row=0, column=2)
        tk.Button(F5, text="Back", width=10, font=self.BodyFont, command=self.GotoCompMain).grid(row=0, column=3)

        F7 = tk.Frame(F6, bd=1)
        F7.grid(row=0, column=0)

        Schools = self.Competition.FindSwissSite(RoundNum, Site)
        for i, School in enumerate(Schools):
            tk.Label(F7, text=School.Key, bd=1, font=self.BodyFont).grid(row=0, column=i)
            Entry = tk.Entry(F7, width=5, font=self.BodyFont)
            Entry.grid(row=1, column=i)
            Entry.bind('<FocusOut>', partial(self.ValidateFocusLeft, i))
            Entry.bind('<Return>', partial(self.NextEntry, i, len(Schools)))
            Entry.bind('<BackSpace>', partial(self.ClearText, i))
            Entry.insert(0, str(School.SwissScores[int(RoundNum) - 1]))

    def ValidateFocusLeft(self, i, event=None):
        try:
            Val = int(self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].get())
            if Val < 0:
                self.InvalidResponse(i)
            else:
                self.ValidateInd(i)
        except ValueError:
            self.InvalidResponse(i)

    def NextEntry(self, i, n, event=None):
        if i < n - 1:
            self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i + 1].focus_set()
        else:
            self.Validate()

    def ClearText(self, i, event=None):
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].delete(0, tk.END)

    def InvalidResponse(self, i):
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].delete(0, tk.END)
        self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].insert(0, "0")

    def ValidateInd(self, i, Event=None):
        try:
            Val = int(self.master.winfo_children()[1].winfo_children()[1].winfo_children()[0].winfo_children()[i].get())
            if Val < 0:
                self.InvalidResponse(i)
            else:
                Schools = self.Competition.FindSwissSite(self.RoundNum, self.Site)
                Schools[i].SwissScores[int(self.RoundNum) - 1] = Val
        except ValueError:
            self.InvalidResponse(i)

    def Validate(self):
        Schools = self.Competition.FindSwissSite(self.RoundNum, self.Site)
        for i in range(len(Schools)):
            self.ValidateInd(i)
        self.Competition.WriteToFile()
        self.Competition.UpdateTotalsSchool()
        self.ReloadScreen()

    def NextSite(self):
        SiteDialog = SiteSelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
        Site = SiteDialog.SelKey
        if Site is not None:
            self.Site = Site
            self.ReloadScreen()

    def ChooseSchoolName(self, Name=None, event=None):
        SchoolDialog = SchoolNameSelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
        SchoolKey = SchoolDialog.SelKey
        if SchoolKey is not None:
            self.SchoolKey = SchoolKey
            self.School = self.Competition.FindKey(SchoolKey)
            self.ReloadScreen()

    def ChooseSchoolKey(self, Key=None, event=None):
        SchoolDialog = SchoolKeySelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
        SchoolKey = SchoolDialog.SelKey
        if SchoolKey is not None:
            self.SchoolKey = SchoolKey
            self.School = self.Competition.FindKey(SchoolKey)
            self.ReloadScreen()

    def ChooseSite(self, event=None):
        SiteDialog = SiteSelector(self.root, self.MedTitleFont, self.BodyFont, self.Competition)
        Site = SiteDialog.SelKey
        if Site is not None:
            self.Site = Site
            self.ReloadScreen()

    def ReloadScreen(self):
        self.ClearBody()
        SwissContestBody(
            self.master, self.root, self.TitleFont, self.MedTitleFont,
            self.BodyFont, self.Competition, self.RoundNum, self.Site
        )

    def ChooseRound(self, event=None):
        RoundDialog = SwissRoundNumberselector(self.root, self.MedTitleFont, self.BodyFont)
        RoundNum = RoundDialog.SelKey
        if RoundNum is not None:
            self.RoundNum = RoundNum
            self.ReloadScreen()

    def GenerateRound(self):
        # Check if previous round scores are missing
        if self.RoundNum > 1:
            missing_scores = False
            for School in self.Competition.SchoolList:
                if School.SwissScores[int(self.RoundNum) - 2] == 0:
                    missing_scores = True
                    break
            
            if missing_scores:
                if not messagebox.askyesno("Warning", 
                    f"Scores for round {int(self.RoundNum)-1} have not been entered for all schools. "
                    "Generating new pairings without these scores may result in unfair matches. "
                    "Do you want to continue?"):
                    return

        self.Competition.GenerateSwissPartners(self.RoundNum)
        self.Competition.WriteToFile()
        self.ReloadScreen()

    def PrintRound(self):
        self.Competition.PrintSwissPartnersCSV(self.RoundNum)
        self.Competition.PrintSwissPartners(self.RoundNum)

    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def GotoCompMain(self):
        self.ClearBody()
        CompMainMenuBody(self.master, self.root, self.TitleFont, self.MedTitleFont, self.BodyFont, self.Competition)

    def GotoCompMainGenScreen(self):
        self.ClearBody()
        CompMainMenuBody(self.master, self.root, self.TitleFont, self.MedTitleFont, self.BodyFont, self.Competition)

class ReportMenu:
    def __init__(self, master, root, TitleFont, MedTitleFont, BodyFont, Competition):
        self.TitleFont = TitleFont
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont
        self.master = master
        self.root = root
        self.Competition = Competition

        F1 = tk.Frame(master, bd=1)
        F1.grid(row=0, column=0)
        Str1 = 'Report Menu\n'
        tk.Label(F1, text=Str1, bd=1, font=self.TitleFont).grid(row=0, column=0)

        F2 = tk.Frame(master, bd=1)
        F2.grid(row=1, column=0)

        a1 = tk.Button(F2, text="1. Run Report", font=self.BodyFont, width=32, command=self.RunReport)
        a1.grid(row=0, column=0)

        b1 = tk.Button(F2, text="2. Update Master File", font=self.BodyFont, width=32, command=self.UpdateMasterFile)
        b1.grid(row=1, column=0)

        c1 = tk.Button(F2, text="3. Back", font=self.BodyFont, width=32, command=self.GotoCompMainGenScreen)
        c1.grid(row=2, column=0)

    def GotoCompMainGenScreen(self):
        self.ClearBody()
        CompMainMenuBody(self.master, self.root, self.TitleFont, self.MedTitleFont, self.BodyFont, self.Competition)

    def RunReport(self):
        self.Competition.PrintFinal()
        self.Competition.PrintOverall()

    def UpdateMasterFile(self):
        self.Competition.UpdateMasterFile()

    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()

def LoadMainMenu(root, LargeTitleFont, MedTitleFont, BodyFont):
    return MainMenuBody(root, root, LargeTitleFont, MedTitleFont, BodyFont) 