# UI-based FSR Sensors Characterization Tool
The tool allows data acquisition from one or more FSR sensors providing measurement charts. It provides two main functionalities:
1. On-demand data acquisition for FSR sensor characterization
2. Continuous acquisition for tracking the weight distribution during gait phases

## Setup
Install the requirements
```sudo pip install -r requirements.txt```

## Hardware
The tool works with:
1. Arduino Uno board
2. Interlink Electronics FSR 402 sensors
3. One 10kOhm restistor per sensor

Three Arduino analogic pins are used to read the voltage divider output. The primary resistor is 10kOhm, whereas the FSR is the variable secondary resistor. The Arduino sketch is in ```docs\arudino_app```

## Configuration file
Stored in ```docs/src/``` the most important part is the MQTT section.  

**Warning** If the Arduino trigger are changed is necessary to change the sketch accordingly.

## Sensor Characterization
Connect the Arduino board to the device running the tool.

The Arduino reference pin is ```A0```. Acquired data and charts are locally saved in ```Output/SensorCharacterization```.
To send data over MQTT the checkbox in the UI muist be flagged, then once the tool is running:
1. Insert the output filename
2. Insert the used weight in grams for the sensor characterization and press 'Submit'
3. The terminal will show the FSR resistance value w.r.t. the used weigth
4. When finished press 'Plot' to show the charts.

## Footstep Tracker
Connect the Arduino board to the device running the tool.

The Footstep Tracker functionality is used to obtain a continous data stream from the FSR. The Arduino reference pins are ```A0, A1, A3```.
The tool saves 4 files (3 with acquisition from each sensor and 1 with the merged data). For the charts it does the same.
Outputs are saved in ```Output/SensorCharacterization```.  
Once the tool is running:
1. Insert the output filename
2. Press 'Start' to start data acquisition
3. Press 'Sopt' to stop the acquisition. The plots are automatically displayed

## Further Reading
[LoRa Evaluation in Mobility Conditions for a Connected Smart Shoe Measuring Physical Activity](https://ieeexplore.ieee.org/abstract/document/8805037)

##
2018 Luca Gioacchini
