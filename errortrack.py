import logging
import datetime
import Adafruit_DHT
from mpu6050 import mpu6050

logfile = "/home/pi/Desktop/operationlog.log"
logging.basicConfig(filename=logfile,level=logging.DEBUG)

class ComponentFailure(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self, cause, sensor_obj, sensor)
        fail_type = 'VibrationFailure'
        time_of_fail = datetime.datetime.now()
        logging.error('{}: {} - {}'.format(fail_type, time_of_fail, cause))
        attempt = 0

        # check if sensor has output
        while attempt < 3:
        	if sensor_obj.get_temp():
        		logging.info('Sensor Output: {} - {}'.format(datetime.datetime.now(), sensor_obj.get_temp()))
        		break
        	else:
        		attempt += 1
        		logging.error('Sensor Output: {} - {} - attempt: {}'.format(datetime.datetime.now(), 'No Output', attempt))		
        		# Send to aws IOT
        if attempt >= 3:
        	#reboot pi
        	pass

'''
class EnviormentFailure(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class NetworkFailure(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

'''