import Tkinter as tk
import tkFont
import tkFileDialog
import csv
import tkMessageBox
from functools import partial
from .DialogueBoxes import SetupMenuRegisterSchool,SetupMenuNewSchool,SetupMenuModifyRegisterSchool,SetupMenuCompetitionName,SwissRoundNumberselector,SchoolKeySelector,SiteSelector,SchoolNameSelector
from ..Structures.Structs import PreviousSchoolList,RegisterSchoolList,RegisteredSchool,PreviousSchool,CompetitionSchoolList
   
class MainMenuBody:
    def __init__(self, master,root, TitleFont,MedTitleFont, BodyFont,DataDir='./Data/'):
        
        self.TitleFont = TitleFont
        self.MedTitleFont= MedTitleFont 
        self.BodyFont = BodyFont
        
        self.master = master
        self.root = root
        self.DataDir = DataDir
               
        F1 = tk.Frame(self.master,height=10,width=10, bd=1)
        F1.grid(row = 0, column = 0)
        

        Str1 = 'Math Day Score Keeper Program'
        tk.Label(F1, text=Str1,bd = 4, font=self.TitleFont).grid(row = 0, column = 0)

        a1 = tk.Button(F1, text="1. Set-Up Competition", font=self.BodyFont, width=32, command=self.GotoSetupMenu)
        a1.grid(row = 1, column = 0)
        
        b1 = tk.Button(F1, text="2. Load Competition", font=self.BodyFont, width=32, command=self.GotoCompMain)
        b1.grid(row = 2, column = 0)
        
        c1 = tk.Button(F1, text="3. Exit", font=self.BodyFont, width=32, command=self.Exit)
        c1.grid(row = 3, column = 0)
        
    def Exit(self):
        self.root.destroy()
        
    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
    def GotoSetupMenu(self):
        self.ClearBody()
        SetupMenuBody(self.master,self.root,self.TitleFont,self.MedTitleFont, self.BodyFont,self.DataDir)
        
    def GotoCompMain(self):
        FileName = tkFileDialog.askopenfilename(initialdir = self.DataDir ,title = "Select Competition File",filetypes = (("Comma Seperated Files","*.csv"),('All Files','*')))
        
        if (FileName):
            self.ClearBody()
            MasterDir = self.DataDir + "Master/"
            Competition = CompetitionSchoolList(SchoolList=[],File=FileName,MasterDir=MasterDir,DataDir = self.DataDir)
            Competition.ReadFromFile()
            CompMainMenuBody(self.master,self.root, self.TitleFont, self.MedTitleFont, self.BodyFont,Competition)
        
        
