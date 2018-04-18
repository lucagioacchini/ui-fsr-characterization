#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This script defines all the graphic features of the DatAcquisition GUI. 
At the bottom there are the main functions of the program tabs. The other
functions which are in the "functions" file are bound here

2018 Luca Gioacchini
"""

from Tkinter import*
from functools import partial
import src.functions as sensor
import src.config as config
import time
import Pmw
import PIL.Image
import PIL.ImageTk
import os


#this class is used to print into the textbox the stdout
class RedirectText(object):
	def __init__(self, text_ctrl):
		self.output = text_ctrl
	
	def write(self, string):
		self.output.insert(END, string)
		self.output.see(END)

#main layout class
class Layout:
	def __init__(self, master):
		self.master = master
		master.title("DatAcquisition")
		master.geometry("700x600")
		master.resizable(0,0)
#==========================================================================#		
#NOTEBOOK TAB
		Pmw.initialise()
		self.notebook = Pmw.NoteBook(master)
		self.tab_1 = self.notebook.add('Sensor Characterization')
		self.tab_2 = self.notebook.add('Footstep Tracker')
		self.notebook.pack(fill = BOTH, expand = True)

#TAB 1: SENSOR CHARACTERIZATION
		#define the little upper filler
		self.upper_frame_filler=Frame(self.tab_1, height = 20)
		self.upper_frame_filler.pack(side=TOP)		

#TAB 1 SX SCREEN
		#define the sx frame
		self.sx_frame=Frame(self.tab_1)
		self.sx_frame.pack(side=LEFT, fill = Y)
			
	#FILE NAME STUFF
		#file name label
		self.fname_label = Label(self.sx_frame, text="Enter the output file name")
		self.fname_label.pack()
		#file name text box
		self.fname_text_box=Entry(self.sx_frame, bd=1)
		self.fname_text_box.pack()
		#file name button
		self.save_fname_tab1 = partial(self.save_fname, self.fname_text_box)
		self.fname_button = Button(self.sx_frame, text="Save", width = 6, command=self.save_fname_tab1)
		self.fname_button.pack()
				
	#WEIGHT STUFF	
		#weight label
		self.weight_label = Label(self.sx_frame, text="Enter the weight")
		self.weight_label.pack()
		#weight text box
		self.weight_text_box=Entry(self.sx_frame, bd=1, state = DISABLED)
		self.weight_text_box.pack()
		#weight button
		self.weight_button = Button(self.sx_frame, state = DISABLED, text="Submit", width = 6, command=self.sub_weight)
		self.weight_button.pack()
		self.weight_button.pack()
		
	#CHECKBUTTON STUFF
		self.flag = IntVar()
		self.client = None
		self.check=Checkbutton(self.sx_frame, text="MQTT", variable=self.flag, command=self.MQTT_switch)
		self.check.pack()
		
#TAB 1 DX SCREEN
		#define the dx frame
		self.dx_frame=Frame(self.tab_1)#leave it
		self.dx_frame.pack(side=RIGHT, fill=Y)
		
		#define the dx sub frames
		self.sub_frame_up=Frame(self.dx_frame)
		self.sub_frame_up.pack(fill = Y, expand = True)
		#
		self.sub_frame_filler=Frame(self.dx_frame, height=10)
		self.sub_frame_filler.pack()
		#
		self.sub_frame_down=Frame(self.dx_frame)
		self.sub_frame_down.pack(side=BOTTOM)
		
	#TERMINAL STUFF		
		#define the scroll bar
		self.scroll=Scrollbar(self.sub_frame_up)
		self.scroll.pack(side=RIGHT, fill=Y)
		#define the terminal output
		self.terminal = Text(self.sub_frame_up, height = 28, background="black", foreground="White", bd=0)
		self.terminal.pack(side=LEFT, fill=Y)
		#link the terminal and scroll bar
		self.terminal.config(yscrollcommand=self.scroll.set)
		self.scroll.config(command=self.terminal.yview)
		#call the output redirect class
		redir = RedirectText(self.terminal)
		sys.stdout = redir
		#print the output
		self.to_print = """"""
		self.terminal.insert(END, self.to_print)

	#LOWER BUTTON STUFF	
		#plot button
		self.plot_tab1 = partial(self.plot, None, "tab_1")
		self.plot_button = Button(self.sub_frame_down, text="Plot", state = DISABLED , width = 6, command=self.plot_tab1)
		self.plot_button.pack(side=LEFT)
		
		#close button
		self.close_button = Button(self.sub_frame_down, text="Close", width = 6, command=master.quit)
		self.close_button.pack(side=RIGHT)
		
#TAB 2: FOOTSTEP TRACKER
#TAB 2 UPPER SCREEN: INPUT
		#define the upper frame
		self.upper_frame2=Frame(self.tab_2)
		self.upper_frame2.pack(side=TOP)
		#sx upper subframe
		self.upper_sub_sx=Frame(self.upper_frame2)
		self.upper_sub_sx.pack(side=LEFT)
		#central filler
		self.upper_sub_filler=Frame(self.upper_frame2, width = 200)
		self.upper_sub_filler.pack(side=LEFT)
		#dx lower subframe
		self.upper_sub_dx=Frame(self.upper_frame2)
		self.upper_sub_dx.pack(side=RIGHT)
		
	#FILE NAME STUFF
		#file name label
		self.fname_label2 = Label(self.upper_sub_sx, text="Enter the output file name")
		self.fname_label2.pack()
		#file name text box
		self.fname_text_box2=Entry(self.upper_sub_sx, bd=1)
		self.fname_text_box2.pack()
		#file name button
		self.save_fname_tab2 = partial(self.save_fname, self.fname_text_box2)
		self.fname_button2 = Button(self.upper_sub_sx, text="Save", width = 6, command=self.save_fname_tab2)
		self.fname_button2.pack()
		
	#START/STOP STUFF
		#start/stop function with arguments
		self.avvio = partial(self.footstep_tracker, "start")
		self.stop = partial(self.footstep_tracker, "stop")
		#start button
		self.start_button = Button(self.upper_sub_dx, text="Start", state = DISABLED, width = 6, command=self.avvio)
		self.start_button.pack(side=LEFT)
		#stop button
		self.stop_button = Button(self.upper_sub_dx, text="Stop", state = DISABLED, width = 6, command=self.stop)
		self.stop_button.pack(side=LEFT)
		#close button
		self.close_button = Button(self.upper_sub_dx, text="Close", width = 6, command=master.quit)
		self.close_button.pack(side=RIGHT)
		
#TAB 2 LOWER SCREEN: GRAPHICS
		#define the lower frame
		self.lower_frame2=Frame(self.tab_2)
		self.lower_frame2.pack(fill=BOTH, expand=True)
		self.notebook_graph = Pmw.NoteBook(self.lower_frame2)
		#define the 3 graphic tab
		self.tab_1_graph = self.notebook_graph.add('1st Metatarsus')
		self.tab_2_graph = self.notebook_graph.add('5th Metatarsus')
		self.tab_3_graph = self.notebook_graph.add('Heel')
		self.tab_4_graph = self.notebook_graph.add("Merged")
		self.notebook_graph.pack(fill=BOTH, expand=True)
		#load and insert the photo of the 1st tab
		self.im_1 = PIL.Image.open("docs\img\photo_1.png")
		self.photo_1 = PIL.ImageTk.PhotoImage(self.im_1)
		self.photo_label_1 = Label(self.tab_1_graph, image=self.photo_1)
		self.photo_label_1.pack()
		#load and insert the photo of the 2nd tab
		self.im_2 = PIL.Image.open("docs\img\photo_2.png")
		self.photo_2 = PIL.ImageTk.PhotoImage(self.im_2)
		self.photo_label_2 = Label(self.tab_2_graph, image=self.photo_2)
		self.photo_label_2.pack()
		#load and insert the photo of the 3rd tab
		self.im_3 = PIL.Image.open("docs\img\photo_3.png")
		self.photo_3 = PIL.ImageTk.PhotoImage(self.im_3)
		self.photo_label_3 = Label(self.tab_3_graph, image=self.photo_3)
		self.photo_label_3.pack()
		#load and insert the photo of the 4th tab
		self.im_4 = PIL.Image.open("docs\img\photo_4.png")
		self.photo_4 = PIL.ImageTk.PhotoImage(self.im_4)
		self.photo_label_4 = Label(self.tab_4_graph, image=self.photo_4)
		self.photo_label_4.pack()

#==========================================================================#
#FUNCTIONS

#GENERAL FUNCTIONS
	#Take the fname from text input and save the variable.
	#The weight stuff are enabled only if the fname is saved.
	def save_fname(self, widget):
		self.fname = widget.get()	
		if self.fname == "":
			print "ERROR: Empty field. File name required"
		else:
			self.name = self.fname+"_"+config.name_4+".txt"
			#Enable all the buttons that are disabled
			if (widget==self.fname_text_box):
				self.weight_button.config(state=NORMAL)
				self.weight_text_box.config(state=NORMAL)
				self.plot_button.config(state=NORMAL)
			elif (widget==self.fname_text_box2):
				self.start_button.config(state=NORMAL)
				self.stop_button.config(state=NORMAL)
	
	#If the PLOT button is pressed from TAB_1 the graphic is plotted and showed
	#as a pop-up thanks to the funcion in the FUNCTIONS file.
	#If the PLOT button is pressed from TAB_2 the 3 graphics are plotted and 
	#showed in the lower frame.
	def plot(self, fname, tab):
		if tab=="tab_2":
			sensor.plot_graphic(fname+"_"+config.name_1+".txt",config.name_1, tab)
			sensor.plot_graphic(fname+"_"+config.name_2+".txt",config.name_2, tab)
			sensor.plot_graphic(fname+"_"+config.name_3+".txt",config.name_3, tab)
			sensor.merge_graphic(fname, "Merged")
			os.chdir("Output\Footstep Tracker")
			#Update the 3 graphics
			self.update_graphic(config.name_1, fname+"_"+config.name_1+".png")
			self.update_graphic(config.name_2, fname+"_"+config.name_2+".png")
			self.update_graphic(config.name_3, fname+"_"+config.name_3+".png")
			self.update_graphic("Merged", fname+"_Merged.png")
		elif tab=="tab_1":
			fname=self.fname
			sensor.plot_graphic(fname+"_"+config.name_4+".txt",config.name_4, tab)
				
#TAB_1 FUNCTIONS			
	#Checkbutton function. It sets up the MQTT connection and send
	#the weight value as message. The FLAG variable is given by the
	#checkbox
	def MQTT_switch(self):
		if self.flag.get() == 1:
			self.client = sensor.start_client()			
		if self.flag.get() ==0:
			sensor.disconnect()
			
	#Take the weight from text input, receive the data from arduino 
	#and send it through the MQTT protocol
	def sub_weight(self):
		weight = self.weight_text_box.get()
		resistance=sensor.detect_value(weight, self.flag.get(), self.client)
		os.chdir("Output\Sensor Characterization")
		sensor.save_file(weight,resistance,self.name)

#TAB_2 FUNCTIONS
	#The START/STOP button send the trigger to this function.
	#The trigger is sent to the function in the FUNCTIONS file that
	#can control Arduino.
	#After that all the buttons are disabled until the STOP button 
	#is not pressed.		
	def footstep_tracker(self, trigger):
		sensor.detect_trigger(trigger, self.fname)
		if trigger=="start":
			self.weight_button.config(state=DISABLED)
			self.fname_button.config(state=DISABLED)
			self.check.config(state=DISABLED)
			self.plot_button.config(state=DISABLED)
			self.close_button.config(state=DISABLED)
			self.fname_button2.config(state=DISABLED)
			self.start_button.config(state=DISABLED)
		if trigger=="stop":
			self.weight_button.config(state=NORMAL)
			self.fname_button.config(state=NORMAL)
			self.check.config(state=NORMAL)
			self.plot_button.config(state=NORMAL)
			self.close_button.config(state=NORMAL)
			self.fname_button2.config(state=NORMAL)
			self.start_button.config(state=NORMAL)
			#When the stop button is presed the 3 graphics are plotted.
			self.plot(self.fname, "tab_2")

	#Update the three graphics in the lower frame of TAB_2
	def update_graphic(self, element, fname):
		if element==config.name_1:
			self.im_2 = PIL.Image.open(fname)
			self.photo_2 = PIL.ImageTk.PhotoImage(self.im_2)
			self.photo_label_2.configure(image=self.photo_2)
		elif element==config.name_2:
			self.im_3 = PIL.Image.open(fname)
			self.photo_3 = PIL.ImageTk.PhotoImage(self.im_3)
			self.photo_label_3.configure(image=self.photo_3)
		elif element==config.name_3:
			self.im_1 = PIL.Image.open(fname)
			self.photo_1 = PIL.ImageTk.PhotoImage(self.im_1)
			self.photo_label_1.configure(image=self.photo_1)
		elif element=="Merged":
			self.im_4 = PIL.Image.open(fname)
			self.photo_4 = PIL.ImageTk.PhotoImage(self.im_4)
			self.photo_label_4.configure(image=self.photo_4)

