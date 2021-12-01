#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import time
import serial
import sys
import board
from adafruit_bme280 import basic as adafruit_bme280
import RPi.GPIO as GPIO

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
port = serial.Serial("/dev/serial0", baudrate=9600, timeout = 1.5)
text = port.read(32)


#header = ['Time','Temperature','Pressure','Humidity','PM 1','PM 2.5','PM 10']

#times = []
#temperatures = []
#pressure = []
#humidity = []
#pm_1 = []
#pm_25 = []
#pm_10 = []

#start_time = time.time()
#current_time = time.time()


count = 0

def AQIWeather_Radiation_SensorData(interval, detect_time, delay, title):
  header = ['Time','Temperature','Pressure','Humidity','PM 1','PM 2.5','PM 10','Counts within Interval','CPM within Interval']
  
  GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
  GPIO.setup(17, GPIO.IN)    # set 3V3 as input (button)

  # Define a threaded callback function to run in another thread when events are detected  
  #count = 0
  def my_callback(channel):  
    if GPIO.input(17):     # if pin 17 == 1
      global count
      count += 1
      #print(str(count) + ": Rising edge detected on 3V3")
    
  # when a changing edge is detected on pin 17, regardless of whatever   
  # else is happening in the program, the function my_callback will be run  
  GPIO.add_event_detect(17, GPIO.RISING, callback=my_callback)

  times = []
  temperatures = []
  pressure = []
  humidity = []
  pm_1 = []
  pm_25 = []
  pm_10 = []
  
  counts_int = []  
  CPM_int = []

  time.sleep(delay)
  
  start_time = time.time()
  current_time = time.time()

  
  
    
  with open(title,'w', newline = '') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',')
    writer.writerow(header)
    while current_time < start_time + detect_time:
      global count
      count = count
      
      interval_count = count
      interval_CPM = interval_count / (interval/60)
      current_time = time.time() 
      
      times.append(current_time)
      counts_int.append(interval_count)
      CPM_int.append(interval_CPM)
      
      count = 0
    
      temp = bme280.temperature
      press = bme280.pressure
      humid = bme280.relative_humidity
      pm1 = int.from_bytes(text[4:6], byteorder = 'big')
      pm25 = int.from_bytes(text[6:8], byteorder = 'big')
      pm10 = int.from_bytes(text[8:10], byteorder = 'big')
      current_time = time.time() 
      
      #times.append(current_time)
      temperatures.append(temp)
      pressure.append(press)
      humidity.append(humid)
      pm_1.append(pm1)
      pm_25.append(pm25)
      pm_10.append(pm10)
      
      writer.writerow([current_time, temp, press, humid, pm1, pm25, pm10, interval_count, interval_CPM])
      time.sleep(interval)
    
      #print(current_time, temp, press, humid, pm1, pm25, pm10, interval_count, interval_CPM)
    print()
    print("\n")
    
    tot_counts = sum(counts_int)
    print("Total Counts = " + str(tot_counts))
    min_int = detect_time / 60
    print("Overall CPM = " + str(tot_counts/min_int))
  
      
    
  #finally:                   # this block will run no matter how the try block exits  
  GPIO.cleanup()         # clean up after yourself 
    
#if len(sys.argv) > 1:
interval = int(sys.argv[1])
    #if len(sys.argv) > 2:
detect_time = int(sys.argv[2])
delay = int(sys.argv[3])
title = sys.argv[4]          

AQIWeather_Radiation_SensorData(interval,sleep_time,delay,title)