# Set up Option 1        
class SetupMenuBody:
    def __init__(self, master,root, TitleFont,MedTitleFont, BodyFont,DataDir):

        
        self.TitleFont = TitleFont
        self.MedTitleFont = MedTitleFont
        self.BodyFont = BodyFont       
        
        self.master = master
        self.root = root
        self.DataDir= DataDir
        self.MasterDir = self.DataDir + "Master/"
        self.ContestNameInitScores = []
        
        self.PrevList = PreviousSchoolList(MasterFile=self.MasterDir + "Schools.csv")
        self.PrevList.ReadFromFile()   
        
        self.Registered = RegisterSchoolList(SchoolList=[])
        
        
        F1 = tk.Frame(master, bd=1)
        F1.grid(row = 0, column = 0)
        Str1 = 'Competition Set-Up\n'
        tk.Label(F1, text=Str1,bd = 1, font=self.TitleFont).grid(row = 0, column = 0)
               
        F2 = tk.Frame(master, bd=1)
        F2.grid(row = 1, column = 0)
        
        F3 = tk.Frame(master, bd=1)
        F3.grid(row = 2, column = 0)
        
        F4 = tk.Frame(F2, bd=1)
        F4.grid(row = 0, column = 0)
        
        F5 = tk.Frame(F2, bd=1)
        F5.grid(row = 0, column = 1)
        
        F6 = tk.Frame(F2, bd=1)
        F6.grid(row = 1, column = 0)
        
        F7 = tk.Frame(F2, bd=1)
        F7.grid(row = 1, column = 1)
        
        
        tk.Button(F6, text="New",width=10, font=self.BodyFont, command=self.AddSchoolToList).grid(row = 0, column = 0)
        tk.Button(F6, text="Register",width=10, font=self.BodyFont, command=self.RegisterSchool).grid(row = 0, column = 1)
        
        
        
        tk.Button(F7, text="Modify",width=10, font=self.BodyFont, command=self.Modify).grid(row = 0, column = 0)
        tk.Button(F7, text="Remove",width=10, font=self.BodyFont, command=self.Remove).grid(row = 0, column = 1)
        tk.Button(F7, text="Order",width=10, font=self.BodyFont, command=self.Order).grid(row = 0, column = 2)
        tk.Button(F7, text="Done",width=10, font=self.BodyFont, command=self.Done).grid(row = 0, column = 3)

        tk.Button(F7, text="Back",width=10, font=self.BodyFont, command=self.GotoMainMenu).grid(row = 1, column = 3)

        tk.Label(F4, text="Previous School List",bd = 1, font=self.MedTitleFont).grid(row = 0, column = 0)
        
        
        self.ListBox1 = tk.Listbox(F4,width= 40,font=self.BodyFont)
        self.ListBox1.grid(row = 1, column = 0)
        self.ListBox1.bind('<Double-1>', self.RegisterSchool)
        
        scrollbar = tk.Scrollbar(F4, orient="vertical")
        scrollbar.config(command=self.ListBox1.yview)
        scrollbar.grid(row = 1, column = 1)
        self.ListBox1.config(yscrollcommand=scrollbar.set)
        
        
        i = 0
        for School in self.PrevList.SchoolList:
            self.ListBox1.insert(i,School.Name)
            i = i + 1
        
        tk.Label(F5, text="Registered School List",bd = 1, font=self.MedTitleFont).grid(row = 0, column = 0)
        self.ListBox2 = tk.Listbox(F5,width= 80,font=self.BodyFont)
        self.ListBox2.grid(row = 1, column = 0)
        
        scrollbar = tk.Scrollbar(F5, orient="vertical")
        scrollbar.config(command=self.ListBox2.yview)
        scrollbar.grid(row = 1, column = 1)
        self.ListBox2.config(yscrollcommand=scrollbar.set)
        self.ListBox2.bind('<Double-1>', self.Modify)
        
        HeaderString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key','School','Location','Z Score')
        self.ListBox2.insert(1,HeaderString)
        #SeperatorString = "{:-^120}".format('')
        #self.ListBox2.insert(2,SeperatorString)


    def AddSchoolToList(self):

        AddSchoolDialog = SetupMenuNewSchool(self.root,self.MedTitleFont,self.BodyFont,self.Registered,self.PrevList)

        SelKey = AddSchoolDialog.SelKey
        SchoolName = AddSchoolDialog.NewSchoolName
        SchoolLocation = AddSchoolDialog.NewSchoolLocation
        
        if (SelKey != None):
        
            SchoolHist = PreviousSchool(SchoolName,SchoolLocation,0.0)
            SchoolReg = SchoolHist.Register(SelKey)
            
            self.PrevList.AddToList(SchoolHist)
            self.PrevList.SortList()
            self.PrevList.WriteToFile()
            
            #Add to Master File     
            
            self.Registered.AddToList(SchoolReg)
            

            self.ListBox1.delete(0,tk.END)
            i = 0
            for School in self.PrevList.SchoolList:
                self.ListBox1.insert(i,School.Name)
                i = i + 1
        

            NumString = "{:2.3f}".format(0)
            
            SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(SchoolReg.Key,SchoolReg.Name,SchoolReg.Location,NumString)
            
            self.ListBox2.insert(1 + len(self.Registered.SchoolList),SchoolString)


        
    def RegisterSchool(self,event=None):

        item = self.ListBox1.get('active')  #get clicked item
        School = self.PrevList.FindName(item)
        

        SchoolDialog = SetupMenuRegisterSchool(self.root,School,self.MedTitleFont,self.BodyFont,self.Registered)
        SelKey = SchoolDialog.SelKey
        
        if(SelKey != None):
            RegSchool = School.Register(SelKey)
            NumString = "{:2.3f}".format(RegSchool.HistZScore)
            SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(RegSchool.Key,RegSchool.Name,RegSchool.Location,NumString)
            
            self.ListBox2.insert(2 + len(self.Registered.SchoolList),SchoolString)
            
            self.Registered.AddToList(RegSchool)
       

    def Modify(self,event=None):
        SelectedItem = self.ListBox2.get('active')
        SelectedItemKey = SelectedItem.split( )[0]
        
        if SelectedItemKey != 'Key':
            
            School = self.Registered.FindKey(SelectedItemKey)
            
            self.Registered.RemoveFromList(School)
            
            #Modify
            ModifySchoolDialog = SetupMenuModifyRegisterSchool(self.root,School,self.Registered,self.MedTitleFont,self.BodyFont)
            
            SelKey = ModifySchoolDialog.SelKey
            
            if(SelKey != None):
                
                School.Key = SelKey
                self.Registered.AddToList(School)
                
            else:
                self.Registered.AddToList(School)
            
            self.Registered.SortList()
            #Update ListBox
            self.ListBox2.delete(0,tk.END)
            HeaderString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key','School','Location','Z Score')
            self.ListBox2.insert(1,HeaderString)
            i = 0
            for School in self.Registered.SchoolList:
                NumString = "{:2.3f}".format(School.HistZScore)
                SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(School.Key,School.Name,School.Location,NumString)
                self.ListBox2.insert(1 + i,SchoolString)
                i = i + 1
  

        
    def Remove(self):
        SelectedItem = self.ListBox2.get('active')
        SelectedItemKey = SelectedItem.split( )[0]
        
        if SelectedItemKey != 'Key':
            
            self.Registered.RemoveFromListKey(SelectedItemKey)            
            self.Registered.SortList()
            #Update ListBox
            self.ListBox2.delete(0,tk.END)
            HeaderString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key','School','Location','Z Score')
            self.ListBox2.insert(1,HeaderString)
            i = 0
            for School in self.Registered.SchoolList:
                NumString = "{:2.3f}".format(School.HistZScore)
                SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(School.Key,School.Name,School.Location,NumString)
                self.ListBox2.insert(1 + i,SchoolString)
                i = i + 1

    def Order(self):
        self.Registered.SortList()
        self.ListBox2.delete(0,tk.END)
        HeaderString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format('Key','School','Location','Z Score')
        self.ListBox2.insert(1,HeaderString)
        i = 0
        for School in self.Registered.SchoolList:
            NumString = "{:2.3f}".format(School.HistZScore)
            SchoolString = "{:^5}|{:^40.40}|{:^10}|{:^8}".format(School.Key,School.Name,School.Location,NumString)
            self.ListBox2.insert(1 + i,SchoolString)
            i = i + 1

    def Done(self):
        self.Order()
        
        if (not self.Registered.ValidKeyOrder()):
            tkMessageBox.showwarning("Error", 'Invalid Keys. \n Check Key List is valid. \n (Every Key should be followed by either numerical or alphabetical successor)')
        else:
            CompNameDialog = SetupMenuCompetitionName(self.root,self.DataDir, self.MedTitleFont, self.BodyFont)
            if (CompNameDialog.FileName != None):
                Comp = CompetitionSchoolList(File=CompNameDialog.FileName,MasterDir=self.MasterDir,DataDir=self.DataDir)
                Comp.CompeteRegistered(self.Registered)
                Comp.WriteToFile()
                self.GotoMainMenu()

  
        
    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()
            
    def GotoMainMenu(self):
        self.ClearBody()
        MainMenuBody(self.master,self.root,self.TitleFont,self.MedTitleFont, self.BodyFont,self.DataDir)

