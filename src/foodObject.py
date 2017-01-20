# foodObject.py
# Author: Noah J Epstein
# Created: 4/1/2016
# Modified: 4/4/2016

import os
import numpy as np
# import vlc # only on osx


# A FoodItem object has attributes:
#	'RFIDTag' -- the rfid tag number of the tagged item
#   'name' -- the name of the food
# 	'foodGroup' -- the dinner plate food group of the item, i.e. grains, dairy etc.
#   'healthIndex' -- the percieved healthiness of the food, on a scale from 1-10
#   'soundFile' -- an mp3 file that holds an mp3 description of the food.
#    appendToCSV(filename.CSV) -- appends the fooditem to a csv file
#    saveToNewCSV(filename.csv) -- writes the foodItem to a csv file. overwrites an old csv. be careful.
#    playSound() -- plays the sound file for the food item -- to be implemented
class FoodItem:

	def __init__(self, RFIDTag = -1, name = 'NOT A FOOD', foodGroup = 'NONE', healthIndex = -1, soundFile = 'NONE'):
		self.RFIDTag = RFIDTag
		self.name = name
		self.foodGroup = foodGroup
		self.healthIndex = healthIndex

		if (os.path.isfile(soundFile) and soundFile.endswith('.mp3')):
			self.soundFile = soundFile
		elif soundFile == 'NONE':
			self.soundFile = soundFile
		else:
			self.soundFile = soundFile


	def appendToCSV(self, filename):

		csvRow = (str(self.RFIDTag)     + ',' +
			      str(self.name)        + ',' +
				  str(self.foodGroup)   + ',' +
				  str(self.healthIndex) + ',' +
				  str(self.soundFile)   + '\n')

		fd = open(filename,'a')
		fd.write(csvRow)
		fd.close()

	def saveToNewCSV(self, filename):

		csvRow = (str(self.RFIDTag)     + ',' +
			      str(self.name)        + ',' +
				  str(self.foodGroup)   + ',' +
				  str(self.healthIndex) + ',' +
				  str(self.soundFile)   + '\n')

		fd = open(filename,'w')
		fd.write(csvRow)
		fd.close()

	def CSVRowToFoodItem(self, row):
		rowArr = np.genfromtxt(row, delimiter = ",")
		self.RFIDTag = rowArr[0]
		self.name = rowArr[1]
		self.foodGroup = rowArr[2]
		self.healthIndex = rowArr[3]
		self.soundFile = rowArr[4]


	def playSound(self):

		if self.soundFile != 'NONE':

			soundfiledir = "/home/pi/foodGame/sounds/"
			# for use on raspberry pi
			bashstr = "omxplayer -o local " + soundfiledir + self.soundFile
			os.system(bashstr)

		else:
			print "NOT IMPEMENTED"
