#======CONFIGURATION FILE======#

#MQTT Section------------------
import socket 
host = socket.gethostbyname(socket.gethostname())
port = 1883	
topic = "resistance"
username = "univpm"
passwd = "univpm_test"

#Constant Section--------------
name_1 = "Metat_V"
name_2 = "Heel"
name_3 = "Metat_I"
name_4 = "Sensor"

#Arduino Triggers Section------
sensor_characterization = 'A'
footstep_tracker_start = 'B'
footstep_tracker_stop = 'C'


