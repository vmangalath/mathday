import csv
from ..Functions.Functions import NextKey     

class PreviousSchool:
    def __init__(self,Name,Location,HistZScore):
        self.Name = Name
        self.Location = Location
        self.HistZScore = HistZScore
    def __str__(self):
        return "( %s , %s , %s )" %(self.Name,self.Location,self.HistZScore)
    def Register(self,Key):
        return RegisteredSchool(Key,self.Name,self.Location,self.HistZScore)

class RegisteredSchool(PreviousSchool):
    def __init__(self,Key,Name,Location,HistZScore):
        PreviousSchool.__init__(self,Name,Location,HistZScore)
        self.Key = Key
    def __str__(self):
        return "( %s , %s , %s , %s )" %(self.Key,self.Name,self.Location,self.HistZScore)
    def GenerateCompetitionSchool(self,GroupScores,SwissScores,SwissPartners,CrossScores,RelayScores):
        return CompetitionSchool(self.Key,self.Name,self.Location,self.HistZScore,GroupScores,SwissScores,SwissPartners,CrossScores,RelayScores)

class CompetitionSchool(RegisteredSchool):

    def __init__(self,Key,Name,Location,HistZScore,GroupScores,SwissScores,SwissPartners,CrossScores,RelayScores):
        
        RegisteredSchool.__init__(self,Key,Name,Location,HistZScore)
        
        self.GroupScores = GroupScores
        self.SwissScores = SwissScores
        self.CrossScores = CrossScores
        self.RelayScores = RelayScores
        
        self.SwissPartners = SwissPartners
        
        self.Total = sum(self.GroupScores + self.SwissScores + self.CrossScores + self.RelayScores)
        
    def __str__(self):
        return "( %s , %s , %s , %s , %s , %s , %s , %s , %s )" %(self.Key,self.Name,self.Location,self.HistZScore, self.GroupScores, self.SwissScores,self.SwissPartners, self.CrossScores, self.RelayScores)        

    def Listify(self):
        return [self.Key,self.Name,self.Location,self.HistZScore] + self.GroupScores + self.SwissScores + self.SwissPartners + self.CrossScores + self.RelayScores
    
    def TotalUpdate(self,ContestString=['A']):
        self.Total = 0
        for Contest in ContestString:
            
            if(Contest == 'G'):
                self.Total = self.Total + sum(self.GroupScores)
            elif(Contest == 'G1to8'):
                self.Total = self.Total + sum(self.GroupScores[:8])
            elif(Contest == 'S'):
                self.Total = self.Total + sum(self.SwissScores)
            elif(Contest == 'SQ1'):
                self.Total = self.Total + self.SwissScores[0]
            elif(Contest == 'SQ2'):
                self.Total = self.Total + self.SwissScores[1]
            elif(Contest == 'SQ3'):
                self.Total = self.Total + self.SwissScores[2]
            elif(Contest == 'SQ4'):
                self.Total = self.Total + self.SwissScores[3]
            elif(Contest == 'SQ5'):
                self.Total = self.Total + self.SwissScores[4]
            elif(Contest == 'C'):
                self.Total = self.Total + sum(self.CrossScores)
            elif(Contest == 'R'):
                self.Total = self.Total + sum(self.RelayScores)
            elif(Contest == 'A'):
                self.Total = self.Total + sum(self.GroupScores) + sum(self.SwissScores) + sum(self.CrossScores) + sum(self.RelayScores)
                break
                
            