class CompMainMenuBody:
    def __init__(self, master,root, TitleFont, MedTitleFont, BodyFont,Competition):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont
        self.MedTitleFont = MedTitleFont
        
        self.master = master
        self.root = root
        
        #Load Competition
        self.Competition = Competition       

        
        F1 = tk.Frame(self.master,height=10,width=10, bd=1)
        F1.grid(row = 0, column = 0)
        
        #CCompetition Name
        Str1 = 'Math Day Score Keeper Program'
        tk.Label(F1, text=Str1,bd = 4, font=self.TitleFont).grid(row = 0, column = 0)

        a1 = tk.Button(F1, text="Group Contest", font=self.BodyFont, width=32, command=self.GotoGroupMenu)
        a1.grid(row = 1, column = 0)
        
        b1 = tk.Button(F1, text="Swiss Contest", font=self.BodyFont, width=32, command=self.GotoSwissMenu)
        b1.grid(row = 2, column = 0)
        
        c1 = tk.Button(F1, text="Cross Contest", font=self.BodyFont, width=32, command=self.GotoCrossMenu)
        c1.grid(row = 3, column = 0)
        
        d1 = tk.Button(F1, text="Relay Contest", font=self.BodyFont, width=32, command=self.GotoRelayMenu)
        d1.grid(row = 4, column = 0)
        
        f1 = tk.Button(F1, text="Back", font=self.BodyFont, width=32, command=self.GotoMainMenu)
        f1.grid(row = 5, column = 0)
        
    def GotoGroupMenu(self):
        self.ClearBody()
        GroupContestBody(self.master,self.root,self.TitleFont,self.MedTitleFont,self.BodyFont,self.Competition,self.Competition.SchoolList[0].Key)

    
    def GotoSwissMenu(self):
        self.ClearBody()
        SwissContestBody(self.master,self.root,self.TitleFont,self.MedTitleFont,self.BodyFont,self.Competition,1,self.Competition.ValidSwissSites[0])
        
    def GotoCrossMenu(self):
        self.ClearBody()
        CrossContestBody(self.master,self.root,self.TitleFont,self.MedTitleFont,self.BodyFont,self.Competition,self.Competition.SchoolList[0].Key)

        
    def GotoRelayMenu(self):
        self.ClearBody()
        RelayContestBody(self.master,self.root,self.TitleFont,self.MedTitleFont,self.BodyFont,self.Competition,self.Competition.SchoolList[0].Key)

        
    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
    def GotoMainMenu(self):
        self.ClearBody()
        MainMenuBody(self.master,self.root,self.TitleFont,self.MedTitleFont, self.BodyFont,self.Competition.DataDir)


#Group Competition
class GroupContestBody:
    def __init__(self, master,root, TitleFont, MedTitleFont, BodyFont,Competition,SchoolKey):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont
        self.MedTitleFont = MedTitleFont
        
        self.Competition = Competition
        
        self.master = master
        self.root = root
        
        self.SchoolKey = SchoolKey
        self.School = self.Competition.FindKey(self.SchoolKey)
                
        
        F0 = tk.Frame(self.master,height=10,width=10, bd=1)
        F0.grid(row = 0, column = 0)
        
        #CCompetition Name
        Str1 = 'Group Contest'
        tk.Label(F0, text=Str1,bd = 4, font=self.TitleFont).grid(row = 0, column = 0)
        
        F1 = tk.Frame(self.master,height=10,width=10, bd=1)
        F1.grid(row = 1, column = 0)
        
        F1f1 = tk.Frame(F1,height=10,width=10, bd=1)
        F1f1.grid(row = 0, column = 0)
        
        School1 = self.School.Key
        School1Lab =  tk.Label(F1f1, text=School1,width=4,bd = 4, font=self.TitleFont)
        School1Lab.grid(row = 0, column = 0)
        School1Lab.bind('<Double-1>',self.ChooseSchoolKey)
        
        School1Name = self.School.Name[:40]
        School1NameLab =  tk.Label(F1f1, text=School1Name,width=40,bd = 4, font=self.TitleFont)
        School1NameLab.grid(row = 0, column = 1)
        School1NameLab.bind('<Double-1>',self.ChooseSchoolName)
        
        F1f2 = tk.Frame(F1,height=10,width=10, bd=1)
        F1f2.grid(row = 1, column = 0)
        
        #Put In Questions And Labels
        GroupNum = 4
        self.Entries = []
        
                
        for i in range(len(self.Competition.ValidGroupNames)):
            QString = 'Q' + str(self.Competition.ValidGroupNames[i])
            tk.Label(F1f2, text=QString,width=6,bd = 4, font=self.TitleFont).grid(row=2*(i/GroupNum),column=i%GroupNum)
            
            TempEntryVal = tk.StringVar(value=str(self.School.GroupScores[i]))
            self.Entries.append(tk.Entry(F1f2, textvariable=TempEntryVal,width=4,bd = 4, font=self.TitleFont))
            self.Entries[i].grid(row=2*(i/GroupNum) + 1,column=i%GroupNum)
            
            EntryClearTest = partial(self.ClearText, i)
            self.Entries[i].bind('<FocusIn>', EntryClearTest)
            
            ValidateOnLeave = partial(self.ValidateFocusLeft, i)
            self.Entries[i].bind('<FocusOut>', ValidateOnLeave)
        
        #All widgets need to be created for next to work
        for i in range(len(self.Entries)):
            EntryNext = partial(self.NextEntry, i,len(self.Entries))
            self.Entries[i].bind('<Return>', EntryNext)
        
        
        F2 = tk.Frame(self.master,height=10,width=10, bd=1)
        F2.grid(row = 2, column = 0)
        
        tk.Button(F2, text="Select School Key", font=self.BodyFont, width= 20, command=self.ChooseSchoolKey).grid(row = 0, column = 0)
        tk.Button(F2, text="Select School Name", font=self.BodyFont, width= 20, command=self.ChooseSchoolName).grid(row = 0, column = 1)
        
        BackBut = tk.Button(F2, text="Back", font=self.TitleFont, width= 8, command=self.GotoCompMain)
        BackBut.grid(row = 1, column = 2)

    def ValidateFocusLeft(self,i,event=None):
        if( not self.ValidateInd(i)):
            self.Entries[i].focus()

        
    def NextEntry(self,i,n,event=None):
        if (i < n -1):
            
            if(self.ValidateInd(i)):
                self.Entries[i+1].focus()
            else:
                self.InvalidResponse(i)
        else:
            
            if(self.ValidateInd(i)):
                #Current School Index =
                Curi = self.Competition.SchoolList.index(self.School)
                
                self.Competition.WriteToFile()
                self.SchoolKey = self.Competition.SchoolList[ (Curi + 1) % len(self.Competition.SchoolList)].Key
                
                self.ReloadScreen()
                
            else:
                self.InvalidResponse(i)

    def ClearText(self,i,event=None):
        self.Entries[i].delete(0, "end")
    
    def InvalidResponse(self,i):
        self.ClearText(i)
        self.Entries[i].focus()

    def ValidateInd(self,i,Event=None):
        
        if (self.Entries[i].get() == ''):
            self.Entries[i].insert(0, str(self.School.GroupScores[i]))
        
        try:
            TempScore = int(self.Entries[i].get())
            
            if (TempScore < 0 or TempScore > self.Competition.ValidGroupScores[i]):
                    string1 = 'Entered Score for Q' + str(self.Competition.ValidGroupNames[i]) + ' Not Valid. \n Must be between 0 and ' + str(self.Competition.ValidGroupScores[i]) 
                    tkMessageBox.showwarning("Error", string1)
                    return False
            else:
                self.School.GroupScores[i] = TempScore 
                return True
        
        except Exception:
                string1 = 'Entered Score for Q' + str(self.Competition.ValidGroupNames[i]) + ' Not A Number.'
                tkMessageBox.showwarning("Error", string1)
                
                return False

    def Validate(self):
        Valids = []
        
        for i in range(len(self.Competition.ValidGroupScores)):
            
            if (self.Entries[i].get() == ''):
                self.Entries[i].insert(0, str(self.School.GroupScores[i]))
         
            try:
                TempScore = int(self.Entries[i].get())
                
                if (TempScore < 0 or TempScore > self.Competition.ValidGroupScores[i]):
                    string1 = 'Entered Score for Q' + str(self.Competition.ValidGroupNames[i]) + ' Not Valid. \n Must be between 0 and ' + str(self.Competition.ValidGroupScores[i]) 
                    tkMessageBox.showwarning("Error", string1)
                    Valids.append(False)
                else:
                    Valids.append(True)
                    self.School.GroupScores[i] = TempScore 
                    
            except Exception:
                string1 = 'Entered Score for Q' + str(self.Competition.ValidGroupNames[i]) + ' Not A Number.'
                tkMessageBox.showwarning("Error", string1)
                Valids.append(False)
        
        if False in Valids:
            return False
        else:
            self.Competition.WriteToFile()
            return True


    def ChooseSchoolName(self,event=None):
        
        if (self.Validate()):
            SchoolKeySelectorDialog = SchoolNameSelector(self.root,self.Competition,self.School.Name,self.TitleFont, self.BodyFont)
            
            #Find Site by School Key
            SchoolFound = self.Competition.FindName(SchoolKeySelectorDialog.SelName)
            self.SchoolKey = SchoolFound.Key
            self.ReloadScreen()
        
    def ChooseSchoolKey(self,event=None):
        
        if (self.Validate()):
            SchoolKeySelectorDialog = SchoolKeySelector(self.root,self.Competition,self.School.Key,self.TitleFont, self.BodyFont)
            
            #Find Site by School Key
            self.SchoolKey = SchoolKeySelectorDialog.SelKey
            self.ReloadScreen()
        
    def ReloadScreen(self):
        self.ClearBody()
        GroupContestBody(self.master,self.root,self.TitleFont,self.MedTitleFont,self.BodyFont,self.Competition,self.SchoolKey)   
        
    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
    def GotoCompMain(self):
        
        if (self.Validate()):
            self.ClearBody()
            
            CompMainMenuBody(self.master,self.root, self.TitleFont, self.MedTitleFont, self.BodyFont,self.Competition)



