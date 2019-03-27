import shutil
import os
import re

wdir = "./Data/Master/ReportTemplates/Individual/"
sdir= "./Data/ReportTest/"

School = 'Blah Blah'

SchoolFileName = School.replace(' ','')


#Make a test directory
if (not os.path.exists(sdir)):
    os.makedirs(sdir)


Source = os.path.join(wdir, 'IndividulSchoolTemplate.tex')
Destination = os.path.join(sdir, SchoolFileName+'.tex')


AllOutputNames = {
                    'SchoolName' : 'Blah Blah',\
                    'SchoolLocation' : 'City',\
                    'SchoolTotal' : '368',\
                    'SchoolGroupTotal' : '1',\
                    'SchoolGroupQ1' : '1',\
                    'SchoolGroupQ2' : '1',\
                    'SchoolGroupQ3' : '1',\
                    'SchoolGroupQ4' : '1',\
                    'SchoolGroupQ5' : '1',\
                    'SchoolGroupQ6' : '1',\
                    'SchoolGroupQ7' : '1',\
                    'SchoolGroupQ8' : '1',\
                    'SchoolGroupQ9' : '1',\
                    'SchoolGroupQ10' : '1',\
                    'SchoolSwissTotal' : '1',\
                    'SchoolSwissQ1' : '1',\
                    'SchoolSwissQ2' : '1',\
                    'SchoolSwissQ3' : '1',\
                    'SchoolSwissQ4' : '1',\
                    'SchoolSwissQ5' : '1',\
                    'SchoolCrossTotal' : '1',\
                    'SchoolCrossQ1' : '1',\
                    'SchoolCrossQ2' : '1',\
                    'SchoolCrossQ3' : '1',\
                    'SchoolCrossQ4' : '1',\
                    'SchoolRelayTotal' : '1',\
                    'SchoolRelayQ1' : '1',\
                    'SchoolRelayQ2' : '1',\
                    'SchoolRelayQ3' : '1',\
                    'SchoolRelayQ4' : '1',\
                    'SchoolRelayQ5' : '1',\
                    'SchoolRelayQ6' : '1',\
                    'SchoolRelayQ7' : '1',\
                    'SchoolRelayQ8' : '1',\
                    'SchoolRelayQ9' : '1',\
                    'SchoolRelayQ10' : '1',\
                    'SchoolRelayQ11' : '1',\
                    'SchoolRelayQ12' : '1',\
                    'SchoolRelayQ13' : '1',\
                    'SchoolRelayQ14' : '1',\
                    'SchoolRelayQ15' : '1',\
                    'SchoolRelayQ16' : '1',\
                    'SchoolRelayQ17' : '1',\
                    'SchoolRelayQ18' : '1',\
                    'SchoolRelayQ19' : '1',\
                    'SchoolRelayQ20' : '1'}


with open(Source,'r') as SourceTemplateFile:
    with open(Destination,'wb') as DestinationFile:
        
        ReadSourceLines = SourceTemplateFile.readlines()
        
        for Line in ReadSourceLines:
            
            VarName = re.search('!(.*)!', Line)
            
            if (VarName != None):
                VarNameString = VarName.group(1)
                NewLine = Line.replace('!'+VarNameString+'!', AllOutputNames[VarNameString] )
            else:
                NewLine = Line
            
            DestinationFile.write(NewLine + '\n')


    

