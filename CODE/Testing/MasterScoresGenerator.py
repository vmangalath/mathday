
import csv
import os

wdir = "./Data/Master/Scores/"


# Name of Contest = FileName
# Question Number and Valid score


# Group

Contestn = 10

MaximumValidScore = 2*[15] + 2*[20] + 2*[25] + 2*[30] + 2*[35]

s = wdir +  "GroupContestScores.csv"

with open(s,'w') as file1:
    writefile = csv.writer(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    writefile.writerow(["Question Number","MaximumValidScore" ])        
               
    for i in range(Contestn):
        rowwrite = [str(i+1), str(MaximumValidScore[i])]
        writefile.writerow(rowwrite)
        
# Swiss Score
        
Contestn = 5

MaximumValidScore = Contestn*[60]

s = wdir +  "SwissContestScores.csv"

with open(s,'w') as file1:
    writefile = csv.writer(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    writefile.writerow(["Question Number","MaximumValidScore" ])        
               
    for i in range(Contestn):
        rowwrite = [str(i+1), str(MaximumValidScore[i])]
        writefile.writerow(rowwrite)
        
# Cross Score
        
Contestn = 4

MaximumValidScore = Contestn*[15]

s = wdir +  "CrossContestScores.csv"

with open(s,'w') as file1:
    writefile = csv.writer(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    writefile.writerow(["Question Number","MaximumValidScore" ])        
               
    for i in range(Contestn):
        rowwrite = [str(i+1), str(MaximumValidScore[i])]
        writefile.writerow(rowwrite)
        
# Relay Score
        
Contestn = 20

MaximumValidScore = 2*[10] + 2*[5] + 2*[15] + 2*[10] + 2*[15] + 2*[5] + 2*[20] + 2*[10] + 2*[15] + 2*[20]

s = wdir +  "RelayContestScores.csv"

with open(s,'w') as file1:
    writefile = csv.writer(file1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    writefile.writerow(["Question Number","MaximumValidScore" ])        
               
    for i in range(Contestn):
        rowwrite = [str(i+1), str(MaximumValidScore[i])]
        writefile.writerow(rowwrite)
    
    
    

