import Tkinter as tk
import tkFont
import tkFileDialog
import csv
import tkMessageBox
from functools import partial
from .DialogueBoxes import SetupMenuRegisterSchool,SetupMenuNewSchool,SetupMenuModifyRegisterSchool,SetupMenuCompetitionName
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
        self.ClearBody()
        CompMainMenuBody(self.master,self.root, self.TitleFont, self.MedTitleFont, self.BodyFont,self.DataDir)
        
        
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
                Comp = CompetitionSchoolList(File=CompNameDialog.FileName,MasterDir=self.MasterDir)
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
    def __init__(self, master,root, TitleFont, MedTitleFont, BodyFont,DataDir='./Data/'):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont
        self.MedTitleFont = MedTitleFont
        
        self.master = master
        self.root = root
        self.DataDir = DataDir
        self.MasterDir = self.DataDir + 'Master/'
        
        #Load Competition
        self.FileName = tkFileDialog.askopenfilename(initialdir = "./Data/",title = "Select file",filetypes = (("Comma Seperated Files","*.csv"),("all files","*.*")))
        
        if not self.FileName:
            #Cancel selected on dialogue box
            self.GotoMainMenu()
        else:
            
            #chek valid Competition
            
            self.Competition = CompetitionSchoolList(File=self.FileName,MasterDir=self.MasterDir)
            self.Competition.ReadFromFile()
            
            self.Competition.PrintList()
            
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
        print('Swiss')
        
    def GotoCrossMenu(self):
        print('Cross')
        
    def GotoRelayMenu(self):
        print('Relay')
        
    def ClearBody(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
    def GotoMainMenu(self):
        self.ClearBody()
        MainMenuBody(self.master,self.root,self.TitleFont,self.MedTitleFont, self.BodyFont,self.DataDir)

        
def LoadMainMenu(root,LargeTitleFont,MedTitleFont,BodyFont):
    root.title("MathDay ScoreKeeper")
    BodyFrame  = tk.Frame(root)
    BodyFrame.grid(row = 0, column = 0)
    MainMenuBody(BodyFrame,root,LargeTitleFont,MedTitleFont,BodyFont)
    
        

