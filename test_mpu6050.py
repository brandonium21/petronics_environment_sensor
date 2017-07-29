#!/usr/bin/python
from mpu6050 import mpu6050

sensor = mpu6050(0x68)

while True:

    acc_data = sensor.get_accel_data()

    print 'AccX: {0:0.4f} AccY: {1:0.4f} AccZ: {2:0.4f}'.format(acc_data['x'],acc_data['y'],acc_data['z'])

