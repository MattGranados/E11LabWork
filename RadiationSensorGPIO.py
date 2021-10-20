import RPi.GPIO as GPIO  
from time import sleep     # this lets us have a time delay 
import sys

count = 0

def callback_final(detect_time):  
  GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
  GPIO.setup(17, GPIO.IN)    # set 3V3 as input (button)  
    
  # Define a threaded callback function to run in another thread when events are detected  
  #count = 0
  def my_callback(channel):  
    if GPIO.input(17):     # if pin 17 == 1
      global count
      count += 1
      print(str(count) + ": Rising edge detected on 3V3") 
    
  
  
  # when a changing edge is detected on pin 17, regardless of whatever   
  # else is happening in the program, the function my_callback will be run  
  GPIO.add_event_detect(17, GPIO.RISING, callback=my_callback)  
  
  sleep(detect_time)         # wait 30 seconds  
   
  print("\n")
  print(str(count) + " counts detected in total") 
  
  CPS = count/detect_time
  print(str(CPS) + " Counts per Second")    
    
  #finally:                   # this block will run no matter how the try block exits  
  GPIO.cleanup()         # clean up after yourself  
  
detect_time= int(sys.argv[1])
callback_final(detect_time)
  