#SWISS Competition        
class SwissContestBody:
    def __init__(self, master,root, TitleFont, MedTitleFont, BodyFont,Competition,RoundNum,Site):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont
        self.MedTitleFont = MedTitleFont
        
        self.Competition = Competition
        
        self.master = master
        self.root = root
        
        self.RoundNum = RoundNum
        self.Site = Site
        
        #Check if Round Valid
        self.SwissPartners = self.Competition.SwissPartnerFindBySite(self.RoundNum ,self.Site)
        
        
        if (self.SwissPartners == None):
            #Generate Round
            Str1 = 'Swiss Contest Generate Round ' +str(self.RoundNum)
            tk.Label(self.master, text=Str1,bd = 4, font=self.TitleFont).grid(row = 0, column = 0)
            
            GenerateRoundBut = tk.Button(self.master, text="Generate Round", font=self.TitleFont, width=16, command=self.GenerateRound)
            GenerateRoundBut.grid(row = 1, column = 0)
            
            BackBut = tk.Button(self.master, text="Back", font=self.TitleFont, width= 8, command=self.GotoCompMainGenScreen)
            BackBut.grid(row = 1, column = 1)
            
        else:
            
            
            F1 = tk.Frame(self.master,height=10,width=10, bd=1)
            F1.grid(row = 0, column = 0)
            
            #CCompetition Name
            Str1 = 'Swiss Contest'
            tk.Label(F1, text=Str1,bd = 4, font=self.TitleFont).grid(row = 0, column = 0)
            
            Str1 = 'Round ' + str(self.RoundNum)
            RoundLab = tk.Label(F1, text=Str1,bd = 4, font=self.TitleFont)
            RoundLab.grid(row = 1, column = 0)
            RoundLab.bind('<Double-1>',self.ChooseRound)
            
            F0 = tk.Frame(self.master,height=10,width=10, bd=1)
            F0.grid(row = 1, column = 0)
        
            
            F2 = tk.Frame(F0,height=10,width=10, bd=1)
            F2.grid(row = 1, column = 0)
            
            F2f1 = tk.Frame(F2,height=10,width=10, bd=1)
            F2f1.grid(row = 0, column = 0)
            
            F2f1f1 = tk.Frame(F2f1,height=10,width=10, bd=1)
            F2f1f1.grid(row = 0, column = 0)
            
            SiteLab =  tk.Label(F2f1f1, text=self.Site,width=4,bd = 4, font=self.TitleFont)
            SiteLab.grid(row = 0, column = 0)
            SiteLab.bind('<Double-1>',self.ChooseSite)
            
            i = 0
            self.Entries = []
            for i in range( len(self.SwissPartners)  ):
                School= self.SwissPartners[i].Key
                SchoolLab =  tk.Label(F2f1, text=School,width=4,bd = 4, font=self.TitleFont)
                SchoolLab.grid(row = i, column = 1)
                ChooseSchoolKey = partial(self.ChooseSchoolKey,School)
                SchoolLab.bind('<Double-1>',ChooseSchoolKey)
                
                SchoolName = self.SwissPartners[i].Name[:40]
                SchoolNameLab =  tk.Label(F2f1, text=SchoolName,width=40,bd = 4, font=self.TitleFont)
                SchoolNameLab.grid(row = i, column = 2)
                ChooseSchoolName = partial(self.ChooseSchoolName,self.SwissPartners[i].Name)
                SchoolNameLab.bind('<Double-1>',ChooseSchoolName)
                
                
                SchoolScore = self.SwissPartners[i].SwissScores[RoundNum-1]
                SchoolScoreTKVal = tk.StringVar(self.master, value=str(SchoolScore))
                self.Entries.append(tk.Entry(F2f1, textvariable=SchoolScoreTKVal,width=4,bd = 4, font=self.TitleFont))
                self.Entries[i].grid(row = i, column = 3)
                
                EntryClearTest = partial(self.ClearText, i)
                self.Entries[i].bind('<FocusIn>', EntryClearTest)
                
                ValidateOnLeave = partial(self.ValidateFocusLeft, i)
                self.Entries[i].bind('<FocusOut>', ValidateOnLeave)
            
        
            
            
        
            #All widgets need to be created for next to work
            for i in range(len(self.Entries)):
                EntryNext = partial(self.NextEntry, i,len(self.Entries))
                self.Entries[i].bind('<Return>', EntryNext)
    
    
            F3 = tk.Frame(F0,height=10,width=10, bd=1)
            F3.grid(row = 1, column = 1)
            
            ChangeRoundBut = tk.Button(F3, text="Change Round", font=self.BodyFont, width=16, command=self.ChooseRound)
            ChangeRoundBut.grid(row = 0, column = 0)
            
            GenerateRoundBut = tk.Button(F3, text="Generate Round", font=self.BodyFont, width=16, command=self.GenerateRound)
            GenerateRoundBut.grid(row = 1, column = 0)
    
            F4 = tk.Frame(F0,height=10,width=10, bd=1)
            F4.grid(row = 2, column = 1)
            
            #OKBut = tk.Button(F4, text="Ok", font=self.TitleFont, width= 8, command=self.Validate)
            #OKBut.grid(row = 0, column = 0)
            
            BackBut = tk.Button(F4, text="Back", font=self.TitleFont, width= 8, command=self.GotoCompMain)
            BackBut.grid(row = 1, column = 0)
            
            F5 = tk.Frame(self.master,height=10,width=10, bd=1)
            F5.grid(row = 2, column = 0)
            
            
            tk.Button(F5, text="Select Site", font=self.BodyFont, width= 12, command=self.ChooseSite).grid(row = 0, column = 0)
            tk.Button(F5, text="Select School Key", font=self.BodyFont, width= 20, command=ChooseSchoolKey).grid(row = 0, column = 1)
            tk.Button(F5, text="Select School Name", font=self.BodyFont, width= 20, command=ChooseSchoolName).grid(row = 0, column = 2)


    def ValidateFocusLeft(self,i,event=None):
        if( not self.ValidateInd(i)):
            self.Entries[i].focus()

        
    def NextEntry(self,i,n,event=None):
        if (i < n -1):
            
            if(self.ValidateInd(i)):
                self.Entries[i+1].focus()
            else:
                self.InvalidResponse(i)
        else:
            
            if(self.ValidateInd(i)):
                #Current School Index =
                Curi = self.Competition.ValidSwissSites.index(self.Site)
                
                self.Competition.WriteToFile()
                self.Site = self.Competition.ValidSwissSites[ (Curi + 1) % len(self.Competition.ValidSwissSites)]
                
                self.ReloadScreen()
                
            else:
                self.InvalidResponse(i)

    def ClearText(self,i,event=None):
        self.Entries[i].delete(0, "end")
    
    def InvalidResponse(self,i):
        self.ClearText(i)
        self.Entries[i].focus()

    def ValidateInd(self,i,Event=None):
        
        if (self.Entries[i].get() == ''):
            self.Entries[i].insert(0, str(self.SwissPartners[i].SwissScores[self.RoundNum - 1]))
        
        try:
            TempScore = int(self.Entries[i].get())
            
            if (TempScore < 0 or TempScore > self.Competition.ValidSwissScores[self.RoundNum - 1]):
                    string1 = 'Entered Score for' + str(self.SwissPartners[i].Name) + ' Not Valid. \n Must be between 0 and ' + str(self.Competition.ValidSwissScores[self.RoundNum - 1]) 
                    tkMessageBox.showwarning("Error", string1)
                    return False
            else:
                self.SwissPartners[i].SwissScores[self.RoundNum - 1] = TempScore 
                return True
        
        except Exception:
                string1 = 'Entered Score for' + str(self.SwissPartners[i].Name) + ' Not A Number.'
                tkMessageBox.showwarning("Error", string1)
                
                return False            
        
    def Validate(self):
        Valids = []
        
        for i in range(len(self.Entries)):
            
            if (self.Entries[i].get() == ''):
                self.Entries[i].insert(0, str(self.SwissPartners[i].SwissScores[self.RoundNum - 1]))
         
            try:
                TempScore = int(self.Entries[i].get())
                
                if (TempScore < 0 or TempScore > self.Competition.ValidSwissScores[self.RoundNum - 1]):
                        string1 = 'Entered Score for' + str(self.SwissPartners[i].Name) + ' Not Valid. \n Must be between 0 and ' + str(self.Competition.ValidSwissScores[self.RoundNum - 1]) 
                        tkMessageBox.showwarning("Error", string1)
                        Valids.append(False)
                else:
                    self.SwissPartners[i].SwissScores[self.RoundNum - 1] = TempScore 
                    Valids.append(True)
                    
            except Exception:
                string1 = 'Entered Score for' + str(self.SwissPartners[i].Name) + ' Not A Number.'
                tkMessageBox.showwarning("Error", string1)
                Valids.append(False)
        
        if False in Valids:
            return False
        else:
            
            if (self.SwissPartners[0].SwissScores[self.RoundNum - 1] + self.SwissPartners[1].SwissScores[self.RoundNum - 1] != self.Competition.ValidSwissScores[self.RoundNum - 1]):
                string1 = 'Entered Scores for Teams Do Not Add To ' +str(self.Competition.ValidSwissScores[self.RoundNum - 1]) 
                tkMessageBox.showwarning("Error", string1)
                return False
                
            self.Competition.WriteToFile()
            return True

    def ChooseSchoolName(self,Key,event=None):
        
        if (self.Validate()):
            SchoolKeySelectorDialog = SchoolNameSelector(self.root,self.Competition,Key,self.TitleFont, self.BodyFont)
            
            #Find Site by School Key
            SchoolFound = self.Competition.FindName(SchoolKeySelectorDialog.SelName)
            self.Site = SchoolFound.SwissSites[self.RoundNum - 1]
            self.ReloadScreen()
        
    def ChooseSchoolKey(self,Key,event=None):
        
        if (self.Validate()):
            SchoolKeySelectorDialog = SchoolKeySelector(self.root,self.Competition,Key,self.TitleFont, self.BodyFont)
            
            #Find Site by School Key
            SchoolFound = self.Competition.FindKey(SchoolKeySelectorDialog.SelKey)
            self.Site = SchoolFound.SwissSites[self.RoundNum - 1]
            self.ReloadScreen()
        
    def ChooseSite(self,event=None):
        
        if (self.Validate()):
            
            SiteSelectorDialog = SiteSelector(self.root,self.Competition,self.Site,self.TitleFont, self.BodyFont)
            
            self.Site = SiteSelectorDialog.SelKey
            self.ReloadScreen()
        
    def ReloadScreen(self):
        self.ClearBody()
        SwissContestBody(self.master,self.root,self.TitleFont,self.MedTitleFont,self.BodyFont,self.Competition,self.RoundNum,self.Site)
    
    def ChooseRound(self,event=None):
        if (self.Validate()):
            RoundSelectDialog = SwissRoundNumberselector(self.root,self.Competition,self.RoundNum,self.TitleFont, self.BodyFont)
            self.RoundNum = RoundSelectDialog.SelRoundNum
            self.ReloadScreen()
    
    def GenerateRound(self):
        self.Competition.GenerateSwissPartners(self.RoundNum)
        self.ReloadScreen()
    
        
    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
    def GotoCompMain(self):
        
        if (self.Validate()):
            self.ClearBody()
            
            CompMainMenuBody(self.master,self.root, self.TitleFont, self.MedTitleFont, self.BodyFont,self.Competition)

    def GotoCompMainGenScreen(self):
        self.ClearBody()
        CompMainMenuBody(self.master,self.root, self.TitleFont, self.MedTitleFont, self.BodyFont,self.Competition)
 

