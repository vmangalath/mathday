#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
--- All Non-GUI Classes ---

    These classes are used by the GUI calls to perform the real work of the program

"""

######--IMPORTS--######
import csv
import numpy as np
from Lib.Functions.Functions import NextKey, ReplaceTemplate, IsKey


"""
    Individual School Classes

"""

class PreviousSchool:
    """Class for storing information about a school from previous competitions."""
    def __init__(self, Name, Location, HistZScore):
        #PreviousSchool is an object linking 3 variables
        #   Name - Name of the School
        #   Location - Location of the School ('City' or 'Country')
        #   HistZScore - Previous Z Score result
        self.Name = Name
        self.Location = Location
        self.HistZScore = float(HistZScore)

    #When converted to a string it is just a tuple containing its 3 values
    def __str__(self):
        return f"{self.Name} ({self.Location})"

    #Registers the current school given a 'Key'
    def Register(self, Key):
        """Register the school for a competition."""
        return RegisteredSchool(self.Name, self.Location, self.HistZScore, Key)

class RegisteredSchool(PreviousSchool):
    """Class for storing information about a school registered for a competition."""
    def __init__(self, Name, Location, HistZScore, Key):
        #RegisteredSchool is a PreviousSchool with an extra variable
        #   Key - Key of the School for the Competition (e.g 'A1' is a key), these are unique for each team in a competition
        super().__init__(Name, Location, HistZScore)
        self.Key = Key

    def __str__(self):
        return f"( {self.Key} , {self.Name} , {self.Location} , {self.HistZScore} )"

    #Enters the current School into the Competition, making it a CompetitionSchool
    def GenerateCompetitionSchool(self, GroupScores, SwissScores, CrossScores, RelayScores, SwissPartners, SwissSites):
        return CompetitionSchool(self.Key, self.Name, self.Location, self.HistZScore, 
                               GroupScores, SwissScores, CrossScores, RelayScores, 
                               SwissPartners, SwissSites)

class CompetitionSchool(RegisteredSchool):
    """Class for storing information about a school during a competition."""
    def __init__(self, Key, Name, Location, HistZScore, GroupScores, SwissScores, 
                 CrossScores, RelayScores, SwissPartners, SwissSites):
        #CompetitionSchool is a RegisteredSchool with extra variables
        # GroupScores - A list containing all the Scores for the Group Contest
        # SwissScores - A list containing all the Scores for the Swiss Contest
        # CrossScores - A list containing all the Scores for the Cross Contest
        # RelayScores - A list containing all the Scores for the Relay Contest
        # AllScoreDict - A dictionary with the Contest names as keys and the values as the appropriate Score list
        # SwissPartners - A list of the Schools Swiss Partners of all rounds
        # SwissSites - A list of the Schools Swiss Sites for all rounds
        # Total - a variable that gives the current Score of the School
        super().__init__(Name, Location, HistZScore, Key)

        self.GroupScores = GroupScores
        self.SwissScores = SwissScores
        self.CrossScores = CrossScores
        self.RelayScores = RelayScores

        self.AllScoreDict = {
            'Group': self.GroupScores,
            'Swiss': self.SwissScores,
            'Cross': self.CrossScores,
            'Relay': self.RelayScores
        }

        self.SwissPartners = SwissPartners
        self.SwissSites = SwissSites

        self.Total = sum(self.GroupScores + self.SwissScores + self.CrossScores + self.RelayScores)

    def __str__(self):
        return f"( {self.Key} , {self.Name} , {self.Location} , {self.HistZScore} , {self.GroupScores} , {self.SwissScores} , {self.CrossScores} , {self.RelayScores} , {self.SwissPartners} , {self.SwissSites} )"

    #Produces a list version of the Schools values
    def Listify(self):
        return [self.Key, self.Name, self.Location, self.HistZScore] + \
               self.GroupScores + self.SwissScores + self.CrossScores + \
               self.RelayScores + self.SwissPartners + self.SwissSites

    #checks if all the scores for a given contest are zero
    def AllZerosScores(self, ContestName):
        return all(x == 0 for x in self.AllScoreDict[ContestName])

    #Updates the Total variable for a given number of contests
    def TotalUpdate(self, ContestString=['A']):
        #reset the Total value
        self.Total = 0

        #ContestString is a list of strings that determine what contest totals
        #contribute to the Total

        # 'G' - All Group Questions
        # 'G1to8' - Group Questions 1 through 8
        # 'S' - All Swiss Rounds
        # 'SQ<Number>' - <Number> Swiss Round
        # 'C' - All Cross Questions
        # 'R' - All Relay Questions
        # 'A' - All Questions (Overall Total)
        for Contest in ContestString:
            if Contest == 'G':
                self.Total += sum(self.GroupScores)
            elif Contest == 'G1to8':
                self.Total += sum(self.GroupScores[:8])
            elif Contest == 'S':
                self.Total += sum(self.SwissScores)
            elif Contest == 'SQ1':
                self.Total += self.SwissScores[0]
            elif Contest == 'SQ2':
                self.Total += self.SwissScores[1]
            elif Contest == 'SQ3':
                self.Total += self.SwissScores[2]
            elif Contest == 'SQ4':
                self.Total += self.SwissScores[3]
            elif Contest == 'SQ5':
                self.Total += self.SwissScores[4]
            elif Contest == 'C':
                #self.CrossScores is just the number of ticks, the actual score 4 times the number of ticks
                self.Total += 4 * sum(self.CrossScores)
            elif Contest == 'R':
                self.Total += sum(self.RelayScores)
            elif Contest == 'A':
                #self.CrossScores is just the number of ticks, the actual score 4 times the number of ticks
                self.Total = sum(self.GroupScores) + sum(self.SwissScores) + \
                            4 * sum(self.CrossScores) + sum(self.RelayScores)
                break

    #Writes a Schools Report for the Competition
    def WriteReport(self, TemplateFile, SchoolFile):
        #Uses ReplaceTemplate defined in Functions.py

        #Generate Dictionary for Value Names and Values
        AllOutputNames = {
            'SchoolName': self.Name,
            'SchoolLocation': self.Location,
            'SchoolTotal': str(self.Total)
        }

        for ContestKey in self.AllScoreDict:
            for i in range(len(self.AllScoreDict[ContestKey])):
                NewKey = f'School{ContestKey}Q{i+1}'
                AllOutputNames[NewKey] = str(self.AllScoreDict[ContestKey][i])

            NewKey = f'School{ContestKey}Total'

            if ContestKey == 'Cross':
                #Cross final scores multiplies by 4
                AllOutputNames[NewKey] = str(4 * sum(self.AllScoreDict[ContestKey]))
            else:
                AllOutputNames[NewKey] = str(sum(self.AllScoreDict[ContestKey]))

        #Write File
        ReplaceTemplate(TemplateFile, SchoolFile, AllOutputNames)

    def UpdateTotalScore(self):
        """Update the total score for the school."""
        self.Total = sum(self.GroupScores + self.SwissScores + self.CrossScores + self.RelayScores)

    def UpdateZScore(self, Mean, Std):
        """Update the Z-score for the school."""
        if Std == 0:
            self.ZScore = 0
        else:
            self.ZScore = (self.Total - Mean) / Std

class SwissPair:
    """Class for storing information about a pair of schools in a Swiss round."""
    def __init__(self, Site, School1Key, School2Key):
        self.Site = Site
        self.School1Key = School1Key
        self.School2Key = School2Key

    def SchoolKeyInPair(self, Key):
        return (self.School1Key == Key) or (self.School2Key == Key)

    def __str__(self):
        return f"( {self.Site} , {self.School1Key} , {self.School2Key} )"

class ListOfSwissPairs:
    """Class for storing a list of Swiss pairs."""
    def __init__(self):
        self.Pairs = []

    def AddPair(self, Pair):
        """Add a pair to the list."""
        self.Pairs.append(Pair)

    def GetPairs(self):
        """Get the list of pairs."""
        return self.Pairs

class PreviousSchoolList:
    """Class for storing a list of schools from previous competitions."""
    def __init__(self, SchoolList=[], MasterFile=None):
        self.SchoolList = SchoolList
        self.MasterFile = MasterFile

    def ReadFromFile(self):
        self.SchoolList = []
        with open(self.MasterFile, 'r', newline='') as file1:
            readfile = csv.reader(file1, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            next(readfile)  # Skip header
            for row in readfile:
                SchoolTemp = PreviousSchool(row[0], row[1], float(row[2]))
                self.SchoolList.append(SchoolTemp)
        self.SortList()

    def WriteToFile(self):
        self.SortList()
        with open(self.MasterFile, 'w', newline='') as file1:
            writefile = csv.writer(file1, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writefile.writerow(['Name', 'Location', 'Historical Z-Score'])
            for School in self.SchoolList:
                writefile.writerow([str(School.Name), str(School.Location), str(School.HistZScore)])

    def AddToList(self, School):
        """Add a school to the list."""
        self.SchoolList.append(School)

    def SortList(self):
        #sort the school list by name
        self.SchoolList.sort(key=lambda School: School.Name)

    def PrintList(self):
        print(self.MasterFile)
        for School in self.SchoolList:
            print(School)

    def FindName(self, Name):
        """Find a school by name."""
        for School in self.SchoolList:
            if School.Name == Name:
                return School
        return None

    def NameInList(self, Name):
        return any(School.Name == Name for School in self.SchoolList)

class RegisterSchoolList:
    """Class for storing a list of schools registered for a competition."""
    def __init__(self, SchoolList=[]):
        self.SchoolList = SchoolList

    def AddToList(self, School):
        """Add a school to the list."""
        self.SchoolList.append(School)

    def RemoveFromList(self, School):
        """Remove a school from the list."""
        self.SchoolList.remove(School)

    def RemoveFromListKey(self, Key):
        """Remove a school from the list by key."""
        self.SchoolList = [School for School in self.SchoolList if School.Key != Key]

    def SortList(self):
        #sort the school list by name
        self.SchoolList.sort(key=lambda School: School.Name)

    def PrintList(self):
        for School in self.SchoolList:
            print(School)

    def FindKey(self, Key):
        """Find a school by key."""
        for School in self.SchoolList:
            if School.Key == Key:
                return School
        return None

    def FindName(self, Name):
        for School in self.SchoolList:
            if School.Name == Name:
                return School
        return None

    def KeyInList(self, Key):
        return any(School.Key == Key for School in self.SchoolList)

    def NameInList(self, Name):
        return any(School.Name == Name for School in self.SchoolList)

    def ValidKey(self, Key):
        """Check if a key is valid."""
        return IsKey(Key)

    def ValidKeyOrder(self):
        """Check if the keys are in a valid order"""
        #Keys should be in the form of a letter followed by a number
        #e.g. A1, A2, B1, B2, etc.
        for School in self.SchoolList:
            if not self.ValidKey(School.Key):
                return False
        return True

class CompetitionSchoolList:
    """Class for storing a list of schools during a competition."""
    def __init__(self, SchoolList=[], File=None, MasterDir=None, DataDir=None):
        self.SchoolList = SchoolList
        self.File = File
        self.MasterDir = MasterDir
        self.DataDir = DataDir

    def ReadInitFiles(self):
        #Read the initial files for the competition
        #This includes the competition file and the master file
        self.ReadFromFile()
        self.UpdateTotalsSchool()

    def CompeteRegistered(self, RegisteredSchoolList):
        #Convert the registered schools to competition schools
        self.SchoolList = []
        for School in RegisteredSchoolList.SchoolList:
            CompetitionSchoolTemp = School.GenerateCompetitionSchool(
                [0] * 10,  # GroupScores
                [0] * 5,   # SwissScores
                [0] * 10,  # CrossScores
                [0] * 5,   # RelayScores
                [''] * 5,  # SwissPartners
                [''] * 5   # SwissSites
            )
            self.SchoolList.append(CompetitionSchoolTemp)

    def SortList(self):
        #sort the school list by name
        self.SchoolList.sort(key=lambda School: School.Name)

    def SortListName(self):
        #sort the school list by name
        self.SchoolList.sort(key=lambda School: School.Name)

    def SortListScores(self):
        #sort the school list by total score
        self.SchoolList.sort(key=lambda School: School.Total, reverse=True)

    def ClearAllSwiss(self, RoundNum='1'):
        #RoundNums from 1 to 5
        for School in self.SchoolList:
            School.SwissScores[int(RoundNum) - 1] = 0
            School.SwissPartners[int(RoundNum) - 1] = ''
            School.SwissSites[int(RoundNum) - 1] = ''

    def WriteToFile(self):
        with open(self.File, 'w', newline='') as file1:
            writefile = csv.writer(file1, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #Write header
            Header = ['Key', 'Name', 'Location', 'HistZScore']
            Header += ['Group' + str(i+1) for i in range(10)]
            Header += ['Swiss' + str(i+1) for i in range(5)]
            Header += ['Cross' + str(i+1) for i in range(10)]
            Header += ['Relay' + str(i+1) for i in range(5)]
            Header += ['SwissPartner' + str(i+1) for i in range(5)]
            Header += ['SwissSite' + str(i+1) for i in range(5)]
            writefile.writerow(Header)
            #Write data
            for School in self.SchoolList:
                writefile.writerow(School.Listify())

    def ReadFromFile(self):
        with open(self.File, 'r', newline='') as file1:
            readfile = csv.reader(file1, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            Header = next(readfile)
            self.SchoolList = []
            for row in readfile:
                Key = row[0]
                Name = row[1]
                Location = row[2]
                HistZScore = float(row[3])
                GroupScores = [int(x) for x in row[4:14]]
                SwissScores = [int(x) for x in row[14:19]]
                CrossScores = [int(x) for x in row[19:29]]
                RelayScores = [int(x) for x in row[29:34]]
                SwissPartners = row[34:39]
                SwissSites = row[39:44]
                CompetitionSchoolTemp = CompetitionSchool(
                    Key, Name, Location, HistZScore,
                    GroupScores, SwissScores, CrossScores, RelayScores,
                    SwissPartners, SwissSites
                )
                self.SchoolList.append(CompetitionSchoolTemp)

    def FindKey(self, Key):
        for School in self.SchoolList:
            if School.Key == Key:
                return School
        return None

    def FindName(self, Name):
        for School in self.SchoolList:
            if School.Name == Name:
                return School
        return None

    def KeyInList(self, Key):
        return any(School.Key == Key for School in self.SchoolList)

    def NameInList(self, Name):
        return any(School.Name == Name for School in self.SchoolList)

    def AllZerosScores(self, Key, ContestName, IsSiteKey=False, RoundNum=1):
        School = self.FindKey(Key)
        if School is None:
            return True
        if ContestName == 'Swiss':
            if IsSiteKey:
                return School.SwissSites[RoundNum - 1] == ''
            else:
                return School.SwissScores[RoundNum - 1] == 0
        else:
            return School.AllZerosScores(ContestName)

    def HowManyLettersInKeys(self):
        #Count how many different letters are used in the keys
        Letters = set()
        for School in self.SchoolList:
            Letters.add(School.Key[0])
        return len(Letters)

    def PrintList(self):
        for School in self.SchoolList:
            print(School)

    def PossibleSwissSites(self):
        #Get all possible Swiss sites
        Sites = set()
        for School in self.SchoolList:
            for Site in School.SwissSites:
                if Site != '':
                    Sites.add(Site)
        return sorted(list(Sites))

    def HowManyLettersInSites(self):
        #Count how many different letters are used in the sites
        Letters = set()
        for School in self.SchoolList:
            for Site in School.SwissSites:
                if Site != '':
                    Letters.add(Site[0])
        return len(Letters)

    def UpdateTotalsSchool(self):
        """Update total scores for all schools."""
        for School in self.SchoolList:
            School.TotalUpdate()

        # Calculate mean and standard deviation
        Scores = [School.Total for School in self.SchoolList]
        Mean = np.mean(Scores)
        Std = np.std(Scores)

        # Update Z-scores
        for School in self.SchoolList:
            School.UpdateZScore(Mean, Std)

    def FindSwissSite(self, RoundNum, Site):
        """Find schools in a Swiss round at a specific site."""
        Schools = []
        for School in self.SchoolList:
            if School.SwissSites[RoundNum - 1] == Site:
                Schools.append(School)
        return Schools

    def FindSwissSiteBySchool(self, RoundNum, SchoolKey):
        School = self.FindKey(SchoolKey)
        if School is None:
            return None
        return School.SwissSites[RoundNum - 1]

    def GetSwissPartnersBySite(self, RoundNum):
        #Get all Swiss partners for a given round
        Partners = []
        for School in self.SchoolList:
            if School.SwissPartners[RoundNum - 1] != '':
                Partners.append((School.Key, School.SwissPartners[RoundNum - 1]))
        return Partners

    def PrintSwissPartnersCSV(self, RoundNum):
        """Print Swiss round pairings to a CSV file."""
        Pairs = self.GenerateSwissPartners(RoundNum)
        FileName = f"{self.DataDir}SwissRound{RoundNum}.csv"

        with open(FileName, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['School1', 'School2'])
            for Pair in Pairs.GetPairs():
                writer.writerow([Pair.School1.Key, Pair.School2.Key])

    def PrintSwissPartners(self, RoundNum):
        """Print Swiss round pairings to a text file."""
        Pairs = self.GenerateSwissPartners(RoundNum)
        FileName = f"{self.DataDir}SwissRound{RoundNum}.txt"

        with open(FileName, 'w', encoding='utf-8') as f:
            f.write(f"Swiss Round {RoundNum} Pairings\n")
            f.write("=" * 40 + "\n\n")
            for Pair in Pairs.GetPairs():
                f.write(f"{Pair.School1.Key} vs {Pair.School2.Key}\n")
                f.write(f"{Pair.School1.Name} vs {Pair.School2.Name}\n\n")

    def GenerateSwissPartners(self, RoundNum):
        """Generate Swiss round pairings."""
        # Check if previous round scores have been entered
        if RoundNum > 1:
            for School in self.SchoolList:
                if School.SwissScores[RoundNum - 2] == 0:
                    raise ValueError(f"Scores for round {RoundNum-1} have not been entered for all schools. Please enter all scores before generating round {RoundNum}.")

        # Sort schools by total score
        self.SchoolList.sort(key=lambda x: x.Total, reverse=True)

        # Create pairs
        Pairs = ListOfSwissPairs()
        UsedSchools = set()

        for i, School1 in enumerate(self.SchoolList):
            if School1 in UsedSchools:
                continue

            # Find the best available opponent
            BestOpponent = None
            BestScoreDiff = float('inf')

            for School2 in self.SchoolList[i+1:]:
                if School2 in UsedSchools:
                    continue

                ScoreDiff = abs(School1.Total - School2.Total)
                if ScoreDiff < BestScoreDiff:
                    BestOpponent = School2
                    BestScoreDiff = ScoreDiff

            if BestOpponent:
                Pair = SwissPair(NextKey(self.PossibleSwissSites()), School1.Key, BestOpponent.Key)
                Pairs.AddPair(Pair)
                UsedSchools.add(School1)
                UsedSchools.add(BestOpponent)

        return Pairs

    def PrintFinal(self):
        """Print final results to a text file."""
        FileName = f"{self.DataDir}FinalResults.txt"

        with open(FileName, 'w', encoding='utf-8') as f:
            f.write("Final Results\n")
            f.write("=" * 40 + "\n\n")

            # Sort by total score
            self.SchoolList.sort(key=lambda x: x.Total, reverse=True)

            for i, School in enumerate(self.SchoolList, 1):
                f.write(f"{i}. {School.Name} ({School.Key})\n")
                f.write(f"   Total Score: {School.Total}\n")
                f.write(f"   Z-Score: {School.ZScore:.3f}\n")
                f.write(f"   Group: {sum(School.GroupScores)}\n")
                f.write(f"   Cross: {sum(School.CrossScores)}\n")
                f.write(f"   Relay: {sum(School.RelayScores)}\n")
                f.write(f"   Swiss: {sum(School.SwissScores)}\n\n")

    def GetTop10(self, Location):
        #Get top 10 schools for a given location
        self.SortListScores()
        Top10 = []
        for School in self.SchoolList:
            if School.Location == Location:
                Top10.append(School)
                if len(Top10) == 10:
                    break
        return Top10

    def PrintOverall(self):
        """Print overall results to a text file."""
        FileName = f"{self.DataDir}OverallResults.txt"

        with open(FileName, 'w', encoding='utf-8') as f:
            f.write("Overall Results\n")
            f.write("=" * 40 + "\n\n")

            # Sort by Z-score
            self.SchoolList.sort(key=lambda x: x.ZScore, reverse=True)

            for i, School in enumerate(self.SchoolList, 1):
                f.write(f"{i}. {School.Name} ({School.Key})\n")
                f.write(f"   Z-Score: {School.ZScore:.3f}\n")
                f.write(f"   Total Score: {School.Total}\n\n")

    def UpdateMasterFile(self):
        """Update the master file with results from this competition."""
        MasterFile = f"{self.MasterDir}Schools.csv"
        MasterList = PreviousSchoolList(MasterFile)
        MasterList.ReadFromFile()

        for School in self.SchoolList:
            MasterSchool = MasterList.FindName(School.Name)
            if MasterSchool:
                # Update Z-score using weighted average
                MasterSchool.HistZScore = (MasterSchool.HistZScore + School.ZScore) / 2
            else:
                # Add new school
                MasterList.AddToList(PreviousSchool(School.Name, School.Location, School.ZScore))

        MasterList.SortList()
        MasterList.WriteToFile() 