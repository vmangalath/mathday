"""
--- Generate Master Score Files That Are Identical To Old ScoreKeeper
"""


######--IMPORTS--######
import csv
import os


######--Function To Write QuestionNames and MaxValidScores to a CSV file-######
def WriteMasterFile(FileName,QuestionNames,MaximumValidScores):
        
    
    with open(FileName,'w') as File1:
        writefile = csv.writer(File1, delimiter = ',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
        writefile.writerow(["Question Name","Maximum Valid Score" ])        
                   
        for i in range(len(QuestionNames)):
            writefile.writerow([QuestionNames[i], str(MaximumValidScores[i])])
    


######--Working Directory-######
WorkDir = os.path.join('..','Data','Master','Scores') 

#make the directory if it doesnt exist
if (not os.path.exists(WorkDir)):
    os.makedirs(WorkDir)



######--Group Scores-######
MaximumValidScores = 2*[15] + 2*[20] + 2*[25] + 2*[30] + 2*[35]
Contestn = len(MaximumValidScores)
QuestionNames = ['Q' + str(x)for x in range(1,Contestn+1)]

FileName = os.path.join(WorkDir,"GroupContestScores.csv") 

WriteMasterFile(FileName,QuestionNames,MaximumValidScores)


######--Swiss Scores-######            
Contestn = 5

MaximumValidScores = Contestn*[60]
QuestionNames = ['Round ' + str(x)for x in range(1,Contestn+1)]

FileName = os.path.join(WorkDir,"SwissContestScores.csv") 

WriteMasterFile(FileName,QuestionNames,MaximumValidScores)

        
######--Cross Scores-######       
Contestn = 4

MaximumValidScores = Contestn*[15]
QuestionNames = ['Q' + str(x)for x in range(1,Contestn+1)]

FileName = os.path.join(WorkDir,"CrossContestScores.csv") 

WriteMasterFile(FileName,QuestionNames,MaximumValidScores)
    
    
######--Relay Scores-######    
MaximumValidScores = 2*[10] + 2*[5] + 2*[15] + 2*[10] + 2*[15] + 2*[5] + 2*[20] + 2*[10] + 2*[15] + 2*[20]
Contestn =len(MaximumValidScores)
QuestionNames = ['Q' + str(x)for x in range(1,Contestn+1)]

FileName = os.path.join(WorkDir,"RelayContestScores.csv") 

WriteMasterFile(FileName,QuestionNames,MaximumValidScores)
