# MathDay ScoreKeeper Program

Requirements: Python version 2.7 with libraries: Tkinter,tkFont, tkFileDialog,tkMessageBox, scipy,csv,os,functools,random,string,numpy,copy,subprocess, scipy.stats, re

Latex: (TexLive or MikeTex) used with function 'pdf2latex'

requires Tex packages: xcolor 


Program written to keep scores for MathDay at ANU.

Folder Structure:


		Code - Contains the mathday program which is run by running MathDay.py
			Data - Folder for all the Data and Report files for the running of the competition
				Master - Contains all the Master Files and Templates used to run competition 
						(editing this should be done with extreme caution)
						
			Generators - A little script to generate the deafult Master files for valid scores
			
			
			Lib - All the libraries and functions called by MathDay.py
			
			
		DataCopy - Contains a copy of the Master file directory, for safekeeping.
		
		OriginalScoreKeeper - Contains the original ScoreKeeper Program files (database files may be 				useful for getting legacy data). Also contains the original ScoreKeeper manual
		

Makefile - I just used this makefile to make the git calls easy to do
