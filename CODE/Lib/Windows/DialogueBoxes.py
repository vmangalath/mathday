

import Tkinter as tk
import tkMessageBox
import tkFont
import os
import string
from functools import partial
from ..Structures.Structs import PreviousSchoolList,RegisterSchoolList
from ..Functions.Functions import IsKey

class SetupMenuRegisterSchool(tk.Toplevel):

    def __init__(self, root,School, TitleFont, BodyFont,Registered, title = 'Register School From List'):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont 

        tk.Toplevel.__init__(self, root)
        self.transient(root)

        if title:
            self.title(title)

        self.root = root
        
        self.SelKey=None
        
        self.Registered = Registered
        self.Registered.SortList()
        
        if len(self.Registered.SchoolList) == 0:
            self.CurrKey = 'A1'
        else:
            PrevKey = self.Registered.SchoolList[-1].Key
            self.CurrKey = str(PrevKey[0] + str( int(PrevKey[1:]) + 1))
            
        self.School = School
        

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(row = 0, column = 0)

        self.wait_visibility()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (root.winfo_rootx()+50,
                                  root.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):      
        
        F0 = tk.Frame(self, bd=1)
        F0.grid(row = 0, column = 0)
        
        F1 = tk.Frame(F0, bd=1)
        F1.grid(row = 0, column = 0)
        
        tk.Label(F1, text="Key",width=6,bd = 1, font=self.TitleFont).grid(row = 1, column = 0)
        CurrKeytv = tk.StringVar(self, value=str(self.CurrKey))
        self.E1 = tk.Entry(F1, font=self.BodyFont,width=6,textvariable=CurrKeytv)
        self.E1.grid(row = 2, column = 0)
        
        F2 = tk.Frame(F0, bd=1)
        F2.grid(row = 0, column = 1)
        tk.Label(F2, text="School Name",bd = 1, font=self.TitleFont).grid(row = 1, column = 0)
        tk.Label(F2, text=self.School.Name,bd = 1,font=self.BodyFont).grid(row = 2, column = 0)
 

        tk.Button(self, text="OK", width=10, command=self.ok).grid(row=1, column=1)
        tk.Button(self, text="Cancel", width=10, command=self.cancel).grid(row=1, column=2)


    #
    # standard button semantics

    def ok(self, event=None):
        SelKey = self.E1.get()
        #Check Format
        
        if (not IsKey(SelKey)):   
            tkMessageBox.showwarning("Error", 'Invalid Key. \n Keys are an uppercase letter followed by one or two digits.')
        
        #Check if Key in list already
        elif (self.Registered.KeyInList(SelKey)):
            tkMessageBox.showwarning("Error", 'Key Already Registered')
        
        #School Already In List
        elif (self.Registered.NameInList(self.School.Name) ):
            tkMessageBox.showwarning("Error", 'School Already Registered')
        else:
            
            self.SelKey = SelKey
            self.withdraw()
            self.update_idletasks()
            self.cancel()
            
    def cancel(self, event=None):

        # put focus back to the parent window
        self.root.focus_set()
        self.destroy()
        

class SetupMenuModifyRegisterSchool(tk.Toplevel):

    def __init__(self, root,School,Registered, TitleFont, BodyFont, title = 'Modify School'):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont 

        tk.Toplevel.__init__(self, root)
        self.transient(root)

        if title:
            self.title(title)

        self.root = root
        
        self.SelKey=None
        
        self.Registered = Registered

        self.School = School


        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(row = 0, column = 0)

        self.wait_visibility()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (root.winfo_rootx()+50,
                                  root.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):      
        
        F0 = tk.Frame(self, bd=1)
        F0.grid(row = 0, column = 0)
        
        F1 = tk.Frame(F0, bd=1)
        F1.grid(row = 0, column = 0)
        
        tk.Label(F1, text="Key",width=6,bd = 1, font=self.TitleFont).grid(row = 1, column = 0)
        CurrKeytv = tk.StringVar(self, value=str(self.School.Key))
        self.E1 = tk.Entry(F1, font=self.BodyFont,width=6,textvariable=CurrKeytv)
        self.E1.grid(row = 2, column = 0)
        
        F2 = tk.Frame(F0, bd=1)
        F2.grid(row = 0, column = 1)
        tk.Label(F2, text="School Name",bd = 1, font=self.TitleFont).grid(row = 1, column = 0)
        tk.Label(F2, text=self.School.Name,bd = 1,font=self.BodyFont).grid(row = 2, column = 0)

        tk.Button(self, text="OK", width=10, command=self.ok).grid(row=1, column=1)
        tk.Button(self, text="Cancel", width=10, command=self.cancel).grid(row=1, column=2)        
    #
    # standard button semantics

    def ok(self, event=None):
        SelKey = self.E1.get()
        #Check Format
        if (not IsKey(SelKey)):
            tkMessageBox.showwarning("Error", 'Invalid Key. \n Keys are an uppercase letter followed by one or two digits.')
        elif (self.Registered.KeyInList(SelKey)):
            tkMessageBox.showwarning("Error", 'Key Already Registered')        
        else:
            
            self.SelKey = SelKey
            self.withdraw()
            self.update_idletasks()
            self.cancel()
            
    def cancel(self, event=None):

        # put focus back to the parent window
        self.root.focus_set()
        self.destroy()
        
        
