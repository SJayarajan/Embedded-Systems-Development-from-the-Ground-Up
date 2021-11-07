# ESP 32 Base Waether Stataion Version-1
#Programmed by Santhosh Jayarajan
#Date: 4/10/2021
#Using Web Sockets and WifI connection
#
#IMPORT LIBRARIES
import machine
import time
import socket
import network
import Wifi_Creds
import dht

# START OF CODE
led = machine.Pin(2,machine.Pin.OUT)
led.off()

Wifi=network.WLAN(network.STA_IF)
Wifi.active(True)
Wifi.connect(Wifi_Creds.ssid,Wifi_Creds.password)
if Wifi.isconnected()==True:
    led.on()
print(Wifi.isconnected())
print(Wifi.ifconfig())

# ************************************
# Configure the socket connection
# over TCP/IP
# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',180)) # specifies that the socket is reachable by any address the machine happens to have
s.listen(5)     # max of 5 socket connections

#DHT sensor initializations

d = dht.DHT22(machine.Pin(23))

#Web page to be displayed
def web_page():

#DHT readings
    d.measure()
    Temp_C=d.temperature()
    Temp_C=35.0
    Hum_Per = d.humidity()
    Hum_Per=75.0
    Forecast1="Weather Forcast here"
    Forecast2="Detailed Weather Forecast here"

#Temperature Forecast    
    if Temp_C<=10.0:
        Forecast1="The Temperature is very Cold and "
    if Temp_C>10.0 and Temp_C<=19.0:
        Forecast1="The Temperature is Quite Cold and "    
    if Temp_C>19.0 and Temp_C<=29.0:
        Forecast1="The Temperature is Marginally Cold and "
    if Temp_C>29.0 and Temp_C<=39.0:
        Forecast1="The Temperature is Quite Warm and "
    if Temp_C>39.0 and Temp_C<=49.0:
        Forecast1="The Temperature is Really Hot and "
#Humidity Forecast
    if Hum_Per<=10.0:
        Forecast1 = Forecast1+"Very Dry"
    if Hum_Per>=10.0 and Hum_Per<30.0:
        Forecast1 = Forecast1+"Dry"
    if Hum_Per>=30.0 and Hum_Per<50.0:
        Forecast1 = Forecast1+"Slightly Dry"
    if Hum_Per>=50.0 and Hum_Per<70.0:
        Forecast1 = Forecast1+"Slightly Wet"
    if Hum_Per>=70.0 and Hum_Per<90.0:
        Forecast1 = Forecast1+"Very Wet"

#DETAILED FORECAST
#Temperature Forecast DETAILED   
    if Temp_C<=10.0:
        Forecast2="The Weather is Chill- Wear warm Clothes and "
    if Temp_C>10.0 and Temp_C<=19.0:
        Forecast2="The Weather is a Bit Chill -Wear Warm Clothes and "    
    if Temp_C>19.0 and Temp_C<=29.0:
        Forecast2="The Weather is Pleasent - Wear Light Clothes and "
    if Temp_C>29.0 and Temp_C<=39.0:
        Forecast2="The Weather is Warm - Wear very Light Clothes and "
    if Temp_C>39.0 and Temp_C<=49.0:
        Forecast2="The Weather is Really Warm - Wear Beach Clothes and "

# Humidity Forecast DETAILED
    if Hum_Per<=10.0:
        Forecast2 = Forecast1+"the Air is Very Dry (Use Moisturizers)"
    if Hum_Per>=10.0 and Hum_Per<30.0:
        Forecast2 = Forecast1+"the Air is Dry (Use Moisturizers)"
    if Hum_Per>=30.0 and Hum_Per<50.0:
        Forecast2 = Forecast1+"the Air is Slightly Dry (Use Sun Screen)"
    if Hum_Per>=50.0 and Hum_Per<70.0:
        Forecast2 = Forecast1+"the Air is Slightly Moist (Use Sun Screen)"
    if Hum_Per>=70.0 and Hum_Per<90.0:
        Forecast2 = Forecast1+"the Air is Very Moist (Use Normal Cream)"
   
#HTML PAGE
    html_page = """<!DOCTYPE html>
<html>
<head>
<style>
table {
  width:100%;
}
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
  border:ridge 5px red;
  background-color:black; color:yellow;
  
}
th, td {
  padding: 15px;
  text-align: left;
 }
TD{font-family: Calibri; font-size: 10pt;}

</style>
</head>
<meta http-equiv="refresh" content="5">
<body bgcolor="MediumSeaGreen">

<h1><center><font face="Calibri">Weather Station Ver 1.0</font></center></h1>

<table>
  <tr>
    <th><h2><center>Temperature in Deg C</center></h2></th>
    <th><h2><center>Humidity in %</center></h2></th> 
    <th><h2><center>Forecast</center></h2></th>
  </tr>
  <tr>
    <td><center>""" + str(Temp_C) + """</center></td>
    <td><center>""" + str(Hum_Per) + """</center></td>
    <td><center>""" + str(Forecast1) + """</center></td>
  </tr>
  
</table>
<br>
<br>
<h1><center><font face="Calibri">Weather Forcast Details</font></center></h1>
  """ + str(Forecast2) + """
   
  <br><br>

</body>
</html>"""
    return html_page  


while True:
    #Socket accept 
    conn, addr = s.accept()
    print("Got connection from %s" % str(addr))
    
    #Socket receive
    request=conn.recv(1024)
    print("")
    print("Content %s" % str(request))

    #Socket send
    request = str(request)
    
    #Create a socket reply
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    
    #Socket close
    conn.close()
