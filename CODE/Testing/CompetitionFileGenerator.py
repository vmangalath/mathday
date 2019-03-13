
import csv
import os

CompetitionName = "2019"
MasterFileLocation = "/home/jp/Documents/PhD/project/MathDay/CODE/New/Data/Master/"


def GenerateCompetitionDirAndFiles(MasterFileLocation,SchoolNamesAndKeys):
    
    



"""
wdir = "./Data/2019/"


if not os.path.exists(wdir):
    os.makedirs(wdir)

Schools = ["School 1", "School 2" , "2 cool 4 skool"]
SchoolKeys = ["A1", "A2","A3"]
Location = ["City", "Country","City"]
HistoricalZScore = [0,1,-1]

n = len(Schools)

qlen = 10

Comp1init = n*[qlen*[0]]

s = wdir +  "LineUp.csv"
with open(s,'w') as file2:
    writefile2 = csv.writer(file2, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    writefile2.writerow(["School Key","School Name", "Status","Historical Z Score","Score Comp1 Q1","Score Comp1 Q2","Score Comp1 Q3","Score Comp1 Q4","Score Comp1 Q5","Score Comp1 Q6","Score Comp1 Q7","Score Comp1 Q8","Score Comp1 Q9","Score Comp1 Q10", \
    "Score Comp2 Q1","Score Comp2 Q2","Score Comp2 Q3","Score Comp2 Q4","Score Comp2 Q5", \
    "Score Comp3 Q1","Score Comp3 Q2","Score Comp3 Q3","Score Comp3 Q4","Score Comp3 Q5","Score Comp3 Q6","Score Comp3 Q7","Score Comp3 Q8","Score Comp3 Q9","Score Comp3 Q10","Score Comp3 Q11","Score Comp3 Q12","Score Comp3 Q13","Score Comp3 Q14","Score Comp3 Q15","Score Comp3 Q16","Score Comp3 Q17","Score Comp3 Q18","Score Comp3 Q19","Score Comp3 Q20" \
    ])        
               
    for j in range(n):
        rowwrite = [str(SchoolKeys[j]), str(Schools[j]) , str(Location[j]) , str(HistoricalZScore[j])] + 10*[str(1)] + 5*[str(2)] + + 20*[str(3)]
        writefile2.writerow(rowwrite)
"""