class SetupMenuNewSchool(tk.Toplevel):

    def __init__(self, root, TitleFont, BodyFont,Registered,PrevList, title = 'New School'):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont 

        tk.Toplevel.__init__(self, root)
        self.transient(root)

        if title:
            self.title(title)

        self.root = root
        
        self.SelKey=None
        
        
        self.PrevList = PrevList
        
        self.Registered = Registered
        self.Registered.SortList()
        
        if len(self.Registered.SchoolList) == 0:
            self.CurrKey = 'A1'
        else:
            PrevKey = self.Registered.SchoolList[-1].Key
            self.CurrKey = str(PrevKey[0] + str( int(PrevKey[1:]) + 1))
            
    
        self.NewSchoolName = None
        self.NewSchoolLocation = 'City'
        self.VarLoc = None


        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(row = 0, column = 0)

        self.wait_visibility()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (root.winfo_rootx()+50,
                                  root.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):      
        
        F0 = tk.Frame(self, bd=1)
        F0.grid(row = 0, column = 0)
        
        F1 = tk.Frame(F0, bd=1)
        F1.grid(row = 0, column = 0)
        
        tk.Label(F1, text="Key",width=6,bd = 1, font=self.TitleFont).grid(row = 1, column = 0)
        
        CurrKeytv = tk.StringVar(self, value=str(self.CurrKey))
        self.E1 = tk.Entry(F1, font=self.BodyFont,width=6,textvariable=CurrKeytv)
        self.E1.grid(row = 2, column = 0)
        
        
        F2 = tk.Frame(F0, bd=1)
        F2.grid(row = 0, column = 1)
        tk.Label(F2, text="School Name",bd = 1, font=self.TitleFont).grid(row = 1, column = 0)
        
        self.E2 = tk.Entry(F2, font=self.BodyFont,width=40)
        self.E2.grid(row = 2, column = 0)
        
        F3 = tk.Frame(F0, bd=1)
        F3.grid(row = 0, column = 2)
        tk.Label(F3, text="Location",bd = 1, font=self.TitleFont).grid(row = 0, column = 0)
        
        self.VarLoc = tk.StringVar(value="City")
        tk.Radiobutton(F3, font=self.BodyFont, text="City", variable=self.VarLoc, value='City',
                          command=self.RadioSelectLocation).grid(row = 1, column = 0)        
        tk.Radiobutton(F3, font=self.BodyFont, text="Country", variable=self.VarLoc, value="Country",
                          command=self.RadioSelectLocation).grid(row = 2, column = 0)      


        tk.Button(self, text="OK", width=10, command=self.ok).grid(row=1, column=1)
        tk.Button(self, text="Cancel", width=10, command=self.cancel).grid(row=1, column=2)
        
    def RadioSelectLocation(self):
        self.NewSchoolLocation = self.VarLocation.get()
        
    #
    # standard button semantics

    def ok(self, event=None):
        SelKey = self.E1.get()
        SchoolName = self.E2.get()
        #Check Format
        #Check Format
        if (not IsKey(SelKey)):   
            tkMessageBox.showwarning("Error", 'Invalid Key. \n Keys are an uppercase letter followed by one or two digits.')
        
        #Check if Key in list already
        elif (self.Registered.KeyInList(SelKey)):
            tkMessageBox.showwarning("Error", 'Key Already Registered')
        
        #School Already In List
        elif (self.Registered.NameInList(SchoolName) ):
            tkMessageBox.showwarning("Error", 'School Already Registered')
        #School Already In List
        elif (self.PrevList.NameInList(SchoolName) ):
            tkMessageBox.showwarning("Error", 'School Already in Previous List')
        else:
            

            self.SelKey = SelKey
            self.NewSchoolName = SchoolName
            
            self.withdraw()
            self.update_idletasks()
            self.cancel()

            
    def cancel(self, event=None):

        # put focus back to the parent window
        self.root.focus_set()
        self.destroy()


