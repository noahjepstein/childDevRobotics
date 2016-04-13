import os
import numpy as np
# import vlc # only on osx

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
			print "Sound file specified must exist and be of .mp3 type."
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

			# for use on osx
			# p = vlc.MediaPlayer(self.soundFile)
			# p.play()
		else: 
			print "NOT IMPEMENTED"