class PreviousSchoolList:
    def __init__(self,SchoolList=[],MasterFile=None):
        self.SchoolList = SchoolList
        self.MasterFile = MasterFile
    def ReadFromFile(self):
        self.SchoolList = []
        with open(self.MasterFile,'r') as file1:
            readfile = csv.reader(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
            j = -1
            for row in readfile:       
                if (j >= 0):
                    SchoolTemp =  PreviousSchool(row[0],row[1],float(row[2]))
                    self.SchoolList.append(SchoolTemp)                        
                j = j + 1 
        self.SortList()
        
    def WriteToFile(self):
        self.SortList()
        with open(self.MasterFile ,'w') as file1:
            writefile = csv.writer(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            writefile.writerow(['Name','Location','Historical Z-Score'])
            for School in self.SchoolList:       
                writefile.writerow([str(School.Name),str(School.Location),str(School.HistZScore)])
    def AddToList(self,School):
        self.SchoolList.append(School)
    def SortList(self):
        #sort the school list by name
        self.SchoolList.sort(key=lambda School: School.Name) 
        
    def PrintList(self):
        print(self.MasterFile)
        for School in self.SchoolList:
            print(School)
    def FindName(self,Name):
        for School in self.SchoolList:
            if(School.Name == Name):
                return School
        return None
    def NameInList(self,Name):
         return len(filter(lambda School: School.Name == Name, self.SchoolList)) != 0


class RegisterSchoolList:
    def __init__(self,SchoolList=[]):
        self.SchoolList = SchoolList
    def AddToList(self,School):
        self.SchoolList.append(School)
    def RemoveFromList(self,School):
        self.SchoolList.remove(School)
    def RemoveFromListKey(self,Key):
        self.RemoveFromList(self.FindKey(Key))
    def SortList(self):
        #sort the school list by name
        self.SchoolList.sort(key=lambda School:  100*ord(School.Key[0]) + int(School.Key[1:])) 
    def PrintList(self):
        for School in self.SchoolList:
            print(School)
    def FindKey(self,Key):
        for School in self.SchoolList:
            if(School.Key == Key):
                return School
        return None
    def KeyInList(self,Key):
         return len(filter(lambda School: School.Key == Key, self.SchoolList)) != 0
    def NameInList(self,Name):
         return len(filter(lambda School: School.Name == Name, self.SchoolList)) != 0
    def ValidKeyOrder(self):
        self.SortList()
        PrevKey = 'A0'
        Result = True
        for School in self.SchoolList:
            Result = Result and NextKey(School.Key,PrevKey)
            PrevKey = School.Key
        return Result
        

class CompetitionSchoolList:
    def __init__(self,SchoolList=[],File=None,MasterDir=None):
        
        self.SchoolList = SchoolList
        self.File = File
        self.MasterDir = MasterDir
        
        self.Contests = ['Group', 'Swiss', 'Cross', 'Relay']
        
        self.ValidGroupScores = []
        self.ValidSwissScores = []
        self.ValidCrossScores = []
        self.ValidRelayScores = []
        self.ValidGroupNames = []
        self.ValidSwissNames = []
        self.ValidCrossNames = []
        self.ValidRelayNames = []
        
        self.ValidScores = [self.ValidGroupScores,self.ValidSwissScores, self.ValidCrossScores, self.ValidRelayScores]
        self.ValidNames = [self.ValidGroupNames,self.ValidSwissNames, self.ValidCrossNames, self.ValidRelayNames]


        self.Result = []
        self.ReadInitFiles()
        
        

    def ReadInitFiles(self):
        for i in range(len(self.Contests)):
            
            FileNameTemp = self.MasterDir + "Scores/" + self.Contests[i] + "ContestScores.csv"         
            with open(FileNameTemp,'r') as file1:
                readfile = csv.reader(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
                j = -1
                for row in readfile:       
                    if (j >= 0):
                        self.ValidNames[i].append(row[0])
                        self.ValidScores[i].append(int(row[1]))                       
                    j = j + 1
        
    def CompeteRegistered(self,RegisteredSchoolList):
        
        RegisteredSchoolList.SortList()
        
        GroupScores = len(self.ValidGroupScores)*[0]
        SwissScores = len(self.ValidSwissScores)*[0]
        CrossScores = len(self.ValidCrossScores)*[0]
        RelayScores = len(self.ValidRelayScores)*[0]
        
        SwissPartners = len(self.ValidSwissScores)*['']
        
        for School in RegisteredSchoolList.SchoolList:
            self.SchoolList.append(School.GenerateCompetitionSchool(GroupScores,SwissScores,SwissPartners,CrossScores,RelayScores))
 
    def SortList(self):
        #sort the school list by name
        self.SchoolList.sort(key=lambda School: 100*ord(School.Key[0]) + int(School.Key[1:]) )  
    
    def WriteToFile(self):
        
        self.SortList()
        with open(self.File ,'w') as file1:
            writefile = csv.writer(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            HeaderList = ['Key','Name','Location','Historical Z-Score']
            for i in range(len(self.ValidNames)):
                for j in range(len(self.ValidNames[i])):
                    nameij = self.Contests[i] + " Q" + str(self.ValidNames[i][j]) + " "
                    HeaderList.append(nameij)
                if(i==1):
                    for j in range(len(self.ValidNames[i])):
                        nameij = self.Contests[i] + " Q" + str(self.ValidNames[i][j]) + " Partner"
                        HeaderList.append(nameij)
                    
            writefile.writerow(HeaderList)
            
            for School in self.SchoolList:
                writefile.writerow(School.Listify())

    def ReadFromFile(self):
        
        #self.SchoolList = []
        
        with open(self.File,'r') as file1:
            readfile = csv.reader(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
            j = -1
            for row in readfile:       
                if (j >= 0):
                    
                    Key = row[0]
                    Name = row[1]
                    Location = row[2]
                    ZScore = float(row[3])
                    
                    AllScores = []
                    ijtot = 4
                    for i in range(len(self.ValidScores)):
                        Scores = []
                        for j in range(len(self.ValidScores[i])):
                            Scores.append(float(row[ijtot]))
                            ijtot = ijtot + 1
                        AllScores.append(Scores)
                        if(i==1):
                            Scores = []
                            for j in range(len(self.ValidScores[i])):
                                Scores.append((row[ijtot]))
                                ijtot = ijtot + 1   
                            AllScores.append(Scores)
                            
                    School = CompetitionSchool(Key,Name,Location,ZScore,AllScores[0],AllScores[1],AllScores[2],AllScores[3],AllScores[4])
                    self.SchoolList.append(School)                   
                j = j + 1 
        self.SortList()
    def FindKey(self,Key):
        for School in self.SchoolList:
            if(School.Key == Key):
                return School
        return None
    def KeyInList(self,Key):
         return len(filter(lambda School: School.Key == Key, self.SchoolList)) != 0
    def NameInList(self,Name):
         return len(filter(lambda School: School.Name == Name, self.SchoolList)) != 0
     
    def PrintList(self):
        for School in self.SchoolList:
            print(School)
    """
    def GenerateScores(self):
        for School in self.SchoolList:
            self.Result.append((School.Key,School.Name))
    """
    
    """    
    def ReadFile(self):
        with open(self.File,'r') as file1:
            readfile = csv.reader(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            j = -1
            for row in readfile:       
                if (j >= 0):
                    
                    School = CompetitionSchool(row[0],row[1],row[2],row[3])
                    
                    AllScores = []
                    rowplace = 4
                    for i in range(len(self.ContestValidMaxScores)):
                        TempScores = []
                        for k in range(len(self.ContestValidMaxScores[i])):
                            TempScores.append(int(row[rowplace]))
                            rowplace = rowplace + 1
                        AllScores.append(TempScores)
                            
                    
                    CurrSchool = School(CurrSchoolKey,CurrSchoolName,CurrSchoolLocation,CurrSchoolHistoricalZScore,AllScores[0],AllScores[1],AllScores[2],AllScores[3])
                        
                    #Validate Here                    
                    self.SchoolDict[CurrSchoolKey] = CurrSchool
                    
            
                j = j + 1
        
    """
            


"""        
class PreviousSchoolList:
    
     
class Competition:
    
    def __init__(self,Directory,MasterLocation):
        
        self.Directory = Directory
        self.FileName = self.Directory + "Competition.csv"
        self.MasterLocation = MasterLocation
        self.Contests = ['Group', 'Swiss', 'Cross', 'Relay']
        self.ContestValidMaxScores = []
        self.SchoolDict = {}
        
        self.ReadInitFiles()
        
        self.ReadFile()
        
    def ReadInitFiles(self):
        
        for ContestName in self.Contests:
            
            FileNameTemp = self.MasterLocation + "Scores/" + ContestName + "ContestScores.csv"
            ContestQuestionNameScoreTemp = []
            
            with open(FileNameTemp,'r') as file1:
                readfile = csv.reader(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
                j = -1
                for row in readfile:       
                    if (j >= 0):
                        ContestQuestionNameScoreTemp.append( (row[0], int(row[1])))                        
                    j = j + 1
            self.ContestValidMaxScores.append(ContestQuestionNameScoreTemp)
            
        
    def ReadFile(self):
        with open(self.FileName,'r') as file1:
            readfile = csv.reader(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            j = -1
            for row in readfile:       
                if (j >= 0):
                    
                    CurrSchoolKey = row[0]
                    CurrSchoolName = row[1]
                    CurrSchoolLocation = row[2]
                    CurrSchoolHistoricalZScore = row[3]
                    
                    AllScores = []
                    rowplace = 4
                    for i in range(len(self.ContestValidMaxScores)):
                        TempScores = []
                        for k in range(len(self.ContestValidMaxScores[i])):
                            TempScores.append(int(row[rowplace]))
                            rowplace = rowplace + 1
                        AllScores.append(TempScores)
                            
                    
                    CurrSchool = School(CurrSchoolKey,CurrSchoolName,CurrSchoolLocation,CurrSchoolHistoricalZScore,AllScores[0],AllScores[1],AllScores[2],AllScores[3])
                        
                    #Validate Here                    
                    self.SchoolDict[CurrSchoolKey] = CurrSchool
                    
            
                j = j + 1
            
    def GenerateFiles(self):
    
    def WriteFile(self):
        
        with open(self.FileName,'w') as file1:
            writefile = csv.writer(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
            writefile.writerow(["School Key","School Name", "Status","Historical Z Score","Score Comp1 Q1","Score Comp1 Q2","Score Comp1 Q3","Score Comp1 Q4","Score Comp1 Q5","Score Comp1 Q6","Score Comp1 Q7","Score Comp1 Q8","Score Comp1 Q9","Score Comp1 Q10", \
    "Score Comp2 Q1","Score Comp2 Q2","Score Comp2 Q3","Score Comp2 Q4","Score Comp2 Q5", \
    "Score Comp3 Q1","Score Comp3 Q2","Score Comp3 Q3","Score Comp3 Q4","Score Comp3 Q5","Score Comp3 Q6","Score Comp3 Q7","Score Comp3 Q8","Score Comp3 Q9","Score Comp3 Q10","Score Comp3 Q11","Score Comp3 Q12","Score Comp3 Q13","Score Comp3 Q14","Score Comp3 Q15","Score Comp3 Q16","Score Comp3 Q17","Score Comp3 Q18","Score Comp3 Q19","Score Comp3 Q20" \
    ])  
                      
            for SchoolKey, School in self.SchoolDict.iteritems():
                GroupScoreStr = map(str, School.GroupScores)
                SwissScoreStr = map(str, School.SwissScores)
                CrossScoreStr = map(str, School.CrossScores)
                rowwrite = [str(School.Key), str(School.Name), str(School.Loc) , str(School.HistZ)  ] + GroupScoreStr + SwissScoreStr + CrossScoreStr
                writefile.writerow(rowwrite)
        
"""
    
