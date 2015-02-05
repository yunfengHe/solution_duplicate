#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015-1-29

@author: yunfeng
'''
#usage ./processor1 [FileToProcess]
import os
import sys
import collections
from difflib import SequenceMatcher

#Use a hash table. This solution has O(n) time complexity in average case.
#http://stackoverflow.com/questions/26364715/efficient-search-algorithm-to-find-duplicate-strings
#dictionary seems to be extremely quick


def readfile(filename):#return a dic in memory
	prolist = []
	try:
		fd = open(filename, "r")
		while True:
			line =  fd.readline()
			if len(line)==0:
				break
			else:
				prolist.append(line)
		fd.close()
		return prolist
	except:
		IOError
		print "IO error, file cannot be opened"
				

def searchfordup(alist):
	global DoubtIndex
	DoubtIndex = collections.OrderedDict()
	length = len(alist)
	for index in range(length):
		entryA = alist[index].split("\t")
		print entryA[0]
		print entryA[1]	
		for innerIndex in range(index+1,length):
			counter = 0			
			entryB = alist[innerIndex].split("\t")
#can be a loop here to check multiple columns
			if entryA[5] == entryB[5] and entryA[6].upper() == entryB[6].upper() :
				ratio = SequenceMatcher(None, entryA[1].lower(),entryB[1].lower()).ratio()
				if ratio > 0.8:
					alist[innerIndex] = "dup" + alist[innerIndex]
				elif ratio > 0.5:
					DoubtIndex[str(index)] = str(innerIndex)
	return alist
			
def writefile(filename, list):
	filetowrite = open(filename, "w")
	for index in range(len(list)):
		filetowrite.write(list[index]) #+ list[key] #+ "\n"
	filetowrite.close()
	return

def writefiledict(filename, list):
	filetowrite = open(filename, "w")
	for key in list:
		filetowrite.write(key + "\t" + list[key] + "\n") #+ list[key] #+ "\n"
	filetowrite.close()
	return

def main(argv):
	filetoread = sys.argv[1]
	memlist = readfile(filetoread)
	markedlist = searchfordup(memlist)
	newfile = filetoread + 'Processed'
	writefile(newfile, markedlist)
	writefiledict("index.txt", DoubtIndex)	
	return

main(sys.argv[1:]) 	



#http://avrilomics.blogspot.fi/2014/01/calculating-similarity-measure-for-two.html
#http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/
#https://docs.python.org/2/library/functions.html#str
#http://stackoverflow.com/questions/423379/using-global-variables-in-a-function-other-than-the-one-that-created-them
#http://stackoverflow.com/questions/17388213/python-string-similarity-with-probability
#http://avrilomics.blogspot.fi/2014/01/calculating-similarity-measure-for-two.html
#http://stackoverflow.com/questions/17388213/python-string-similarity-with-probability
#https://www.ibm.com/developerworks/library/l-python5/
#http://www.idiotinside.com/2014/09/04/string-processing-in-python/
#http://www.pythonforbeginners.com/basics/string-manipulation-in-python
#https://www.udemy.com/blog/python-string-functions/

#def readfile(filename):
#	#ziplist = {}
#	ziplist = collections.OrderedDict()
#	prolist = {}
#	#address = {}
#	try:
#		fd = open(filename, "r")
#		while True:
#			line =  fd.readline()
#			if len(line)==0:
#				break
#			else:
#				newline = line.split("\t")
#				IDnumber = newline[0]
#				zipcode = newline[5]
#				addr = newline[6]
#		
#				if zipcode not in ziplist:
#					ziplist[zipcode] = line #no strip here
#					prolist[IDnumber] = line
#				else:#zipcode is the same
#					entryA = ziplist[zipcode].split("\t")# previous one
#					if entryA[6].upper() == newline[6].upper():#address comparison
#						prolist[IDnumber] = "DUP"+zipcode + "\t" + line
#						
#						ziplist[zipcode] = line
#					else:
#						prolist[IDnumber] = line	
#					
#				
#		fd.close()		
#		return orilist
#	except:
#		IOError
#		print "IO error, file cannot be opened"


#def writefiledict(filename, list):
#	filetowrite = open(filename, "w")
#	for key in list:
#		filetowrite.write(key + "\t" + list[key]) #+ list[key] #+ "\n"
#	filetowrite.close()
#	return
