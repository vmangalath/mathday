import csv
import random
import copy
import string
import numpy
import scipy.stats
import subprocess
import os
from ..Functions.Functions import NextKey,ReplaceTemplate     

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
    def GenerateCompetitionSchool(self,GroupScores,SwissScores,CrossScores,RelayScores,SwissPartners,SwissSites):
        return CompetitionSchool(self.Key,self.Name,self.Location,self.HistZScore,GroupScores,SwissScores,CrossScores,RelayScores,SwissPartners,SwissSites)

class CompetitionSchool(RegisteredSchool):

    def __init__(self,Key,Name,Location,HistZScore,GroupScores,SwissScores,CrossScores,RelayScores,SwissPartners,SwissSites):
        
        RegisteredSchool.__init__(self,Key,Name,Location,HistZScore)
        
        self.GroupScores = GroupScores
        self.SwissScores = SwissScores
        self.CrossScores = CrossScores
        self.RelayScores = RelayScores
        
        self.AllScoreDict = {'Group': self.GroupScores, \
                                   'Swiss': self.SwissScores, \
                                   'Cross': self.CrossScores, \
                                   'Relay': self.RelayScores}
        
        self.SwissPartners = SwissPartners
        self.SwissSites = SwissSites
        
        self.Total = sum(self.GroupScores + self.SwissScores + self.CrossScores + self.RelayScores)
        
        
    def __str__(self):
        return "( %s , %s , %s , %s , %s , %s , %s , %s , %s , %s )" %(self.Key,self.Name,self.Location,self.HistZScore, self.GroupScores, self.SwissScores, self.CrossScores, self.RelayScores,self.SwissPartners,self.SwissSites)        

    def Listify(self):
        return [self.Key,self.Name,self.Location,self.HistZScore] + self.GroupScores + self.SwissScores + self.CrossScores + self.RelayScores + self.SwissPartners + self.SwissSites
    
    def AllZerosScores(self,ContestName):        
        return all(x == 0 for x in self.AllScoreDict[ContestName])
   
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
            
    def WriteReport(self,TemplateFile,SchoolFile):
        
        #Generate Dictionary for Value Names and Values
        AllOutputNames = {
                            'SchoolName' : self.Name,\
                            'SchoolLocation' : self.Location,\
                            'SchoolTotal' : str(self.Total)}
        
        for ContestKey in self.AllScoreDict:
            for i in range(len(self.AllScoreDict[ContestKey])):
                NewKey = 'School'+ContestKey  + 'Q'+ str(i+1) 
                
                AllOutputNames[NewKey] = str(self.AllScoreDict[ContestKey][i])
                
            NewKey = 'School'+ContestKey  + 'Total' 
            AllOutputNames[NewKey] = str(sum(self.AllScoreDict[ContestKey]))
            
        ReplaceTemplate(TemplateFile,SchoolFile,AllOutputNames)
            
            
            
class SwissPair:
    def __init__(self,Site,School1Key, School2Key):
        self.Site = Site
        self.School1Key = School1Key
        self.School2Key = School2Key
    def SchoolKeyInPair(self,Key):
        return (self.School1Key == Key) or (self.School2Key == Key)  
    def __str__(self):
        return "( %s , %s , %s)" %(self.Site,self.School1Key,self.School2Key)     

                        
