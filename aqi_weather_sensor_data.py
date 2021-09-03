import csv
import time
import serial
import sys
import board
from adafruit_bme280 import basic as adafruit_bme280

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
port = serial.Serial("/dev/serial0", baudrate=9600, timeout = 1.5)
text = port.read(32)


header = ['Time','Temperature','Pressure','Humidity','PM 1','PM 2.5','PM 10']

times = []
temperatures = []
pressure = []
humidity = []
pm_1 = []
pm_25 = []
pm_10 = []

start_time = time.time()
current_time = time.time()

interval = 10
sleep_time = 1

if len(sys.argv) > 1:
	interval = int(sys.argv[1])
	if len(sys.argv) > 2:
		sleep_time = int(sys.argv[2])
		
with open('AQIWeatherSensorData.csv','w', newline = '') as csvfile:
  writer = csv.writer(csvfile, delimiter = ',')
  writer.writerow(header)
  while current_time < start_time + interval:
    temp = bme280.temperature
    press = bme280.pressure
    humid = bme280.relative_humidity
    pm1 = int.from_bytes(text[5:7], byteorder = 'big')
    pm25 = int.from_bytes(text[7:9], byteorder = 'big')
    pm10 = int.from_bytes(text[9:11], byteorder = 'big')
    current_time = time.time() 
    
    times.append(current_time)
    temperatures.append(temp)
    pressure.append(press)
    humidity.append(humid)
    pm_1.append(pm1)
    pm_25.append(pm25)
    pm_10.append(pm10)
    
    writer.writerow([current_time, temp, press, humid, pm1, pm25, pm10])
    time.sleep(sleep_time)
    
    #print(current_time)
    
  print()
  

