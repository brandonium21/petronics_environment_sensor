# petronics_environment_sensor
Blah Blah environment sensor

#dependencies:

## Install AWS IOT SDK
```
pip3 install AWSIoTPythonSDK
```

## Install DHT library
```
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
```
```
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl
```
```
sudo python setup.py install
```

## Install mpu6050
```
sudo apt-get install python-smbus
sudo pip3 install mpu6050-raspberrypi
```

# Test 
Run 
```
python3 iot_test.py
```
