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
        print('Group')
    
    def GotoSwissMenu(self):
        self.ClearBody()
        SwissContestBody(self.master,self.root,self.TitleFont,self.MedTitleFont,self.BodyFont,self.Competition,1,'A1')
        
    def GotoCrossMenu(self):
        print('Cross')
        
    def GotoRelayMenu(self):
        print('Relay')
        
    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
    def GotoMainMenu(self):
        self.ClearBody()
        MainMenuBody(self.master,self.root,self.TitleFont,self.MedTitleFont, self.BodyFont,self.Competition.DataDir)
        
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
            
            
            School1 = self.SwissPartners[0].Key
            School1Lab =  tk.Label(F2f1, text=School1,width=4,bd = 4, font=self.TitleFont)
            School1Lab.grid(row = 0, column = 1)
            ChooseSchool1Key = partial(self.ChooseSchoolKey,School1)
            School1Lab.bind('<Double-1>',ChooseSchool1Key)
            
            School1Name = self.SwissPartners[0].Name[:40]
            School1NameLab =  tk.Label(F2f1, text=School1Name,width=40,bd = 4, font=self.TitleFont)
            School1NameLab.grid(row = 0, column = 2)
            ChooseSchool1Name = partial(self.ChooseSchoolName,self.SwissPartners[0].Name)
            School1NameLab.bind('<Double-1>',ChooseSchool1Name)
            
            School1Score = self.SwissPartners[0].SwissScores[RoundNum-1]
            School1ScoreTKVal = tk.StringVar(self.master, value=str(School1Score))
            self.School1ScoreEntry =  tk.Entry(F2f1, textvariable=School1ScoreTKVal,width=4,bd = 4, font=self.TitleFont)
            self.School1ScoreEntry.grid(row = 0, column = 3)
            
            School2 = self.SwissPartners[1].Key
            School2Lab =  tk.Label(F2f1, text=School2,bd = 4,width=4, font=self.TitleFont)
            School2Lab.grid(row = 1, column = 1)
            ChooseSchool2Key = partial(self.ChooseSchoolKey,School2)
            School2Lab.bind('<Double-1>',ChooseSchool2Key)
            
            School2Name = self.SwissPartners[1].Name[:40]
            School2NameLab =  tk.Label(F2f1, text=School2Name,width=40,bd = 4, font=self.TitleFont)
            School2NameLab.grid(row = 1, column = 2)
            ChooseSchool2Name = partial(self.ChooseSchoolName,self.SwissPartners[1].Name)
            School2NameLab.bind('<Double-1>',ChooseSchool2Name)
            
            School2Score = self.SwissPartners[1].SwissScores[RoundNum-1]
            School2ScoreTKVal = tk.StringVar(self.master, value=str(School2Score))
            self.School2ScoreEntry =  tk.Entry(F2f1, textvariable=School2ScoreTKVal,width=4,bd = 4, font=self.TitleFont)
            self.School2ScoreEntry .grid(row = 1, column = 3)
    
    
            F3 = tk.Frame(F0,height=10,width=10, bd=1)
            F3.grid(row = 1, column = 1)
            
            ChangeRoundBut = tk.Button(F3, text="Change Round", font=self.BodyFont, width=16, command=self.ChooseRound)
            ChangeRoundBut.grid(row = 0, column = 0)
            
            GenerateRoundBut = tk.Button(F3, text="Generate Round", font=self.BodyFont, width=16, command=self.GenerateRound)
            GenerateRoundBut.grid(row = 1, column = 0)
    
            F4 = tk.Frame(F0,height=10,width=10, bd=1)
            F4.grid(row = 2, column = 1)
            
            OKBut = tk.Button(F4, text="Ok", font=self.TitleFont, width= 8, command=self.Validate)
            OKBut.grid(row = 0, column = 0)
            
            BackBut = tk.Button(F4, text="Back", font=self.TitleFont, width= 8, command=self.GotoCompMain)
            BackBut.grid(row = 1, column = 0)
        
    def Validate(self):
        Valid = False
        try:
            School1Score = int(self.School1ScoreEntry.get())
            
            if (School1Score < 0 or School1Score > self.Competition.ValidSwissScores[self.RoundNum - 1]):
                string1 = 'Entered Score for ' + self.SwissPartners[0].Name + ' Not Valid. \n Must be between 0 and ' + str(self.Competition.ValidSwissScores[self.RoundNum - 1]) 
                tkMessageBox.showwarning("Error", string1)
            else:
                #Assign The Value
                Valid = True
                self.SwissPartners[0].SwissScores[self.RoundNum-1] = School1Score
                
        except Exception:
            string1 = 'Entered Score for ' + self.SwissPartners[0].Name + ' Not A Number.'
            tkMessageBox.showwarning("Error", string1)
            #ZeroTKVal = tk.StringVar(self.master, value=str(0))
            #self.School1ScoreEntry.set(ZeroTKVal)
            
        try:
            School2Score = int(self.School2ScoreEntry.get())
            
            if (School2Score < 0 or School2Score  > self.Competition.ValidSwissScores[self.RoundNum - 1]):
                string1 = 'Entered Score for ' + self.SwissPartners[1].Name + ' Not Valid. \n Must be between 0 and ' + str(self.Competition.ValidSwissScores[self.RoundNum - 1]) 
                tkMessageBox.showwarning("Error", string1)
                Valid = False
            else:
                self.SwissPartners[1].SwissScores[self.RoundNum-1] = School2Score
                
        except Exception:
            Valid = False
            string1 = 'Entered Score for ' + self.SwissPartners[1].Name + ' Not A Number.'
            tkMessageBox.showwarning("Error", string1)
            #ZeroTKVal = tk.StringVar(self.master, value=str(0))
            #self.School1ScoreEntry.set(ZeroTKVal)
            #Valid
        return Valid
        
        
    
    def Print1(self):
        print('1')
        
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
        
    def ChooseSite(self,Key,event=None):
        
        if (self.Validate()):
            
            SiteSelectorDialog = SiteSelector(self.root,self.Competition,self.Site,self.TitleFont, self.BodyFont)
            
            self.Site = SiteSelectorDialog.SelKey
            self.ReloadScreen()
        
    def ReloadScreen(self):
        self.ClearBody()
        SwissContestBody(self.master,self.root,self.TitleFont,self.MedTitleFont,self.BodyFont,self.Competition,self.RoundNum,self.Site)
    
    def ChooseRound(self,event=None):
        if (self.Validate()):
            self.Competition.WriteToFile()
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
        
def LoadMainMenu(root,LargeTitleFont,MedTitleFont,BodyFont):
    root.title("MathDay ScoreKeeper")
    BodyFrame  = tk.Frame(root)
    BodyFrame.grid(row = 0, column = 0)
    MainMenuBody(BodyFrame,root,LargeTitleFont,MedTitleFont,BodyFont)
    
    

    
        

