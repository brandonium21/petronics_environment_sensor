import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import uuid
import datetime
import json
from random import randint

def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

host = "a1la3qkft0cvmg.iot.us-east-2.amazonaws.com"
myMQTTClient = AWSIoTMQTTClient("factory_sensor")
myMQTTClient.configureEndpoint(host, 8883)
myMQTTClient.configureCredentials("mqtt_res2/VeriSign-Class 3-Public-Primary-Certification-Authority-G5.crt", 
	"mqtt_res2/factory_sensor.private.key", 
	"mqtt_res2/factory_sensor.cert.pem")

'''
# AWSIoTMQTTClient connection configuration
myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
'''
myMQTTClient.connect()
node = str(uuid.uuid4())
timestamp = str(datetime.datetime.now())
data_scheme = json.dumps({
		"temperature": {"value": randint(30, 60), "node": node, "timestamp": timestamp},
		"humidity": {"value": randint(20, 90), "node": node, "timestamp": timestamp},
		"accx": {"value": randint(1, 10), "node": node, "timestamp": timestamp},
		"accy": {"value": randint(1, 10), "node": node, "timestamp": timestamp},
		"accz": {"value": randint(1, 10), "node": node, "timestamp": timestamp},
		"sensorTemp": {"value": randint(20, 90), "node": node, "timestamp": timestamp},
	}
)
#print(data_scheme)
myMQTTClient.subscribe('factoryiot', 1, customCallback)
print myMQTTClient.publish("factoryiot", data_scheme, 1)
time.sleep(2)
myMQTTClient.disconnect()
