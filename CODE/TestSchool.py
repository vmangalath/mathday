"""
from Lib.Structures.Structs import CompetitionSchool,PreviousSchool,RegisteredSchool,RegisterSchoolList, PreviousSchoolList,CompetitionSchoolList

MasterFileSchool = './Data/Master/Schools.csv'
MasterDir = './Data/Master/'
CompFile = './Data/Test/Competition.csv'


PrevList = PreviousSchoolList(MasterFile=MasterFileSchool)
PrevList.ReadFromFile()

RegisterList = [PrevList.SchoolList[1].Register('A1'),PrevList.SchoolList[2].Register('A3'),PrevList.SchoolList[3].Register('A2')]
RegisterSchoolList = RegisterSchoolList(RegisterList)

Comp1 = CompetitionSchoolList(File=CompFile,MasterDir=MasterDir)

Comp1.CompeteRegistered(RegisterSchoolList)

Comp1.SchoolList[0].SwissPartners[0] = 'A2'
Comp1.SchoolList[0].SwissSites[0] = 'A1'

Comp1.WriteToFile()

Comp1.ReadFromFile()
"""


from Lib.Structures.Structs import SwissPair,ListOfSwissPairs

a1 = SwissPair('A1','A2','A3')
a2 = SwissPair('A3','A1','A4')
a3 = SwissPair('A99','A5','A6')

All = ListOfSwissPairs(SwissPairs=[a1,a2,a3])