class SetupMenuCompetitionName(tk.Toplevel):

    def __init__(self, root,DataDir, TitleFont, BodyFont, title = 'Competition Name'):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont 

        tk.Toplevel.__init__(self, root)
        self.transient(root)

        if title:
            self.title(title)

        self.root = root
        self.FileName = None
        self.DataDir = DataDir
        

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(row = 0, column = 0)

        self.wait_visibility()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (root.winfo_rootx()+50,
                                  root.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):      
                
        tk.Label(self, text="Competition Year",width=16,bd = 1, font=self.TitleFont).grid(row = 0, column = 0)
        self.E1 = tk.Entry(self, font=self.BodyFont,width=8)
        self.E1.grid(row = 1, column = 0)
        
        F1 = tk.Frame(self)
        F1.grid(row=2, column=0)       
        tk.Button(F1, text="OK", width=10, command=self.ok,font=self.BodyFont).grid(row=0, column=0)
        tk.Button(F1, text="Cancel", width=10, command=self.cancel,font=self.BodyFont).grid(row=0, column=1)


        
    #
    # standard button semantics

    def ok(self, event=None):
        CompName = self.E1.get()
        
        FileDir = self.DataDir + CompName + "/"
        
        FileName = FileDir + "/" + "Competition.csv"

        #Check Format
        if (os.path.isfile(FileName) ):
            tkMessageBox.showwarning("Year Error", 'Competition Year Already Exists')
        
        else:
            if not os.path.exists(FileDir):
                os.makedirs(FileDir)

            self.FileName = FileName
            
            self.withdraw()
            self.update_idletasks()
            self.cancel()

            
    def cancel(self, event=None):

        # put focus back to the parent window
        self.root.focus_set()
        self.destroy()

