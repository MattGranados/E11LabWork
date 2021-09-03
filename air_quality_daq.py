# Air quality data acquisition 

import serial
import csv
import time

port = serial.Serial("/dev/serial0", baudrate=9600, timeout = 1.5)

text = port.read(32)

#pm1 = int.from_bytes(text[4:6], byteorder = 'big')
#pm25 = int.from_bytes(text[6:8], byteorder = 'big')
#pm10 = int.from_bytes(text[8:10], byteorder = 'big')

# units: micrograms/meter^3

header = ['Time','PM 1','PM 2.5','PM 10']

times = []
pm_1 = []
pm_25 = []
pm_10 = []

start_time = time.time()
stop_time = start_time + 60
current_time = time.time()


with open('AQISensorData.csv','w', newline = '') as csvfile:
  writer = csv.writer(csvfile, delimiter = ',')
  writer.writerow(header)
  while current_time < stop_time:
	  pm1 = int.from_bytes(text[5:7], byteorder = 'big')
	  pm25 = int.from_bytes(text[7:9], byteorder = 'big')
	  pm10 = int.from_bytes(text[9:11], byteorder = 'big')
	  current_time = time.time() 
	  
	  times.append(current_time)
	  pm_1.append(pm1)
	  pm_25.append(pm25)
	  pm_10.append(pm10)
	  
	  writer.writerow([current_time, pm1, pm25, pm10])
	  
	  time.sleep(1)
    
    #print(current_time)
    
  #writer.writerow([times, temperatures, pressure, humidity])
  print()


#void loop()
#{
  #if(Serial.find(0x42)){    //start to read when detect 0x42
    #Serial.readBytes(buf,LENG);

    #if(buf[0] == 0x4d){
      #if(checkValue(buf,LENG)){
        #PM01Value=transmitPM01(buf); //count PM1.0 value of the air detector module
        #PM2_5Value=transmitPM2_5(buf);//count PM2.5 value of the air detector module
        #PM10Value=transmitPM10(buf); //count PM10 value of the air detector module
      #}
    #}
  #}

  #static unsigned long OledTimer=millis();
    #if (millis() - OledTimer >=1000)
    #{
      #OledTimer=millis();

      #Serial.print("PM1.0: ");
      #Serial.print(PM01Value);
      #Serial.println("  ug/m3");

      #Serial.print("PM2.5: ");
      #Serial.print(PM2_5Value);
      #Serial.println("  ug/m3");

      #Serial.print("PM1 0: ");
      #Serial.print(PM10Value);
      #Serial.println("  ug/m3");
      #Serial.println();
    #}

#}
