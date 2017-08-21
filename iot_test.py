import ssl
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import uuid
import datetime

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


# AWSIoTMQTTClient connection configuration
myMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()
data_scheme = {
	"point": str(uuid.uuid4()),
	"timestamp": datetime.datetime.now(),
	"data": {
		"environmental":{
			"temperature": 0.0,
			"humidity": 0.0,
			"timestamp": ''
		},
		"accelerometer":{
			"accx": 0.0,
			"accy": 0.0,
			"accz": 0.0,
			"temperature": 0.0,
			"timestamp": ''
		}
	}
}
myMQTTClient.subscribe('factoryIot', 1, customCallback)
myMQTTClient.publish("factoryIot", str(data_scheme), 1)

time.sleep(2)