class CrossContestBody:
    def __init__(self, master,root, TitleFont, MedTitleFont, BodyFont,Competition,SchoolKey):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont
        self.MedTitleFont = MedTitleFont
        
        self.Competition = Competition
        
        self.master = master
        self.root = root
        
        self.SchoolKey = SchoolKey
        self.School = self.Competition.FindKey(self.SchoolKey)
                
        
        F0 = tk.Frame(self.master,height=10,width=10, bd=1)
        F0.grid(row = 0, column = 0)
        
        #CCompetition Name
        Str1 = 'Cross Contest'
        tk.Label(F0, text=Str1,bd = 4, font=self.TitleFont).grid(row = 0, column = 0)
        
        F1 = tk.Frame(self.master,height=10,width=10, bd=1)
        F1.grid(row = 1, column = 0)
        
        F1f1 = tk.Frame(F1,height=10,width=10, bd=1)
        F1f1.grid(row = 0, column = 0)
        
        School1 = self.School.Key
        School1Lab =  tk.Label(F1f1, text=School1,width=4,bd = 4, font=self.TitleFont)
        School1Lab.grid(row = 0, column = 0)
        School1Lab.bind('<Double-1>',self.ChooseSchoolKey)
        
        School1Name = self.School.Name[:40]
        School1NameLab =  tk.Label(F1f1, text=School1Name,width=40,bd = 4, font=self.TitleFont)
        School1NameLab.grid(row = 0, column = 1)
        School1NameLab.bind('<Double-1>',self.ChooseSchoolName)
        
        F1f2 = tk.Frame(F1,height=10,width=10, bd=1)
        F1f2.grid(row = 1, column = 0)
        
        #Put In Questions And Labels
        self.Entries = []
        GroupNum = 4
        for i in range(len(self.Competition.ValidCrossNames)):
            QString = 'Q' + str(self.Competition.ValidCrossNames[i])
            tk.Label(F1f2, text=QString,width=6,bd = 4, font=self.TitleFont).grid(row=2*(i/GroupNum),column=i%GroupNum)
            
            TempEntryVal = tk.StringVar(value=str(self.School.CrossScores[i]))
            self.Entries.append(tk.Entry(F1f2, textvariable=TempEntryVal,width=4,bd = 4, font=self.TitleFont))
            self.Entries[i].grid(row=2*(i/GroupNum) + 1,column=i%GroupNum)
            
            EntryClearTest = partial(self.ClearText, i)
            self.Entries[i].bind('<FocusIn>', EntryClearTest)
            
            ValidateOnLeave = partial(self.ValidateFocusLeft, i)
            self.Entries[i].bind('<FocusOut>', ValidateOnLeave)
        

        for i in range(len(self.Entries)):
            EntryNext = partial(self.NextEntry, i,len(self.Entries))
            self.Entries[i].bind('<Return>', EntryNext)
             
        
        
        F2 = tk.Frame(self.master,height=10,width=10, bd=1)
        F2.grid(row = 2, column = 0)
        
        tk.Button(F2, text="Select School Key", font=self.BodyFont, width= 20, command=self.ChooseSchoolKey).grid(row = 0, column = 0)
        tk.Button(F2, text="Select School Name", font=self.BodyFont, width= 20, command=self.ChooseSchoolName).grid(row = 0, column = 1)
        
        BackBut = tk.Button(F2, text="Back", font=self.TitleFont, width= 8, command=self.GotoCompMain)
        BackBut.grid(row = 1, column = 2)
        
        
    def ValidateFocusLeft(self,i,event=None):
        if( not self.ValidateInd(i)):
            self.Entries[i].focus()

        
    def NextEntry(self,i,n,event=None):
        if (i < n -1):
            
            if(self.ValidateInd(i)):
                self.Entries[i+1].focus()
            else:
                self.InvalidResponse(i)
        else:
            
            if(self.ValidateInd(i)):
                #Current School Index =
                Curi = self.Competition.SchoolList.index(self.School)
                
                self.Competition.WriteToFile()
                self.SchoolKey = self.Competition.SchoolList[ (Curi + 1) % len(self.Competition.SchoolList)].Key
                
                self.ReloadScreen()
                
            else:
                self.InvalidResponse(i)

    def ClearText(self,i,event=None):
        self.Entries[i].delete(0, "end")
    
    def InvalidResponse(self,i):
        self.ClearText(i)
        self.Entries[i].focus()

    def ValidateInd(self,i,Event=None):
        
        if (self.Entries[i].get() == ''):
            self.Entries[i].insert(0, str(self.School.CrossScores[i]))
        
        try:
            TempScore = int(self.Entries[i].get())
            
            if (TempScore < 0 or TempScore > self.Competition.ValidCrossScores[i]):
                    string1 = 'Entered Score for Q' + str(self.Competition.ValidCrossNames[i]) + ' Not Valid. \n Must be between 0 and ' + str(self.Competition.ValidCrossScores[i]) 
                    tkMessageBox.showwarning("Error", string1)
                    return False
            else:
                self.School.CrossScores[i] = TempScore 
                return True
        
        except Exception:
                string1 = 'Entered Score for Q' + str(self.Competition.ValidCrossNames[i]) + ' Not A Number.'
                tkMessageBox.showwarning("Error", string1)
                
                return False

    def Validate(self):
        Valids = []
        
        for i in range(len(self.Competition.ValidCrossScores)):
            
            if (self.Entries[i].get() == ''):
                self.Entries[i].insert(0, str(self.School.CrossScores[i]))
         
            try:
                TempScore = int(self.Entries[i].get())
                
                if (TempScore < 0 or TempScore > self.Competition.ValidCrossScores[i]):
                    string1 = 'Entered Score for Q' + str(self.Competition.ValidCrossNames[i]) + ' Not Valid. \n Must be between 0 and ' + str(self.Competition.ValidCrossScores[i]) 
                    tkMessageBox.showwarning("Error", string1)
                    Valids.append(False)
                else:
                    Valids.append(True)
                    self.School.CrossScores[i] = TempScore 
                    
            except Exception:
                string1 = 'Entered Score for Q' + str(self.Competition.ValidCrossNames[i]) + ' Not A Number.'
                tkMessageBox.showwarning("Error", string1)
                Valids.append(False)
        
        if False in Valids:
            return False
        else:
            self.Competition.WriteToFile()
            return True


    def ChooseSchoolName(self,event=None):
        
        if (self.Validate()):
            SchoolKeySelectorDialog = SchoolNameSelector(self.root,self.Competition,self.School.Name,self.TitleFont, self.BodyFont)
            
            #Find Site by School Key
            SchoolFound = self.Competition.FindName(SchoolKeySelectorDialog.SelName)
            self.SchoolKey = SchoolFound.Key
            self.ReloadScreen()
        
    def ChooseSchoolKey(self,event=None):
        
        if (self.Validate()):
            SchoolKeySelectorDialog = SchoolKeySelector(self.root,self.Competition,self.School.Key,self.TitleFont, self.BodyFont)
            
            #Find Site by School Key
            self.SchoolKey = SchoolKeySelectorDialog.SelKey
            self.ReloadScreen()
        
    def ReloadScreen(self):
        self.ClearBody()
        CrossContestBody(self.master,self.root,self.TitleFont,self.MedTitleFont,self.BodyFont,self.Competition,self.SchoolKey)   
        
    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
    def GotoCompMain(self):
        
        if (self.Validate()):
            self.ClearBody()
            
            CompMainMenuBody(self.master,self.root, self.TitleFont, self.MedTitleFont, self.BodyFont,self.Competition)