class SwissRoundNumberselector(tk.Toplevel):

    def __init__(self, root,Competition,RoundNum,TitleFont, BodyFont, title = 'Select Round Number'):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont 

        tk.Toplevel.__init__(self, root)
        self.transient(root)

        if title:
            self.title(title)

        self.root = root
        self.Competition = Competition
        self.RoundNum = RoundNum
        self.SelRoundNum = self.RoundNum
        self.TKSelRoundNum = tk.IntVar(value=self.SelRoundNum ) 
        

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(row = 0, column = 0)

        self.wait_visibility()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (root.winfo_rootx()+50,
                                  root.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):      
        
        for i in range(len(self.Competition.ValidSwissScores)):
            RoundName = "Round " + str(i +1)
            tk.Radiobutton(self, font=self.BodyFont, text=RoundName, variable=self.TKSelRoundNum, value=i+1,command=self.RadioSelect).grid(row = i, column = 0)              
        

        tk.Button(self, text="OK", width=10, command=self.ok).grid(row=len(self.Competition.ValidSwissScores) + 1, column=1)
        tk.Button(self, text="Cancel", width=10, command=self.cancel).grid(row=len(self.Competition.ValidSwissScores) + 1, column=2)

    def RadioSelect(self):
        self.SelRoundNum = self.TKSelRoundNum.get()
        
    #
    # standard button semantics

    def ok(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.leave()
            
    def leave(self):
        self.root.focus_set()
        self.destroy()

            
    def cancel(self, event=None):
        
        # put focus back to the parent window
        self.SelRoundNum = self.RoundNum
        self.leave()



class SchoolKeySelector(tk.Toplevel):

    def __init__(self, root,Competition,CurKey,TitleFont, BodyFont, title = 'Select School By Key'):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont 

        tk.Toplevel.__init__(self, root)
        self.transient(root)

        if title:
            self.title(title)

        self.root = root
        self.Competition = Competition
        self.CurKey = CurKey
        self.SelKey = self.CurKey
        

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(row = 0, column = 0)

        self.wait_visibility()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (root.winfo_rootx()+50,
                                  root.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):         
        
        itot = 0
        RowNum = 0
        for LetterAndNum in self.Competition.KeyLetterListCondensed:
            
            si = itot
            for i in range(si,si + LetterAndNum[1]):
                KeyName = self.Competition.SchoolList[i].Key
                GetValueLoc = partial(self.GetValue,KeyName)
                ButTemp = tk.Button(self, text=KeyName, width=4, command=GetValueLoc)
                ButTemp.grid(row=RowNum , column=(i - si))
                itot = itot + 1
            RowNum = RowNum + 1
            
        tk.Button(self, text="Cancel", width=10, command=self.cancel,font=self.BodyFont).grid(row=RowNum + 1, column=(i - si + 1) )
            
        
            
    def GetValue(self,Value):
        self.SelKey = Value
        self.ok()    
  
    #
    # standard button semantics

    def ok(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.leave()
            
    def leave(self):
        self.root.focus_set()
        self.destroy()

            
    def cancel(self, event=None):
        self.SelKey = self.CurKey
        self.leave()
        
class SiteSelector(tk.Toplevel):

    def __init__(self, root,Competition,CurKey,TitleFont, BodyFont, title = 'Select Site'):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont 

        tk.Toplevel.__init__(self, root)
        self.transient(root)

        if title:
            self.title(title)

        self.root = root
        self.Competition = Competition
        self.CurKey = CurKey
        self.SelKey = self.CurKey
        

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(row = 0, column = 0)

        self.wait_visibility()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (root.winfo_rootx()+50,
                                  root.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):         
        
        itot = 0
        RowNum = 0
        for LetterAndNum in self.Competition.SwissSitesLetterCondensed:
            
            si = itot
            for i in range(si,si + LetterAndNum[1]):
                
                KeyName = self.Competition.ValidSwissSites[i]
                GetValueLoc = partial(self.GetValue,KeyName)
                ButTemp = tk.Button(self, text=KeyName, width=4, command=GetValueLoc)
                ButTemp.grid(row=RowNum , column=(i - si))
                itot = itot + 1
                
            RowNum = RowNum + 1
            
        tk.Button(self, text="Cancel", width=10, command=self.cancel,font=self.BodyFont).grid(row=RowNum + 1, column=(i - si + 1) )
            
        
            
    def GetValue(self,Value):
        self.SelKey = Value
        self.ok()    
  
    #
    # standard button semantics

    def ok(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.leave()
            
    def leave(self):
        self.root.focus_set()
        self.destroy()

            
    def cancel(self, event=None):
        self.SelKey = self.CurKey
        self.leave()
        

class SchoolNameSelector(tk.Toplevel):

    def __init__(self, root,Competition,CurName,TitleFont, BodyFont, title = 'Select School By Name'):
        
        self.TitleFont = TitleFont
        self.BodyFont = BodyFont 

        tk.Toplevel.__init__(self, root)
        self.transient(root)

        if title:
            self.title(title)

        self.root = root
        self.Competition = Competition
        self.CurName = CurName
        self.SelName = self.CurName
        

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(row = 0, column = 0)

        self.wait_visibility()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (root.winfo_rootx()+50,
                                  root.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master): 

        self.Competition.SortListName()
        
        self.ListBox1 = tk.Listbox(self,width= 40,font=self.BodyFont)
        self.ListBox1.grid(row = 1, column = 0)
        self.ListBox1.bind('<Double-1>', self.SelectSchool)
        
        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.config(command=self.ListBox1.yview)
        scrollbar.grid(row = 1, column = 1)
        self.ListBox1.config(yscrollcommand=scrollbar.set)

        i = 0
        for School in self.Competition.SchoolList:
            self.ListBox1.insert(i,School.Name)
            i = i + 1        
   
       
        tk.Button(self, text="Select", width=10, command=self.SelectSchool,font=self.BodyFont).grid(row=2, column=2 )
        tk.Button(self, text="Cancel", width=10, command=self.cancel,font=self.BodyFont).grid(row=3, column=2 )
        
        self.Competition.SortList()
            
        
            
    def SelectSchool(self,event=None):
        self.SelName = self.ListBox1.get('active') 
        self.ok()    
  
    #
    # standard button semantics

    def ok(self, event=None):
        self.withdraw()
        self.update_idletasks()
        self.leave()
            
    def leave(self):
        self.root.focus_set()
        self.destroy()

            
    def cancel(self, event=None):
        self.SelName = self.CurName
        self.leave()

        
