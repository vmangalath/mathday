"""
--- Functions used by program ---
    
    These avoid repetition of the code

"""

#####--Imports--#####
import string
import re



""" 
---Functions Related to Keys---

These functions have to do with operations on the keys which for the purpose
of this program are a capital letter followed by two digits

"""



def IsKey(Key):
    #Function checks if 'Key' satisfies our constraints: starts with a capital letter followed by 2 digits
    #try allows the validity check to be properly performed
    try:
        return ((Key[0] in string.ascii_uppercase) and ((int(Key[1:]) < 100) and (int(Key[1:]) > 0)) )
    except TypeError:
        return False
    

def NextKey(Key,PrevKey):
    #Function checks if 'Key' and 'PrevKey' are successive keys, returns True if they are and false otherwise

    #Check Both Are Keys
    if (not IsKey(Key)):
        raise ValueError('Key (Input 1) was not a Valid Key.')
        
    elif (not IsKey(PrevKey)):
        raise ValueError('PrevKey (Input 2) was not a Valid Key.')
    
    else:
        
        #Break up Keys into their letter and numbers
        PrevKeyNum = int(PrevKey[1:])
        PrevKeyLetter = PrevKey[0]
        
        KeyNum = int(Key[1:])
        KeyLetter = Key[0]
        
        #Result will be false unless the conditions are met
        Result = False
        
        #Is the succesor is first letter same, and number is 1 larger (A2 succeeds A1)
        if(KeyLetter == PrevKeyLetter and KeyNum == PrevKeyNum + 1):
            Result = True
        
        #Is the succesor is first letter different and number is 1 (B1 succeeds A4)
        if( (string.ascii_uppercase.index(KeyLetter) == string.ascii_uppercase.index(PrevKeyLetter) + 1) and KeyNum == 1):
            Result = True
        
        return Result

    

"""
---Functions Related to Filling In Templates---
"""
def ReplaceTemplate(TemplateFile,FinalFile,AllOutputNames):
    #TemplateFile - File containing the template with instances of !*! to be replaced (* meaning a wildcard string of any length)
    #FinalFile - File where filled in template will go
    #AllOutputNames - Dictionary containing the values uf all wildcards in the instance of !*! as keys with the corresponding value to replace it with
    #       e.g file may contain !SchoolName!, AllOutPutNames must then be have the key 'SchoolName' with appropriate schools name
    
    with open(TemplateFile,'r') as SourceTemplateFile:
        
        with open(FinalFile,'wb') as DestinationFile:
            
            #Reads in TemplateFile line by line
            ReadSourceLines = SourceTemplateFile.readlines()
            
            for Line in ReadSourceLines:
                
                #Finds all instances of !*! where * is a wildcard of anylength
                VarName = re.search('!(.*)!', Line)
                
                
                if (VarName != None):
                    #If there was an instance of !*! then we replace is with the appropraite value provided by the dictionary 'AllOutputNames'
                    VarNameString = VarName.group(1)
                    NewLine = Line.replace('!'+VarNameString+'!', AllOutputNames[VarNameString] )
                else:
                    #otherwise no replace is necessary
                    NewLine = Line
                
                #Write the modified line into the new file
                DestinationFile.write(NewLine)    