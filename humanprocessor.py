#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2015-1-29

@author: yunfeng
'''
#usage: python humanprocessor.py ProcessedSub-Companies.csv index.txt
import os
import sys
import collections
from difflib import SequenceMatcher
from collections import defaultdict
import signal, os


def readIndexFiletoDict(indexfile):
	with open(indexfile, 'r') as f:
		content = f.readlines()	

	indexdict = defaultdict(list)
	tmp = []

	for index in range(len(content)):
		tmp = content[index].split("\t")
		tmp[len(tmp)-1] = tmp[len(tmp)-1].rstrip()
		key = str(tmp[0])
		for i in range(len(tmp)):# the key tmp[0] shall also be appended, since it is also a line index
			indexdict[key].append(tmp[i])
	
	return indexdict
		
		

def humanmark(datasheet, indexfile, indexdict):	
	# a signal is used to end the human matching process, unfinished work is saved properly by the signal handler
	def handler(signum, frame):
		print "\n##########################################################################################\nShutting down Humanprocessor and save your work..."
		#print "keyA is now %s"%(keyA)# debugging line
		with open(datasheet, 'w') as f:# save exsiting work
			#print content[int(indexdict[keyA][indexC])]# debugging line
			f.writelines(content)
		print "\"%s\" successfully updated!"%(datasheet)
		for i in range(len(done)):# rewrite the indexdict
			if done[i] in indexdict:
				del indexdict[done[i]] # can use pop indexdict[done[i]] to get the deleted key to log to a file
				print "group %s processed and removed from index.txt"%(done[i])			
		writefiledict(indexfile, indexdict)#rewrite index.txt for latter human process		
		print "You can resume the manual matching by running \"humanprocessor.py\" later!\n##########################################################################################"
		sys.exit(0)

	signal.signal(signal.SIGINT, handler)# use SIGINT to shutdown and save previous work
		
	done = [] # A list of processed keys(companies with the same addresses and names of over 50% similarity)

	with open(datasheet, 'r') as f:
		content = f.readlines()

	for keyA in indexdict:# all indexed entry under keyA have same addresses and names of over 50% similarity
		listLength = len(indexdict[keyA])
		for indexC in range(listLength):
			entryC = content[int(indexdict[keyA][indexC])].split("\t")
			#print "now processing line %s of the datasheet"% (str(int(indexdict[keyA][indexC])+1))
			YellowPageFlag = 0
			for indexD in range(indexC+1, listLength):
				entryD = content[int(indexdict[keyA][indexD])].split("\t")				
				print "are these two companies the same?"
				print "%s\n%s"%(entryC[1],entryD[1])
				result = raw_input("'y' if true, 'n' if false\n")
				if result.lower() == 'y' and YellowPageFlag == 0:
					if (entryC[14].startswith("Abo") and entryD[14].startswith("GS")) or (entryD[14].startswith("Abo") and entryC[14].startswith("GS")):
						lineC = "%s\t%s_%s\n"%(content[int(indexdict[keyA][indexC])].rstrip(), "HDUPYellow",str(int(indexdict[keyA][indexD])+1))
						YellowPageFlag = 1
					else:
						lineC = "%s\t%s_%s\n"%(content[int(indexdict[keyA][indexC])].rstrip(), "HDUP",str(int(indexdict[keyA][indexD])+1))
					
					content[int(indexdict[keyA][indexC])] = "%s"%(lineC)# replace original line if dup found
		done.append(keyA)#after one key(address) is pocessed, delete it from the dictionary


	with open(datasheet, 'w') as f:
		f.writelines(content)# f.writelines(content)	
	return

				
def writefiledict(filename, list):
	filetowrite = open(filename, "w")
	for key in list:
		newline = "\t".join(list[key])
		filetowrite.write(newline + "\n")
	filetowrite.close()
	print "\"%s\" successfully updated!"%(filename)
	return	

	
		
def main(argv):	
	if len(sys.argv) != 3:
		sys.exit("Usage: python humanprocessor.py [Processed_datasheet_name] [index.txt]")
	humanmark(sys.argv[1], sys.argv[2], readIndexFiletoDict(sys.argv[2]))
	return

if __name__ == '__main__':	
	main(sys.argv[1:]) 	






#########################References######################################
#http://stackoverflow.com/questions/12371361/using-variables-in-signal-handler-require-global
#http://stackoverflow.com/questions/6970224/providing-passing-argument-to-signal-handler



########################Deserted function###################3
#def humanmark(datasheet, indexdict):
#	with open(datasheet, 'r') as f:
#		content = f.readlines()
#
#	for keyA in indexdict:
#		entryA = content[int(keyA)].split("\t")
#		listLength = len(indexdict[keyA])
#		for indexB in range(listLength):
#			entryB = content[int(indexdict[keyA][indexB])].split("\t")
#			print "are these two companies the same?"
#			print "%s\n%s"%(entryA[1],entryB[1])
#			result = raw_input("'y' if true, n if false\n")
#			if result == 'y':
#				if (entryA[14].startswith("Abo") and entryB[14].startswith("GS")) or (entryB[14].startswith("Abo") and entryA[14].startswith("GS")):
#				
#					linekeyA = "%s\t%s\n"%(content[int(keyA)].rstrip(), "DUPYellow")			
#				else:
#					linekeyA = "%s\t%s\n"%(content[int(keyA)].rstrip(), "DUP")
#				
#				content[int(keyA)] = "%s"%(linekeyA)
#
#		for indexC in range(listLength):
#			entryC = content[int(indexdict[keyA][indexC])].split("\t")
#			for indexD in range(indexC+1, listLength):
#				entryD = content[int(indexdict[keyA][indexD])].split("\t")
#				print "are these two companies the same?"
#				print "%s\n%s"%(entryC[1],entryD[1])
#				result = raw_input("'y' if true, n if false\n")
#				if result == 'y':
#					if (entryC[14].startswith("Abo") and entryD[14].startswith("GS")) or (entryD[14].startswith("Abo") and entryC[14].startswith("GS")):
#						
#						lineindexC = "%s\t%s\n"%(content[int(indexdict[keyA][indexC])].rstrip(), "DUPYellow")
#					else:
#						lineindexC = "%s\t%s\n"%(content[int(indexdict[keyA][indexC])].rstrip(), "DUP")
#					
#					content[int(indexdict[keyA][indexC])] = "%s"%(lineindexC)
#
#	with open(datasheet, 'w') as f:
#		f.writelines(content)# f.writelines(content)	
#	return
			


