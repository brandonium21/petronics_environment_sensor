# Dependancies
import datetime
import csv
import sys
import os
import Adafruit_DHT
import RPi.GPIO as GPIO
from flask import Flask
from multiprocessing import Process, Value

# Variables
store_file = "results.csv"
store_path = ""
storage_location = "{}/{}".format(store_path, store_file)

GPIO.setmode(GPIO.BCM)

#Setup GPIO
red_pin = 18
green_pin = 23
blue_pin = 24
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.output(red_pin, False)
GPIO.output(green_pin, False)
GPIO.output(blue_pin, False)

# Store Data
def StoreData(temp, hum):
    timestamp = datetime.datetime.now()
    if os.path.isfile(storage_location):
        with open(storage_location, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow((timestamp, temp, hum))
    else:
        with open(storage_location, 'w', newline='') as f:
            writer.writerow(('Timestamp', 'Temperature', 'Humidity'))

def UpdateLed(temperature):
    # if temp high; led = Red
    if temperature >= 35.0:
        GPIO.output(red_pin, True)
        GPIO.output(green_pin, False)
        GPIO.output(blue_pin, False)

    # if temp low; led = Blue
    elif temperature <= 20.0:
        GPIO.output(red_pin, False)
        GPIO.output(green_pin, False)
        GPIO.output(blue_pin, True)

    # if temp just right; led = Green
    else:
        GPIO.output(red_pin, False)
        GPIO.output(green_pin, True)
        GPIO.output(blue_pin, False)


# Get Temp and humidity
def GetData(start):
    while True:
    	if loop_on.value == True:
        	humidity, temperature = Adafruit_DHT.read_retry(11, 22)
        	UpdateLed(float(temperature))
        	StoreData(temperature, humidity)
        	#print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)


# Serve dashboard website 
app = Flask(__name__)

@app.route('/')
def hello_world():
    '''
	try:
		with open(storage_location) as f:
            reader = csv.DictReader(f)
                for row in reader:
				    pass
	except:
        '''
    return "Could not retrieve data"

# Run data collection and website side-by-side
if __name__ == "__main__":
   start = Value('b', True)
   p = Process(target=GetData, args=(start,))
   p.start()  
   app.run(debug=True, use_reloader=False)
   p.join()
