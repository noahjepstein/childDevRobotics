import math
import numpy as np 
import csv
import time
import os
import RPi.GPIO as GPIO
import pygame
from RFID_TM import scanRFIDTag
from foodObject import FoodItem


# A FoodItem object has attributes: 
#	'RFIDTag' -- the rfid tag number of the tagged item
#   'name' -- the name of the food
# 	'foodGroup' -- the dinner plate food group of the item, i.e. grains, dairy etc. 
#   'healthIndex' -- the percieved healthiness of the food, on a scale from 1-10
#   'soundFile' -- an mp3 file that holds an mp3 description of the food. 
#   appendToCSV(filename.CSV) -- appends the fooditem to a csv file
#   saveToNewCSV(filename.csv) -- writes the foodItem to a csv file. overwrites an old csv. be careful. 
#   playSound() -- plays the sound file for the food item -- to be implemented

########### GPIO HANDLING and CONSTANTS ##################

RESET_FLAG = False
CHECK_GAME_FLAG = False
RESET_INPUT_CHAN = 22
CHECK_GAME_INPUT_CHAN = 18
SOL_TRIGGER_OUTPUT = 32
READY_LIGHT_OUTPUT_CHAN = 26

TIME_DIFF_MIN = 10000

resetClock = pygame.time.Clock()
checkClock = pygame.time.Clock()


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(RESET_INPUT_CHAN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(CHECK_GAME_INPUT_CHAN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(SOL_TRIGGER_OUTPUT, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(READY_LIGHT_OUTPUT_CHAN, GPIO.OUT, initial = GPIO.LOW)

# data structure initialization

foodList = {}
currentPlate = {}
foodGroups = []

#os.system('omxplayer -o local /home/pi/foodGame/sounds/Windows*')
GPIO.output(READY_LIGHT_OUTPUT_CHAN, True)

# a bunch of funcs for doing random tasks, interrupt handling, etc. 

def loadFoodList():
	
	foodGroupsFile = '/home/pi/foodGame/validFoodGroups.csv'
	f = open(foodGroupsFile, 'rb')
	reader = csv.reader(f)
	global foodGroups
	foodGroups = list(reader)
	f.close()

	foodListFile = '/home/pi/foodGame/foodList.csv'
	f = open(foodListFile, 'rb')
	reader = csv.reader(f)
	foodListRaw = list(reader)
	f.close()
	
	for row in foodListRaw: 
		
		food = FoodItem( RFIDTag = str(row[0]), 
						 name = str(row[1]), 
						 foodGroup = str(row[2]), 
						 healthIndex = str(row[3]), 
						 soundFile = str(row[4]))
		
		foodList[food.RFIDTag] = food

	return foodList

def balancedPlate(): 

	# if foodList.foodGroups contains one of every food group in foodGroups, 
	# plate is balanced (i.e. the child has created a balanced meal)
	# otherwise they must try again

	currFoodGroupList = [food.foodGroup for food in currentPlate.values()]
		

	for food in currentPlate.values():		 
		print str(food.name) + " " + str(food.foodGroup)
		if food.foodGroup not in foodGroups[0]: 
			print "food is not part of a valid food group"
			return False

	if not all(group in currFoodGroupList for group in foodGroups[0]): 
		print "need to have all food groups represented on plate!"
		return False

	groupCounts = collections.Counter(currFoodGroupList)
	if groupCounts['fruit'] not == 2 or groupCounts['fruit'] not == 3:
		return False
	elif groupCounts['vegetable'] not == 3: 
		return False
	elif groupCounts['protein'] > 2:
		return False
	elif groupCounts['dairy'] > 2: 
		return False
	elif groupCounts['treat'] > 1: 
		return False
	elif groupCounts['grain']  not == 3 and groupCounts['grain'] not == 4:
		return False

	return True


def resetCallback(channel):

	global resetClock
	
	timeDiff = resetClock.tick()
	print timeDiff
	
	if timeDiff > TIME_DIFF_MIN: 

		print "Reset detected."
		os.system("omxplayer -o local /home/pi/foodGame/sounds/new\ game.mp3") 
		resetPlate()


def gameCheckCallback(channel): 

	global checkClock
	timeDiff = checkClock.tick()
	print timeDiff
	if timeDiff > TIME_DIFF_MIN: 

		print "Checking state of current game: "

		if balancedPlate(): 
			print "success!"
			triggerSolenoid()
			os.system("omxplayer -o local /home/pi/foodGame/sounds/cheer.mp3")
			# make success sound
			resetPlate()
		else: 
			# make buzzer sound
			os.system("omxplayer -o local /home/pi/foodGame/sounds/buzzer.mp3")
			return

		# if has one of each healthy food group
		# trigger gpio pin for solenoid latch


def triggerSolenoid(): 

	print "Triggering solenoid."
	GPIO.output(SOL_TRIGGER_OUTPUT, True)
	time.sleep(1.000) # wait 1000 ms 
	GPIO.output(SOL_TRIGGER_OUTPUT, False)

def resetPlate():
	print "resetting plate"
	currentPlate.clear()
	print "after call to currentPlate"

######## MAIN GAME CODE #########

foodList = loadFoodList()

while not RESET_FLAG: 

	GPIO.add_event_detect(RESET_INPUT_CHAN, GPIO.RISING, callback = resetCallback, bouncetime = 1000)
	GPIO.add_event_detect(CHECK_GAME_INPUT_CHAN, GPIO.RISING, callback = gameCheckCallback, bouncetime = 1000)

	newID = scanRFIDTag()

	if foodList.has_key(newID):
		foodList[newID].playSound() 
		if not currentPlate.has_key(newID): 
			currentPlate[newID] = foodList[newID]
			print "adding " + foodList[newID].name + " to list"
		else: 
			del currentPlate[newID]
			print "removing " + foodList[newID].name + " from list"


	else: 
		os.system("omxplayer -o local /home/pi/foodGame/sounds/fart.mp3")
		print "Food IDN " + newID + "  not recognized!"

	# compare to list of tags to get a relevant food object
	# add the food object to currentPlate
	# check if current state is healthy meal state
	# can scan object again to remove it 

	# for ID, food in currentPlate.iteritems(): 
	# 	print food.name

	if balancedPlate(): 
		print "Plate currently balanced."
	else: 
		print "Plate not balanced."

	GPIO.remove_event_detect(RESET_INPUT_CHAN)
	GPIO.remove_event_detect(CHECK_GAME_INPUT_CHAN)
	
print foodList
print currentPlate
