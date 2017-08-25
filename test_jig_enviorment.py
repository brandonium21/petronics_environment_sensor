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
import logging
import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import uuid
import json
from mpu6050 import mpu6050
import errortrack


# Variables
store_file = "results.txt"
#store_path = "/media/pi/983F-EB83"
store_path = "/Desktop"
storage_location = "{}/{}".format(store_path, store_file)
sensor = mpu6050(0x68)
node = str(uuid.uuid4())
iot_topic = "factory-node/{}".format(node)

host = "a1la3qkft0cvmg.iot.us-east-2.amazonaws.com"
myMQTTClient = AWSIoTMQTTClient("factory_sensor")
myMQTTClient.configureEndpoint(host, 8883)
myMQTTClient.configureCredentials("mqtt_res2/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.crt",
                                  "mqtt_res2/factory_sensor.private.key",
                                  "mqtt_res2/factory_sensor.cert.pem")

# AWSIoTMQTTClient connection configuration
myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
# Infinite offline Publish queueing
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.connect()

# Store Data


def StoreData(data):
    if os.path.isfile(storage_location):
        with open(storage_location, 'a', newline='') as f:
            json.dump(json.load(data), f)
    else:
        with open(storage_location, 'w', newline='') as f:
            print("blah")
            # Get Temp and humidity
    pass


def GetData(start):
    while True:
        if start.value == True:
            humidity, temperature = Adafruit_DHT.read_retry(11, 22)
            if humidity and temperature:
                timestamp = str(datetime.datetime.now())
                data_scheme = json.dumps({
                    "temperature": {"value": temperature, "node": node, "timestamp": timestamp},
                    "humidity": {"value": humidity, "node": node, "timestamp": timestamp}
                })
                try:
                    myMQTTClient.publish(iot_topic, data_scheme, 1)
                except:
                    #raise ComponentFailure('Could not publish', Adafruit_DHT, 'HDT22')
                    print("There was a publish error HDT")
                    pass

                StoreData(data_scheme)
                print('Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(
                    temperature, humidity))

# Get IMU data


def GetIMU(start):
    while True:
        if start.value == True:
            acc_data = sensor.get_accel_data()
            acc_temp = sensor.get_temp()
            if acc_data and acc_temp:
                timestamp = str(datetime.datetime.now())
                data_scheme = json.dumps({
                    "accx": {"value": acc_data['x'], "node": node, "timestamp": timestamp},
                    "accy": {"value": acc_data['y'], "node": node, "timestamp": timestamp},
                    "accz": {"value": acc_data['z'], "node": node, "timestamp": timestamp},
                    "sensorTemp": {"value": acc_temp, "node": node, "timestamp": timestamp},
                })
                try:
                    myMQTTClient.publish(iot_topic, data_scheme, 1)
                except:
                    #raise ComponentFailure('Could not publish', sensor, 'IMU')
                    print("There was a publish error IMU")
                    pass
                StoreData(data_scheme)
                print('AccX: {0:0.2f} AccY: {1:0.2f} AccZ: {2:0.2f}'.format(
                    acc_data['x'], acc_data['y'], acc_data['z']))

# Run data collection and website side-by-side
if __name__ == "__main__":
    start = Value('b', True)
    p = Process(target=GetData, args=(start,))
    p.start()
    q = Process(target=GetIMU, args=(start,))
    q.start()
    p.join()
    q.join()
