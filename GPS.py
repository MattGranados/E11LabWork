import gps
import time
import csv
import sys

# Listen on port 2947 (gpsd) of localhost
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
       
def GPS_Data(interval, sleep_time, delay, title):
    header = ['Time','Latitude','Longitude']
    
    times = []
    lat_dat = []
    long_dat = []  
        
    time.sleep(delay)
    
    start_time = time.time()
    current_time = time.time()   

         
    with open(title,'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(header)
        while current_time < start_time + interval:
            try:
                report = session.next()
                if report['class'] == 'TPV':
                    if hasattr(report, 'time', 'lat', 'lon'):
                        timef = report.time
                        latitude = report.lat
                        longitude = report.lon
                    
                        current_time = time.time()    
                        times.append(timef)
                        lat_dat.append(latitude)
                        long_dat.append(longitude)
                    
                        writer.writerow([timef, latitude, longitude])
                        time.sleep(sleep_time)
                        print(timef, latitude, longitude)
            except:
                pass
        print()
                
                    
        
  
  
#print()
interval = int(sys.argv[1])
sleep_time = int(sys.argv[2])
delay = int(sys.argv[3])
title = sys.argv[4]  

GPS_Data(interval,sleep_time,delay,title)
