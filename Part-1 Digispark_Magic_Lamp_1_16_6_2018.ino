#include <SoftSerial.h>
#include <TinyPinChange.h>  

//#include <SoftwareSerial.h>
#include <EEPROM.h>

/*
 SMARTBULB By Santhosh Jayarajan
 1. Uses Digispark at 16.5 Mhz Internal
 2.Uses a HC 06 TO commuictae by Bluetooth to the Tiny 85
 3.LED connected to Port 2
 4 HC -06 TO Port - 1and 3
*/
#define SUPLED 2
#define PWMOUT 0

const byte BTRX = 4;
const byte BTTX = 1;


//VARIABLES
double LEDCount;
int BTCommand;
int BTParameter;
byte LightBrightness;
byte LightBrightnessRaw;
SoftSerial BTRead(BTRX,BTTX);

void setup()
{
pinMode(SUPLED,OUTPUT);
pinMode(PWMOUT,OUTPUT);
pinMode(BTRX,INPUT);
pinMode(BTTX,OUTPUT);
BTRead.begin(9600);
EEPROM.write(10,255); 
LightBrightnessRaw=EEPROM.read(10); 
}


//LIGHT ON
void Light_On()
{
LightBrightnessRaw=EEPROM.read(10); 
}
//LIGHT OFF
void Light_Off()
{
LightBrightnessRaw=0;  
}

//BT READ SUBROUTINE
void BTDataRead()
{

if(BTRead.available()>1)
{
digitalWrite(SUPLED,HIGH);
delay(100);
digitalWrite(SUPLED,LOW);

BTCommand=BTRead.parseInt();
BTParameter=BTRead.parseInt(); 
}
if(BTCommand==1){Light_On();}
if(BTCommand==2){Light_Off();}
if(BTCommand==3)
{
LightBrightnessRaw=constrain(BTParameter,0,255);
EEPROM.write(10,LightBrightnessRaw);
if(LightBrightness!=EEPROM.read(10))
{
EEPROM.write(10,LightBrightness);
}


}

}

// MAIN LOOP
void loop() 
{
BTDataRead();  
//Ramp up
if(LightBrightnessRaw>LightBrightness)
{
while(LightBrightnessRaw>LightBrightness){LightBrightness=LightBrightness+1;delay(30);analogWrite(PWMOUT,LightBrightness);}  
}
//Ramp down
if(LightBrightnessRaw<LightBrightness)
{
while(LightBrightnessRaw<LightBrightness){LightBrightness=LightBrightness-1;delay(30);analogWrite(PWMOUT,LightBrightness);}  
}
//Steady State Value
if(LightBrightnessRaw==LightBrightness)
{
analogWrite(PWMOUT,LightBrightness);  
}
}

