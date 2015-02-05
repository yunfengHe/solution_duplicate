#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015-1-29

@author: yunfeng
'''
#usage: python processor3.py [DatasheetName]
import os
import sys
import collections
from difflib import SequenceMatcher
from collections import defaultdict


### Return a dictionary of list in memory. companies with the same zipcode and addr form a list and bond to the same dictionary key, which is the zipcode+addr. ###
def readfile(filename): 
	with open(filename, 'r') as f:
		content = f.readlines()
	
	memdict = defaultdict(list) # use a dictionary of list, then we can simply append without exception
	tmp = []
	
	for i in range(len(content)):
		tmp = content[i].split("\t")
		key = "%s\t%s"%(tmp[5],tmp[6]) 	# key is the zipcode+address
		#print key # debugging line
		value = "%s\t%s"%(str(i), content[i])#str(i) records the line number(original number-1) of the original file and is attached in the dictionary value		
		memdict[key].append(value)
	return memdict
	


### Take in the datasheet dictionary and Make two Global lists, one for duplicates, one for possible duplicates; use SequenceMatcher to compare company names ###
def searchfordup(memdict): 
	global DoubtIndex
	DoubtIndex = defaultdict(list)
	global DupIndex # a index list for duplicated entries
	DupIndex = {}
	for key in memdict: # matching companies with the same zipcode and address
		keyArrayLength = len(memdict[key])
		if keyArrayLength != 1: # if there are multiple companies in one address, loop over the values and find duplications
			for index in range(keyArrayLength):
				entryA = memdict[key][index].split("\t")
				print "searching match for company: %s"%(entryA[2])#entryA[0] is the entry line number
				YellowPageFlag = 0
				for innerIndex in range(index+1, keyArrayLength):
					entryB = memdict[key][innerIndex].split("\t")
					ratio = SequenceMatcher(None, entryA[2].lower(),entryB[2].lower()).ratio()# calculate company name similarity
					if ratio > 0.75 and YellowPageFlag == 0:
						if (entryA[15].startswith("Abo") and entryB[15].startswith("GS")) or (entryB[15].startswith("Abo") and entryA[15].startswith("GS")):
							DupIndex[str(entryA[0])] = "DUPYellow_%s"%(str(int(entryB[0])+1))# (int(entryB[0])+1) gives the actual line number of the entry, in the original file
							YellowPageFlag = 1
						else:
							DupIndex[str(entryA[0])] = "DUP_%s"%(str(int(entryB[0])+1))# even if there are multiple duplicates, entryA must be a duplicate. EntryB only keep record of the last duplicated entry.But it does not matter, the iteration will mark the missed duplications in between
						
					elif ratio > 0.5:# save these undetermined correlations to a dictionary
						DoubtIndex[str(entryA[0])].append(str(entryB[0]))
	print "##########################################################################################\nMachine matching for duplicated company entries done!"						
	return


### Take in the original datasheet and the duplicateDictionary, write the marked content to a newfile ###			
def markfile(newfile, orifile, dupdict):
	with open(orifile, 'r') as f:
		tmplist = f.readlines()
	
	for index in range(len(tmplist)):
		if str(index) in dupdict:
			tmplist[index] = "%s\t%s\n"%(tmplist[index].rstrip(), dupdict[str(index)])

	with open(newfile, 'w') as f:
		f.writelines(tmplist)
	print "Marked datasheet generated and saved as \"%s\""%(newfile)
	return	

### For those undetermined entries in the datasheet, save the company entries' line numbers to a new file for later use. the line numbers are list index, thus is the actual line number minus 1 ###
def writefiledict(filename, list):
	filetowrite = open(filename, "w")
	for key in list:
		newline = "\t".join(list[key])
		filetowrite.write(key + "\t" + newline + "\n")
	filetowrite.close()
	print "Line numbers of undetermined entries are grouped and saved in file \"%s\""%(filename)
	return


def main(argv):
	if len(sys.argv) != 2:
		sys.exit("Usage: python processor3.py [DatasheetName]")
	filetoread = sys.argv[1]
	newfile = "Processed%s"%(filetoread)

	memdic = readfile(filetoread)# read file and construct a dictionary in the memory, reduce computational complexity, save the trouble for searching for a matched zipcode and address
	searchfordup(memdic)
	markfile(newfile, filetoread, DupIndex)# mark the datasheet content and write to a new file
	writefiledict("index.txt", DoubtIndex)	# for those undetermined entries in the datasheet, save the line numbers to index.txt for later use. the line numbers are list index, thus is the actual line number minus 1
	print "Please keep the generated files and run \"humanprocessor.py\" to manually match possible duplicates when convenient.\n##########################################################################################"
	return

if __name__ == '__main__':	
	main(sys.argv[1:]) 	









########################################References#################################################

#Regarding similarity
#http://chairnerd.seatgeek.com/fuzzywuzzy-fuzzy-string-matching-in-python/  (very useful library)
#https://github.com/seatgeek/fuzzywuzzy

#http://avrilomics.blogspot.fi/2014/01/calculating-similarity-measure-for-two.html
#https://docs.python.org/2/library/functions.html#str
#http://stackoverflow.com/questions/423379/using-global-variables-in-a-function-other-than-the-one-that-created-them
#http://stackoverflow.com/questions/17388213/python-string-similarity-with-probability
#http://avrilomics.blogspot.fi/2014/01/calculating-similarity-measure-for-two.html
#http://stackoverflow.com/questions/17388213/python-string-similarity-with-probability
#https://www.ibm.com/developerworks/library/l-python5/
#http://www.idiotinside.com/2014/09/04/string-processing-in-python/
#http://www.pythonforbeginners.com/basics/string-manipulation-in-python
#https://www.udemy.com/blog/python-string-functions/

#Regarding performance-Hash
#Use a hash table. This solution has O(n) time complexity in average case.
#http://www.cs.yale.edu/homes/aspnes/pinewiki/C(2f)HashTables.html
#http://stackoverflow.com/questions/960733/python-creating-a-dictionary-of-lists
#https://docs.python.org/2/library/collections.html#defaultdict-objects
#http://stackoverflow.com/questions/114830/is-a-python-dictionary-an-example-of-a-hash-table
#http://stackoverflow.com/questions/26364715/efficient-search-algorithm-to-find-duplicate-strings


################################################ Trashcode #######################################################

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



				#if key in prolist:# does not work if I do not use the defaultdict	
					#value = str(i) + "\t" + line
					#prolist[key].append(value)			
				#else:
				#	print "nothing is wrong"
				#	prolist[key] = str(i) + "\t" + line



	#value = str(i) + "\t" + line  # bad manner
	#value = "%s\t%s"%(str(i), line)  #good manner, formated input


	#global DoubtIndex
	#DoubtIndex = collections.OrderedDict()
	#global DupIndex # a index list for duplicated entries
	#DupIndex = collections.OrderedDict()


