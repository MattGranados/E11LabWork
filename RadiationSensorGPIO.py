import RPi.GPIO as GPIO  
import time     # this lets us have a time delay 
import sys
import csv


count = 0

def callback_final(interval, detect_time, delay, title):
  header = ['Time', '# of Counts Detected within Interval', 'CPM within Interval']
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
  counts_int = []  
  CPM_int = []
  
  time.sleep(delay)
  
  start_time = time.time()
  current_time = time.time()
  
  #sleep(detect_time)         # wait 30 seconds  
   
   
     #print("\n")
  #print(str(count) + " counts detected in total") 
  
  #print(str(CPS) + " Counts per Second")
  
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
            
      writer.writerow([current_time, interval_count, interval_CPM])
      time.sleep(interval)
      
      print(current_time, interval_count, interval_CPM)
      
      
    print()
    print("\n")
    
    tot_counts = sum(counts_int)
    print("Total Counts = " + str(tot_counts))
    min_int = detect_time / 60
    print("Overall CPM = " + str(tot_counts/min_int))
  
      
    
  #finally:                   # this block will run no matter how the try block exits  
  GPIO.cleanup()         # clean up after yourself  

interval = int(sys.argv[1]) 
detect_time = int(sys.argv[2]) 
delay = int(sys.argv[3]) 
title = sys.argv[4]

callback_final(interval, detect_time, delay, title)
  