class RelayContestBody:
    def __init__(self, master,root, TitleFont, MedTitleFont, BodyFont,Competition,SchoolKey):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont
        self.MedTitleFont = MedTitleFont
        
        self.Competition = Competition
        
        self.master = master
        self.root = root
        
        self.SchoolKey = SchoolKey
        self.School = self.Competition.FindKey(self.SchoolKey)
                
        
        F0 = tk.Frame(self.master,height=10,width=10, bd=1)
        F0.grid(row = 0, column = 0)
        
        #CCompetition Name
        Str1 = 'Relay Contest'
        tk.Label(F0, text=Str1,bd = 4, font=self.TitleFont).grid(row = 0, column = 0)
        
        F1 = tk.Frame(self.master,height=10,width=10, bd=1)
        F1.grid(row = 1, column = 0)
        
        F1f1 = tk.Frame(F1,height=10,width=10, bd=1)
        F1f1.grid(row = 0, column = 0)
        
        School1 = self.School.Key
        School1Lab =  tk.Label(F1f1, text=School1,width=4,bd = 4, font=self.TitleFont)
        School1Lab.grid(row = 0, column = 0)
        School1Lab.bind('<Double-1>',self.ChooseSchoolKey)
        
        School1Name = self.School.Name[:40]
        School1NameLab =  tk.Label(F1f1, text=School1Name,width=40,bd = 4, font=self.TitleFont)
        School1NameLab.grid(row = 0, column = 1)
        School1NameLab.bind('<Double-1>',self.ChooseSchoolName)
        
        F1f2 = tk.Frame(F1,height=10,width=10, bd=1)
        F1f2.grid(row = 1, column = 0)
        
        #Put In Questions And Labels
        GroupNum = 5
        self.Entries = []
        for i in range(len(self.Competition.ValidRelayNames)):
            QString = 'Q' + str(self.Competition.ValidRelayNames[i])
            tk.Label(F1f2, text=QString,width=6,bd = 4, font=self.TitleFont).grid(row=2*(i/GroupNum),column=i%GroupNum)
            
            TempEntryVal = tk.StringVar(value=str(self.School.RelayScores[i]))
            self.Entries.append(tk.Entry(F1f2, textvariable=TempEntryVal,width=4,bd = 4, font=self.TitleFont))
            self.Entries[i].grid(row=2*(i/GroupNum) + 1,column=i%GroupNum)
            
            
            EntryClearTest = partial(self.ClearText, i)
            self.Entries[i].bind('<FocusIn>', EntryClearTest)
            
            ValidateOnLeave = partial(self.ValidateFocusLeft, i)
            self.Entries[i].bind('<FocusOut>', ValidateOnLeave)
        
        #All widgets need to be created for next to work
        for i in range(len(self.Entries)):
            EntryNext = partial(self.NextEntry, i,len(self.Entries))
            self.Entries[i].bind('<Return>', EntryNext)
        
        
        F2 = tk.Frame(self.master,height=10,width=10, bd=1)
        F2.grid(row = 2, column = 0)
        
        tk.Button(F2, text="Select School Key", font=self.BodyFont, width= 20, command=self.ChooseSchoolKey).grid(row = 0, column = 0)
        tk.Button(F2, text="Select School Name", font=self.BodyFont, width= 20, command=self.ChooseSchoolName).grid(row = 0, column = 1)
        
        BackBut = tk.Button(F2, text="Back", font=self.TitleFont, width= 8, command=self.GotoCompMain)
        BackBut.grid(row = 1, column = 2)
        
        
    def ValidateFocusLeft(self,i,event=None):
        if( not self.ValidateInd(i)):
            self.Entries[i].focus()

        
    def NextEntry(self,i,n,event=None):
        if (i < n -1):
            
            if(self.ValidateInd(i)):
                self.Entries[i+1].focus()
            else:
                self.InvalidResponse(i)
        else:
            
            if(self.ValidateInd(i)):
                #Current School Index =
                Curi = self.Competition.SchoolList.index(self.School)
                
                self.Competition.WriteToFile()
                self.SchoolKey = self.Competition.SchoolList[ (Curi + 1) % len(self.Competition.SchoolList)].Key
                
                self.ReloadScreen()
                
            else:
                self.InvalidResponse(i)

    def ClearText(self,i,event=None):
        self.Entries[i].delete(0, "end")
    
    def InvalidResponse(self,i):
        self.ClearText(i)
        self.Entries[i].focus()

    def ValidateInd(self,i,Event=None):
        
        if (self.Entries[i].get() == ''):
            self.Entries[i].insert(0, str(self.School.RelayScores[i]))
        
        try:
            TempScore = int(self.Entries[i].get())
            
            if (TempScore < 0 or TempScore > self.Competition.ValidRelayScores[i]):
                    string1 = 'Entered Score for Q' + str(self.Competition.ValidRelayNames[i]) + ' Not Valid. \n Must be between 0 and ' + str(self.Competition.ValidRelayScores[i]) 
                    tkMessageBox.showwarning("Error", string1)
                    return False
            else:
                self.School.RelayScores[i] = TempScore 
                return True
        
        except Exception:
                string1 = 'Entered Score for Q' + str(self.Competition.ValidRelayNames[i]) + ' Not A Number.'
                tkMessageBox.showwarning("Error", string1)
                
                return False

    def Validate(self):
        Valids = []
        
        for i in range(len(self.Competition.ValidRelayScores)):
            
            if (self.Entries[i].get() == ''):
                self.Entries[i].insert(0, str(self.School.RelayScores[i]))
         
            try:
                TempScore = int(self.Entries[i].get())
                
                if (TempScore < 0 or TempScore > self.Competition.ValidRelayScores[i]):
                    string1 = 'Entered Score for Q' + str(self.Competition.ValidRelayNames[i]) + ' Not Valid. \n Must be between 0 and ' + str(self.Competition.ValidCrossScores[i]) 
                    tkMessageBox.showwarning("Error", string1)
                    Valids.append(False)
                else:
                    Valids.append(True)
                    self.School.RelayScores[i] = TempScore 
                    
            except Exception:
                string1 = 'Entered Score for Q' + str(self.Competition.ValidRelayNames[i]) + ' Not A Number.'
                tkMessageBox.showwarning("Error", string1)
                Valids.append(False)
        
        if False in Valids:
            return False
        else:
            self.Competition.WriteToFile()
            return True


    def ChooseSchoolName(self,event=None):
        
        if (self.Validate()):
            SchoolKeySelectorDialog = SchoolNameSelector(self.root,self.Competition,self.School.Name,self.TitleFont, self.BodyFont)
            
            #Find Site by School Key
            SchoolFound = self.Competition.FindName(SchoolKeySelectorDialog.SelName)
            self.SchoolKey = SchoolFound.Key
            self.ReloadScreen()
        
    def ChooseSchoolKey(self,event=None):
        
        if (self.Validate()):
            SchoolKeySelectorDialog = SchoolKeySelector(self.root,self.Competition,self.School.Key,self.TitleFont, self.BodyFont)
            
            #Find Site by School Key
            self.SchoolKey = SchoolKeySelectorDialog.SelKey
            self.ReloadScreen()
        
    def ReloadScreen(self):
        self.ClearBody()
        RelayContestBody(self.master,self.root,self.TitleFont,self.MedTitleFont,self.BodyFont,self.Competition,self.SchoolKey)   
        
    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
    def GotoCompMain(self):
        
        if (self.Validate()):
            self.ClearBody()
            
            CompMainMenuBody(self.master,self.root, self.TitleFont, self.MedTitleFont, self.BodyFont,self.Competition)

       
def LoadMainMenu(root,LargeTitleFont,MedTitleFont,BodyFont):
    root.title("MathDay ScoreKeeper")
    BodyFrame  = tk.Frame(root)
    BodyFrame.grid(row = 0, column = 0)
    MainMenuBody(BodyFrame,root,LargeTitleFont,MedTitleFont,BodyFont)
    
    

    
        

