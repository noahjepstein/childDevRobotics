# addFoods.py
# Author: Noah J Epstein
# Created: 4/1/2016
# Modified: 4/4/2016
# Adds food items to a list of RFID-tagged food items. 
# A FoodItem object has attributes: 
#	'ID' -- the rfid tag number of the tagged item
#   'name' -- the name of the food item
# 	'foodGroup' -- the dinner plate food group of the item, i.e. grains, dairy etc. 
#   'healthIndex' -- the percieved healthiness of the food, on a scale from 1-10
#   'soundFile' -- an mp3 file that holds an mp3 description of the food. 
#   appendToCSV(filename.CSV) -- appends the fooditem to a csv file
#   saveToNewCSV(filename.csv) -- writes the foodItem to a csv file. overwrites an old csv. be careful. 
# 	playSound() -- plays the sound file for the food item -- to be implemented

import csv
import math
import numpy as np 
import time
from RFID_TM import scanRFIDTag
from foodObject import FoodItem

foodListFile = '/home/pi/foodGame/foodList.csv'
foodSoundsDir = 'sounds/'

print "Keep old food list and add values to it? (y/n)"
print "Pressing y will allow you to append new food items to old list."
print "Pressing n will delete all previous food item values and create new list."
print "Press ctrl-c at any time to quit."

key = raw_input()

if key == "n": 
	if raw_input("Are you sure you want to delete everything? (y/n) ") == "y": 
		makeNewFile = True
else: 
	makeNewFile = False

while True: 

	print "Scan a food item!"

	# get food id
	ID = scanRFIDTag()
	
	f = open(foodListFile)
	if ID in f.read():
		print "ID already in database -- try a different tag."
		continue

	f.close()

	newFood = FoodItem(RFIDTag = ID)

	# assign a name to the food
	newFood.name = raw_input('What is the the food called? ')

	print "Assign a food group." 
	print "protein"
	print "grain"
	print "vegetable"
	print "fruit"
	print "dairy."
	print "treat"
	print "other"
	print "Press enter when done typing."
	newFood.foodGroup = raw_input()

	#print "Great! How healthy is the food, on scale from 1-10? "
	#print "Press enter when done typing."
#	newFood.healthIndex = raw_input()

	# add text to speech creation of sound file for each item
	# currently each food has no soundfile
	print "Type the filename of the sound file associated with this item:"
	newFood.soundFile = raw_input()

	if makeNewFile: 
		newFood.saveToNewCSV(foodListFile)
		makeNewFile = False
	else: 
		newFood.appendToCSV('foodList.csv')






