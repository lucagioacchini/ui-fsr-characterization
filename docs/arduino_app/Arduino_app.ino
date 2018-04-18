#define toggle 8
#define analogPin1 0
#define analogPin2 1
#define analogPin3 3

#define resistor 10000.0//Ohm
#define vIn 5.0//Volt

//Define triggers
char sensor_characterization = 'A';
char footstep_tracker_start = 'B';
char footstep_tracker_stop = 'C';

int trigger;
float vRead1, vRead2, vRead3;
float fsr1, fsr2, fsr3;
float vOut1, vOut2, vOut3;

void setup(){
  Serial.begin(9600);
  fsr1 = fsr2 = fsr3 = 0;
  vRead1 = vRead2 = vRead3 = 0;
}
 
void loop(){
  digitalWrite(LED_BUILTIN, HIGH);
  if (Serial.available()){
    char trigger = Serial.read();
    if (trigger == footstep_tracker_start){
      while(trigger!=footstep_tracker_stop){
       vRead1 = analogRead(analogPin1);
       vOut1 = vIn*vRead1/1024.0;

       vRead2 = analogRead(analogPin2);
       vOut2 = vIn*vRead2/1024.0;

       vRead3 = analogRead(analogPin3);
       vOut3 = vIn*vRead3/1024.0;
       
       fsr1 = acquisition(vOut1);
       fsr2 = acquisition(vOut2);
       fsr3 = acquisition(vOut3);
              
       Serial.print(fsr1);
       Serial.print(":");
       Serial.print(fsr2);
       Serial.print(":");
       Serial.println(fsr3);

       trigger=Serial.read();
       delay(50);
      }
    }
    else if(trigger==sensor_characterization){
    vRead1 = analogRead(analogPin1);
    vOut1 = vIn*vRead1/1024.0;
    fsr1 = acquisition(vOut1);
    Serial.print(fsr1);
    }  
  }
  
  
}


float acquisition(float vOut){
  float fsr;
  if(vOut==0){
    fsr = 0;
  }
  else{
    fsr = (vIn-vOut)*resistor/vOut;
    fsr = fsr/1000;
  }
  return fsr;
}

