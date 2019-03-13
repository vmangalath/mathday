@Echo off
Echo ***** Please wait till invited to close DOS Window ....
Echo -----------------------------------------------------------------------
C:
cd "C:\ScoreKeeper\MATHSDAY\2001"
Echo Copying Head to Head Input from DB Directory to System Directory
Copy "C:\ScoreKeeper\MATHSDAY\2001\SwissHTHin5.txt" "C:\ScoreKeeper\MATHSDAY\2001\data.txt"
Echo Running Java to Determine Head to Head Round 5
"C:\Program Files\JavaSoft\JRE\1.3.0_02\bin\java" Swiss > "C:\ScoreKeeper\MATHSDAY\2001\SwissHTHOut5.txt"
Echo Completed execution of Java Script to Determine Teams to meet Head to Head
Echo -----------------------------------------------------------------------
Echo ***** Close this DOS Window and Continue running Scorekeeper ......
