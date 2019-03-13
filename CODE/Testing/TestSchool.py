from Lib.Structures.Structs import CompetitionSchool,PreviousSchool,RegisteredSchool,RegisterSchoolList, PreviousSchoolList,CompetitionSchoolList

MasterFileSchool = './Data/Master/Schools.csv'
MasterDir = './Data/Master/'
CompFile = './Data/2019/Competition.csv'


PrevList = PreviousSchoolList(MasterFile=MasterFileSchool)
PrevList.ReadFromFile()

RegisterList = [PrevList.SchoolList[1].Register('A1'),PrevList.SchoolList[2].Register('A3'),PrevList.SchoolList[3].Register('A2')]
RegisterSchoolList = RegisterSchoolList(RegisterList)

Comp1 = CompetitionSchoolList(File=CompFile,MasterDir=MasterDir)

#Comp1.CompeteRegistered(RegisterSchoolList)

#Comp1.WriteToFile()
Comp1.ReadFromFile()

Mess = Comp1.FindKey('A2')
Mess.TotalUpdate(['A'])

print(Mess.Total)



