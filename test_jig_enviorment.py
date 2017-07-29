# Dependancies
import datetime
import csv
import sys
import os
import Adafruit_DHT
import RPi.GPIO as GPIO
from flask import Flask
from multiprocessing import Process, Value
import pickle
from mpu6050 import mpu6050

# Variables
store_file = "results.csv"
#store_path = "/media/pi/983F-EB83"
store_path = "/home/pi/Github/brandonium21/results"
storage_location = "{}/{}".format(store_path, store_file)
current_temp = 0.0
current_hum = 0.0
sensor = mpu6050(0x68)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Setup GPIO
red_pin = 2
green_pin = 3
blue_pin = 4
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.output(red_pin, True)
GPIO.output(green_pin, True)
GPIO.output(blue_pin, True)

# Store Data
def StoreData(temp, hum):
    timestamp = datetime.datetime.now()
    if os.path.isfile(storage_location):
        with open(storage_location, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow((timestamp, temp, hum))
        current_hum = hum
        current_temp = temp
    else:
        with open(storage_location, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('Timestamp', 'Temperature', 'Humidity'))

def UpdateLed(temperature):
    GPIO.setmode(GPIO.BCM)
    # if temp high; led = Red
    if temperature >= 35.0:
        GPIO.output(red_pin, False)
        GPIO.output(green_pin, True)
        GPIO.output(blue_pin, True)

    # if temp low; led = Blue
    elif temperature <= 20.0:
        GPIO.output(red_pin, True)
        GPIO.output(green_pin, True)
        GPIO.output(blue_pin, False)

    # if temp just right; led = Green
    else:
        GPIO.output(red_pin, True)
        GPIO.output(green_pin, False)
        GPIO.output(blue_pin, True)


# Get Temp and humidity
def GetData(start):
    while True:
    	if start.value == True:
        	humidity, temperature = Adafruit_DHT.read_retry(11, 22)
        	if humidity and temperature:
                    StoreData(temperature, humidity)
                    UpdateLed(float(temperature))
                    print ('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity))

# Get IMU data
def GetIMU(start):
    while True:
        if start.value == True:
            acc_data = sensor.get_accel_data()
            print ('AccX: {0:0.2f} AccY: {1:0.2f} AccZ: {2:0.2f}'.format(acc_data['x'], acc_data['y'], acc_data['z']))

# Serve dashboard website 
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(current_temp, current_hum)

# Run data collection and website side-by-side
if __name__ == "__main__":
   start = Value('b', True)
   p = Process(target=GetData, args=(start,))
   p.start()  
   q = Process(target=GetIMU, args=(start,))
   q.start()  
   app.run(debug=True, use_reloader=False)
   p.join()
   q.join()
