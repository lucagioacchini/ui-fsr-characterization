#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This script defines the main functions of the program. They manage the MQTT and
the Arduino communication, plot the graphics and save the files. 

2018 Luca Gioacchini
"""

import os
import serial
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
from client import Client
import config
import threading

#This is the first called function. It starts the Arduino communication 
#and creates the Output directory
def start_sensor():
	global arduino
	global topic
	global main_dir

	arduino = serial.Serial("COM4",9600,timeout=0)
	main_dir = os.getcwd()
	if not os.path.isdir("Output"):
		os.mkdir("Output")

#Sensor Characterization "main" function. It sends the trigger to Arduino
#collects data and print them.
def detect_value(value, flag, client):
	#directory management
	os.chdir(main_dir+"\Output")
	if not os.path.isdir("Sensor Characterization"):
		os.mkdir("Sensor Characterization")
	os.chdir("Sensor Characterization")
	#Arduino communication
	weight = value
	time.sleep(0.5)
	arduino.write(config.sensor_characterization)
	time.sleep(0.5)
	resistance = arduino.readline()
	#Terminal communication
	print "Weight: "+value+" g"
	message = str(resistance)
	print "Resistance value:"+message+" kOhm"
	#MQTT communication
	if flag == 1:
		client.publish(topic, message)
	#time.sleep(1)
	os.chdir(main_dir)
	return(resistance)

#Detect the Arduino trigger from the button in TAB_2
def detect_trigger(switch, fname):
	global trigger 
	global foot_raw_name
	
	foot_raw_name=fname
	trigger=switch
	
	if (trigger=="start"):
		#directory management
		os.chdir(main_dir+"\Output")
		if not os.path.isdir("Footstep Tracker"):
			os.mkdir("Footstep Tracker")
		os.chdir("Footstep Tracker")
		#Arduino communication
		arduino.write(config.footstep_tracker_start)
		#Call the Footstep Tracker "main" function
		tracker_acquisition()
	elif (trigger=="stop"):
		arduino.write(config.footstep_tracker_stop)
		#The following two lines close and reopen the Arduino communication
		#cleaning the Serial.
		arduino.close()
		arduino.open()
		tracker_acquisition()

#Footstep Tracker "main" function. It uses the Threading lib. This is because 
#the serial reading is into a while loop. In this way a second thread which 
#"listens to" the trigger in parallel.
def tracker_acquisition():
	#funcion for the Threading lib
	def run():
		nrSample=0
		while(trigger=="start"):
			message = arduino.readline()
			if (message!=""):
				if (nrSample != 0):#because the 0-sample is generally a character	
					#split the message read
					dataArray = message.split(":")
					#divide the message into 3 type of data
					data_1=dataArray[0]#5th metatarsal bone 
					data_2=dataArray[1]#heel
					data_3=dataArray[2]#1st metatarsal bone
					#store the collected data into 4 files
					save_file(nrSample, message, foot_raw_name+"_message.txt")#global message
					save_file(nrSample, data_1, foot_raw_name+"_"+config.name_1+".txt")
					save_file(nrSample, data_2, foot_raw_name+"_"+config.name_2+".txt")
					save_file(nrSample, data_3, foot_raw_name+"_"+config.name_3+".txt")
				nrSample=nrSample+1
					
			if (trigger=="stop"):
				os.chdir(main_dir)
				break
	#threading manangement
	thread = threading.Thread(target=run)  
 	thread.start()

#When called this function creates the MQTT client
def start_client():
	global client
	topic = config.topic
	print"Topic set to:"+topic
	#Create the client and start the connection
	client=Client(config.username, config.passwd, config.host, config.port)
	client.create_connection()
	client.start()
	return client

#Interrupt the MQTT communication
def disconnect():
	client.disconnect()
	client.stop()

#Save data into a .txt file
def save_file(weight, resistance, fname):
	if os.path.isfile(fname):
		res = "\n" + str(weight) + ":" + str(resistance)
	else:
		res = str(weight) + ":" + str(resistance)
	with open(fname, "a") as myfile:
		myfile.write(res)
	myfile.close()


#Plot data and save it into a .png file
def plot_graphic(fname, title, tab):
	#clear the previous graphic
	plt.clf()
	#label management
	if tab=="tab_1":
		plt.xlabel('Weight(g)')
		plt.ylabel('Resistance(kOhm)')
	elif tab=="tab_2":
		os.chdir("Output/Footstep Tracker")
		plt.xlabel('Samples')
		plt.ylabel('Resistance(kOhm)')
	#plot manangement
	x, y = np.loadtxt(fname, delimiter=":", unpack=True)
	plt.plot(x,y,linewidth=1)
	ax=plt.axes()
	ax.yaxis.grid()
	plt.title(title)
	plt.savefig(fname[:-4]+".png")
	if tab=="tab_1":
		plt.show()
	os.chdir(main_dir)

#This function reopens all the Footstep Tracker files and replot the
#data together to compare them
def merge_graphic(fname, title):
	os.chdir("Output/Footstep Tracker")
	plt.clf()
	plt.xlabel("Samples")
	plt.ylabel("Resistance(kOhm)")
	ax=plt.axes()
	ax.yaxis.grid()
	plt.title(title)
	#plt.ylim(0, 50)#MODIFY THIS
	x, y = np.loadtxt(fname+"_"+config.name_1+".txt", delimiter=":", unpack=True)
	plt.plot(x,y,linewidth=1.3, label="Metat_V")
	x, y = np.loadtxt(fname+"_"+config.name_2+".txt", delimiter=":", unpack=True)
	plt.plot(x,y,linewidth=1.3, label="Metat_I")
	x, y = np.loadtxt(fname+"_"+config.name_3+".txt", delimiter=":", unpack=True)
	plt.plot(x,y,linewidth=1.3, label="Heel")
	plt.legend(borderaxespad=0.)
	plt.savefig(fname+"_Merged.png")
	os.chdir(main_dir)
