#import libraries
import RPi.GPIO as GPIO
import time
#GPIO Basic initialization
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Use a variable for the  Pin to use
#If you followed my pictures, it's port 7 => BCM 4
led1 = 4
led2 = 17
led3 = 22
#Initialize your pin
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)
#Turn on the LED
print ("LED on")
GPIO.output(led1,1)
GPIO.output(led2,1)
GPIO.output(led3,1)
#Wait 5s
time.sleep(3)
#Turn off the LED
print ("LED off")
GPIO.output(led1,0)
GPIO.output(led2,0)
GPIO.output(led3,0)
