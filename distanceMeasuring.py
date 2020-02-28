#Libraries
import RPi.GPIO as GPIO
import time
import urllib2


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 00
GPIO_ECHO = 02
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
global dist
def distance():
    print ("At starting of the function")
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime when the ultrasonic wave is sent
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival of ultrasonic wave
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2
    distance = (TimeElapsed * 34300) / 2
    print ("At end of the distance")
 
    return distance
	
if __name__ == '__main__':
    try:
        while 1:
            print ("Inside while loop")
			#Call distance function.
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
			#wait 20 seconds
            time.sleep(20)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
