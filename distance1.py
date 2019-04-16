#Libraries
import RPi.GPIO as GPIO
import time
import smtplib
import urllib2

#Things Speak API Key
myAPI = '9NZUVOA1794DLDIQ' 

#Things Speak URL where we will send the data.
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
global i
global dist1
def distance():
    print ("At starting of the function")
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    print ("At end of the distance")
 
    return distance
def sendemail(i):
    
    server = smtplib.SMTP_SSL('smtp.zoho.com', port=465)
    print("Server Started...")
    server.login('satishreddym@zoho.com','Aosproject100')
    print("Server Login Successful")
    msg ="""From:satishreddym@zoho.com\nTo:satish.reddy617@gmail.com\nSubject: Alert Email\n
   """
    numb=str(i)
    msg = msg+" Warning No:"+numb+"Quantity below the Threshold level for Warning 1"+numb

    try:
        server.sendmail('satishreddym@zoho.com','satish.reddy617@gmail.com',msg)
    except:
        return server

    print("Sending Message...")
    server.quit()
    print("Quit Server")
    # Sending the data to thingspeak
    conn = urllib2.urlopen(baseURL + '&field1=%s' % (i))
    print conn.read()
    # Closing the connection
    conn.close()
dist1=0 
if __name__ == '__main__':
    try:
        print ("Program is executing")
        i=1
        while 1:
            print ("Inside while loop")
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            if dist>7 and abs(dist1-dist)>1:
                print("Inside Sending Email if")
                sendemail(i)
                i=i+1
                dist1=dist
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
