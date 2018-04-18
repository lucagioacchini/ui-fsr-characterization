#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import socket
import paho.mqtt.client as mqtt
import time
import config

class Client():
	def __init__(self, username, passwd, host, port):	
		self.username = config.username
		self.host = config.host
		self.port = config.port
		self.passwd = config.passwd
		self.client = mqtt.Client()
	
	#ACK notification methods	
	def conn_ACK(self, client, userdata, flags, rc):
		if rc == 0:
			print "Connected to "+self.host+":"+str(self.port)
		else:
			print "Connection refused: "+str(rc)
	
	def pub_ACK(self, client, userdata, mid):
		print "Message published"

	def disconn_ACK(self, client, userdata, rc):
		print "Client disconnected"
	
	def sub_ACK(self, client, userdata, mid, granted_qos):
		print "Subscribed to ",self.topic

	def msg_ACK(self, client, userdata, msg):
		print msg.topic+"/"+str(msg.payload)
	
	#client methods	
	def create_connection(self):
		self.client.username_pw_set(self.username, password = self.passwd)
		self.client.connect(self.host, self.port, 60)
		self.client.on_connect = self.conn_ACK
	
	def publish(self, topic, message):
		self.client.publish(topic, payload=message, qos=2)
		self.client.on_publish = self.pub_ACK
	
	def subscribe(self, topic):
		self.client.subscribe(topic, 0)
		self.client.on_subscribe = self.sub_ACK
		
	def disconnect(self):
		self.client.disconnect()
		self.client.on_disconnect = self.disconn_ACK
		
	def start(self):
		self.client.loop_start()
	
	def stop(self):
		self.client.loop_stop()
