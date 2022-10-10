#import RPi.GPIO as GPIO
import os
import time
import adafruit_dht
import board
import paho.mqtt.client as mqtt 
dht_device = adafruit_dht.DHT11(board.D17)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)

access_token="Svln5TOW9TOvEjUfvSp6"
port=1883
mqtt.Client.connected_flag=False#create flag in class
broker='demo.thingsboard.io'
client = mqtt.Client()             #create new instance
topic='v1/devices/me/telemetry'
client.on_connect=on_connect  #bind call back function
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker, port, 1)      #connect to broker
client.username_pw_set(access_token)
while not client.connected_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)
print("in Main Loop")

try:
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            print ('Temp: {0:0.1f} C Humidity: {1:0.1f} %'.format(temperature, humidity))
            msg='{"Temp":" '+ str(temperature) + ' "}'
            client.publish(topic,msg)
            msg_hum='{"Hum":" '+ str(humidity) + ' "}'
            client.publish(topic,msg_hum)
            
        except:
            pass

        time.sleep(1)
except KeyboardInterrupt:
    os.system("pgrep libgpiod | xargs kill")
client.loop_stop()    #Stop loop 
client.disconnect() # disconnect
        