class ListOfSwissPairs:
    def __init__(self,SwissPairsList =[]):
        self.SwissPairsList = SwissPairsList
        
    def SchoolPaired(self,Key):
        Result = False
        for SwissPairInst in self.SwissPairsList:   
            if SwissPairInst.SchoolKeyInPair(Key):
                Result=True
                break
        return Result
    
    def PrintList(self):
        for SwissPair in self.SwissPairsList:
            print(SwissPair)
            
        


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

    def FindName(self,Name):
        for School in self.SchoolList:
            if(School.Name == Name):
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
    def __init__(self,SchoolList=[],File=None,MasterDir=None,DataDir=None):
        
        self.SchoolList = SchoolList
        self.File = File
        self.MasterDir = MasterDir
        self.DataDir = DataDir
        
        self.CompDataDir = os.path.join(os.path.split(self.File)[0], '')
        
        self.CompName = os.path.split(os.path.split(self.File)[0])[1]
        
        self.FinalReportsDir = os.path.join(self.CompDataDir,'FinalReports')
                
        if (not os.path.exists(self.FinalReportsDir)):
            os.makedirs(self.FinalReportsDir)
        
        self.Contests = ['Group', 'Swiss', 'Cross', 'Relay']
        
        self.ValidGroupScores = []
        self.ValidSwissScores = []
        self.ValidCrossScores = []
        self.ValidRelayScores = []
        self.ValidGroupNames = []
        self.ValidSwissNames = []
        self.ValidCrossNames = []
        self.ValidRelayNames = []
        
        
        self.ValidNameScoreDict = {'Group': (self.ValidGroupNames, self.ValidGroupScores), \
                                   'Swiss': (self.ValidSwissNames, self.ValidSwissScores), \
                                   'Cross': (self.ValidCrossNames, self.ValidCrossScores), \
                                   'Relay': (self.ValidRelayNames, self.ValidRelayScores)}
        
        self.ValidSwissSites = []
        
        self.KeyLetterListCondensed = []
        self.SwissSitesLetterCondensed = []


        self.Result = []
        self.ReadInitFiles()
        
        

    def ReadInitFiles(self):
        for i in range(len(self.Contests)):
            
            FileNameTemp = os.path.join( self.MasterDir, "Scores",self.Contests[i]+"ContestScores.csv"         )
            with open(FileNameTemp,'r') as file1:
                readfile = csv.reader(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
                j = -1
                for row in readfile:       
                    if (j >= 0):
                        self.ValidNameScoreDict[self.Contests[i]][0].append(row[0])
                        self.ValidNameScoreDict[self.Contests[i]][1].append(int(row[1]))                     
                    j = j + 1
        
    def CompeteRegistered(self,RegisteredSchoolList):
        
        RegisteredSchoolList.SortList()
        
        
        for School in RegisteredSchoolList.SchoolList:
            
            GroupScores = len(self.ValidGroupScores)*[0]
            SwissScores = len(self.ValidSwissScores)*[0]
            CrossScores = len(self.ValidCrossScores)*[0]
            RelayScores = len(self.ValidRelayScores)*[0]
            
            SwissPartners = len(self.ValidSwissScores)*['']
            SwissSites = len(self.ValidSwissScores)*['']
        
            self.SchoolList.append(School.GenerateCompetitionSchool(GroupScores,SwissScores,CrossScores,RelayScores,SwissPartners,SwissSites))
 
    def SortList(self):
        #sort the school list by name
        self.SchoolList.sort(key=lambda School: 100*ord(School.Key[0]) + int(School.Key[1:]) )  

    def SortListName(self):
        #sort the school list by name
        self.SchoolList.sort(key=lambda School: School.Name )  
        
    def SortListScores(self):
        self.SchoolList.sort(key=lambda School: School.Total, reverse=True )  
        
    def ClearAllSwiss(self,RoundNum='1'):
        #RoundNums from 1 to 5        
        
        for School in self.SchoolList:
            School.SwissPartners[RoundNum -1] = ''
            School.SwissSites[RoundNum -1] = ''
            School.SwissScores[RoundNum-1]= 0
    
    
    def WriteToFile(self):
        
        self.SortList()
        
        with open(self.File ,'w') as file1:
            writefile = csv.writer(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            HeaderList = ['Key','Name','Location','Historical Z-Score']
            
            #Maintains the order, as dictionaries are unordered
            for DictKey in self.Contests:
                
                for j in range(len(self.ValidNameScoreDict[DictKey][0])):
                    nameij = DictKey + self.ValidNameScoreDict[DictKey][0][j] + " "
                    HeaderList.append(nameij)
                        
            #SwissAdminStuff
            #Partners
            DictKey = 'Swiss'
            for j in range(len(self.ValidNameScoreDict[DictKey][0])):
                nameij = DictKey +  self.ValidNameScoreDict[DictKey][0][j] + " Partner"
                HeaderList.append(nameij)
            
            #Swiss Sites
            for j in range(len(self.ValidNameScoreDict[DictKey][0])):
                nameij = DictKey + self.ValidNameScoreDict[DictKey][0][j] + " Sites"
                HeaderList.append(nameij)
                    
            writefile.writerow(HeaderList)
            
            for School in self.SchoolList:
                writefile.writerow(School.Listify())

    def ReadFromFile(self):
        
        self.SchoolList = []
        
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
                    for DictKey in self.Contests:
                        Scores = []
                        for j in range(len(self.ValidNameScoreDict[DictKey][1])):
                            Scores.append(int(row[ijtot]))
                            ijtot = ijtot + 1
                        AllScores.append(Scores)
                    
                    #Read Swiss Partners and Sites
                    for i in range(2):
                            Scores = []
                            for j in range(len(self.ValidNameScoreDict['Swiss'][1])):
                                Scores.append((row[ijtot]))
                                ijtot = ijtot + 1   
                            AllScores.append(Scores)
                            
                    School = CompetitionSchool(Key,Name,Location,ZScore,AllScores[0],AllScores[1],AllScores[2],AllScores[3],AllScores[4],AllScores[5])
                    self.SchoolList.append(School)    
                    
                j = j + 1 
        self.SortList()
        self.PossibleSwissSites()
        self.HowManyLettersInKeys()
        self.HowManyLettersInSites()
        
    def FindKey(self,Key):
        for School in self.SchoolList:
            if(School.Key == Key):
                return School
        return None
        
    def FindName(self,Name):
        for School in self.SchoolList:
            if(School.Name == Name):
                return School
        return None

        
    def KeyInList(self,Key):
         return len(filter(lambda School: School.Key == Key, self.SchoolList)) != 0
         
    def NameInList(self,Name):
         return len(filter(lambda School: School.Name == Name, self.SchoolList)) != 0
         
    def AllZerosScores(self,Key,ContestName,IsSiteKey=False,RoundNum=1):
        if ContestName == 'Swiss':
            if IsSiteKey:
                #Find site
                SwissPartners = self.FindSwissSite(RoundNum,Key)
                return (SwissPartners[0].SwissScores[RoundNum -1] == 0) and (SwissPartners[1].SwissScores[RoundNum -1] == 0)
                
            else:
                SiteKey = self.FindSwissSiteBySchool(RoundNum,Key)
                SwissPartners = self.FindSwissSite(RoundNum,SiteKey)
                return (SwissPartners[0].SwissScores[RoundNum -1] == 0) and (SwissPartners[1].SwissScores[RoundNum -1] == 0)
                
        else:
            School = self.FindKey(Key)
            return School.AllZerosScores(ContestName)
            

    def HowManyLettersInKeys(self):
        self.KeyLetterListCondensed = []
        for Letter in string.ascii_uppercase:
            Count = 0
            for School in self.SchoolList:
                
                if Letter in School.Key:
                    Count = Count +1
                    
            if (Count > 0):
                self.KeyLetterListCondensed.append((Letter,Count))
     
    def PrintList(self):
        for School in self.SchoolList:
            print(School)
            
    def PossibleSwissSites(self):
        self.SortList()
        self.ValidSwissSites = []
        for i in range(0,len(self.SchoolList),2):
            self.ValidSwissSites.append(self.SchoolList[i].Key)
    
    def HowManyLettersInSites(self):
        self.SwissSitesLetterCondensed = []
        for Letter in string.ascii_uppercase:
            Count = 0
            for Site in self.ValidSwissSites:
                
                if Letter in Site:
                    Count = Count +1
                    
            if (Count > 0):
                self.SwissSitesLetterCondensed.append((Letter,Count))    
     
    def UpdateTotalsSchool(self,ContestString=['A']):
        
        for School in self.SchoolList:
            School.TotalUpdate(ContestString)
    
    def FindSwissSite(self,RoundNum,Site):
        return filter(lambda School: School.SwissSites[RoundNum-1] == Site, self.SchoolList)
        
    def FindSwissSiteBySchool(self,RoundNum,SchoolKey):
        School = self.FindKey(SchoolKey)
        return School.SwissSites[RoundNum - 1]

        
    def GetSwissPartnersBySite(self,RoundNum):
        SwissSites = []
        for Site in self.ValidSwissSites:
            Schools = self.FindSwissSite(RoundNum,Site)
            SwissSites.append((Site,Schools))
        return SwissSites
    
    def PrintSwissPartners(self,RoundNum):
        
        SwissSites = self.GetSwissPartnersBySite(RoundNum)
        
        SwissSitesDir = os.path.join(self.CompDataDir,'SwissSites')
        
        if (not os.path.exists(SwissSitesDir)):
            os.makedirs(SwissSitesDir)
        
        FileName = os.path.join(SwissSitesDir,"SwissRound" + str(RoundNum)+ ".csv")        
        
        with open(FileName ,'w') as file1:
            writefile = csv.writer(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            writefile.writerow(['Round ' + str(RoundNum),'',''])
            writefile.writerow(['','',''])
            writefile.writerow(['Site','School Keys','School Names'])
            
            for Site in SwissSites:
                writefile.writerow([str(Site[0]),str(Site[1][0].Key),str(Site[1][0].Name)])
                writefile.writerow(['',str(Site[1][1].Key),str(Site[1][1].Name)])
                writefile.writerow(['','',''])

        
        
    def GenerateSwissPartners(self,RoundNum):
        
        #Clear Previous Swiss Data
        self.ClearAllSwiss(RoundNum)
        
        #Take Group Scores 1 through 8
        ContestString = ['G1to8']
        
        
        for i in range(RoundNum -2):
            RoundString = 'SQ' + str(i+1)
            ContestString.append(RoundString)
            
        #print(ContestString)
        
        #Update Totals
        self.UpdateTotalsSchool(ContestString)
        
        #Sort SchoolList in Score order (Descending)
        self.SortListScores()
        
        SwissPairsListInst = ListOfSwissPairs([])
        
        SwissSites = copy.deepcopy(self.ValidSwissSites)
        
        #Find Partners
        for School in self.SchoolList:
                            
                for i in range(len(School.SwissPartners)):
                    if ( not SwissPairsListInst.SchoolPaired(School.Key)):
                
                        for SchoolPartner in self.SchoolList:
                            
                            if (SchoolPartner != School and (not SwissPairsListInst.SchoolPaired(SchoolPartner.Key)) and SchoolPartner.Key not in School.SwissPartners[i:]):
                                SiteKey = random.choice(SwissSites)
                                SwissSites.remove(SiteKey)
                                SwissPairsListInst.SwissPairsList.append(SwissPair(SiteKey,School.Key,SchoolPartner.Key))
                                break

        
        #Generated SwissPartnerList
        #Now Update Competition Information
        for SwissPairx in SwissPairsListInst.SwissPairsList:
            School1 = self.FindKey(SwissPairx.School1Key)
            
            School1.SwissPartners[RoundNum -1] = SwissPairx.School2Key
            School1.SwissSites[RoundNum -1] = SwissPairx.Site
            
            School2 = self.FindKey(SwissPairx.School2Key)
            
            School2.SwissPartners[RoundNum -1] = SwissPairx.School1Key
            School2.SwissSites[RoundNum -1] = SwissPairx.Site
        
        #Swiss Competition Now Generated
        #write to file
        self.WriteToFile()
        

    def PrintFinal(self):
        print('Final')
        
        #Get School Totals and put in rank order
        self.UpdateTotalsSchool(['A'])    
        self.SortListScores()
        
        #Get Statistics
        
        #Get Scores
        Scores = []
        for School in self.SchoolList:
            print(School.Name)
            Scores.append(School.Total)
            
        ScoreMean = numpy.mean(Scores)
        ScoreStd = numpy.std(Scores)
        ZScores = scipy.stats.zscore(Scores)
        
        #Update Master File
        self.UpdateMasterFile(ZScores)
            
        SchoolReportDir = os.path.join(self.FinalReportsDir, 'IndividualSchoolReports')
            
        if (not os.path.exists(SchoolReportDir)):
            os.makedirs(SchoolReportDir)
        
        with  open(os.devnull, 'w') as DevNullFile:
            #Generate Individual School Report
            for School in self.SchoolList:
                #Template File = 
                TemplateFile = os.path.join(self.MasterDir,'ReportTemplates','Individual','IndividulSchoolTemplate.tex')
            
                
                
                RawSchoolFile = os.path.join(SchoolReportDir, School.Name.replace(' ','') + '.tex')
                
                #Makes Report
                School.WriteReport(TemplateFile,RawSchoolFile)
                
                #Compile it
                CallString = "pdflatex " + School.Name.replace(' ','') + '.tex'
                subprocess.call(CallString, shell=True,cwd=SchoolReportDir,stdout=DevNullFile)  

            
        #Remove unneccessary files
        AllFilesInDir = os.listdir(SchoolReportDir)
        for File in AllFilesInDir:
            if not File.endswith(".pdf"):
                os.remove(os.path.join(SchoolReportDir, File))

        
        #Print Final Results
        self.PrintOverall()
        
            
    def GetTop10(self,Location):
        self.UpdateTotalsSchool(['A'])
        self.SortListScores()
        
        if (Location == 'City' or Location == 'Country'):
            return filter(lambda School: School.Location == Location, self.SchoolList)[:10]
        else:
            return self.SchoolList[:10]
    
    def PrintOverall(self):
        
        OverallReportsDir = os.path.join(self.FinalReportsDir, 'OverallReports')
            
        if (not os.path.exists(OverallReportsDir)):
            os.makedirs(OverallReportsDir)
                

        TemplateFile = os.path.join(self.MasterDir,'ReportTemplates','Final','FinalTemplate.tex')
        OverallFile = os.path.join(OverallReportsDir, 'OverallRankingTop10.tex')
        
        Top10Lists = ['Top','Country']
        
        AllOutputNames = {'ContestName': self.CompName }
            
        
        for Lists in Top10Lists:
            
            ListResult = self.GetTop10(Lists)
            if (len(ListResult) < 10):
                ListResult = ListResult + (10 - len(ListResult))*['\\textcolor{white}{a}']
                
            for i in range(len(ListResult)):
                NewKey = 'School' + Lists + str(i + 1)
                
                if ( isinstance(ListResult[i] , CompetitionSchool)):
                    AllOutputNames[NewKey] = ListResult[i].Name[:40]
                else:
                    AllOutputNames[NewKey] =  ListResult[i]
                    
            if Lists == 'Top':
                for i in range(3):
                    NewKey = 'School' + Lists + str(i + 1) + 'Score'
                
                    if ( isinstance(ListResult[i] , CompetitionSchool)):
                        AllOutputNames[NewKey] = str(ListResult[i].Total)
                    else:
                        AllOutputNames[NewKey] =  ListResult[i]

        ReplaceTemplate(TemplateFile,OverallFile,AllOutputNames)
        
        with  open(os.devnull, 'w') as DevNullFile:
            CallString = "pdflatex " + 'OverallRankingTop10.tex'
            subprocess.call(CallString, shell=True,cwd=OverallReportsDir,stdout=DevNullFile)  

            
        #Remove unneccessary files
        AllFilesInDir = os.listdir(OverallReportsDir)
        for File in AllFilesInDir:
            if not File.endswith(".pdf"):
                os.remove(os.path.join(OverallReportsDir, File))
        
    def UpdateMasterFile(self,ZScoreList):
        MasterFile = os.path.join(self.MasterDir,'Schools.csv')
        OldMaster = PreviousSchoolList(MasterFile=MasterFile)
        
        #Read it in
        OldMaster.ReadFromFile()
        
        #Update
        for i in range(len(self.SchoolList)):
            
            School = OldMaster.FindName(self.SchoolList[i].Name)
            
            if (School == None):
                NewSchool = PreviousSchool(self.SchoolList[i].Name,self.SchoolList[i].Location,ZScoreList[i])
                OldMaster.SchoolList.append(NewSchool)
            else:
                School.HistZScore = ZScoreList[i]
                
        OldMaster.SortList()
        OldMaster.WriteToFile()
        
        #Write out
        
        

        
            
    """    
    def PrintFinal(self):
        print('Final')
        TotalRankings = self.TotalRankingsAndZScore()
        print(TotalRankings)
        
    def TotalRankingsAndZScore(self):
        
        #Get school totals
        self.UpdateTotalsSchool(['A'])
        
        #Order SchoolList by Scores
        self.SortListScores()
        
        #Get Mean and Standarddeviation
        
        ScoreRankings = []
        for School in self.SchoolList:
            ScoreRankings.append(School.Total)
            
        ScoreMean = numpy.mean(ScoreRankings)
        ScoreStd = numpy.std(ScoreRankings)
        
        TotalRankings = []
        i = 1
        
        for School in self.SchoolList:
            ZScore = (School.Total - ScoreMean)/ScoreStd
            TotalRankings.append((i,School.Name,School.Total,School.HistZScore,ZScore))
            i = i +1
        return TotalRankings
    """
        
        
        
