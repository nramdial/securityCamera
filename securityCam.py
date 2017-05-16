import datetime
import os
import smtplib
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import RPi.GPIO as GPIO
import picamera

from photoresistor import rc_time


# This method rotates the servo motor 3 times  to take pictures in each direction
def turnMotor(servo, position):
    if position == 1:
        servo.ChangeDutyCycle(7.5)
        print "This is 7.5"
    elif position == 2:
        servo.ChangeDutyCycle(9.5)
        print "This is 9.5"
    elif position == 3:
        servo.ChangeDutyCycle(5.5)
        print "This is 5.5"
    else:
        return False

    time.sleep(.5)
    return True


def sendGroupMsg(fileDir, email_to, email_from, password, mmsaddr, picdatetime, imagelist):
    # Initialize and fill MIME message
    msg = MIMEMultipart()
    msg['Subject'] = "ENTRANCE DETECTED: PICTURES TAKEN"
    msg['From'] = email_from
    msg['To'] = email_to
    msg.attach(MIMEText("SECURITY IMAGES TAKEN ON " + picdatetime, 'plain'))

    # Set up connection to SMTP server
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()  # Check the smtp connection wit telnet session
    mail.starttls()  # Secure connection with SSL/TLS
    mail.login(email_from, password)

    # Attach images and send MMS
    for i, img in enumerate(imagelist):
        filestr = 'piccapture' + str(i) + '.jpg'
        msg.attach(MIMEImage(img, name=os.path.basename(fileDir + filestr)))
        # Send MMS with individual images
        sendMMS(filestr, email_from, mmsaddr, picdatetime, img, mail)

    # Send the email with grouped images
    mail.sendmail(email_from, email_to, msg.as_string())
    mail.quit()


def sendMMS(fileDir, email_from, mmsaddr, picdatetime, image, mail):
    # Initialize and fill MIME message
    msg = MIMEMultipart()
    msg['Subject'] = "ENTRANCE DETECTED: PICTURES TAKEN"
    msg['From'] = email_from
    msg.attach(MIMEText("SECURITY IMAGES TAKEN ON " + picdatetime, 'plain'))
    msg.attach(MIMEImage(image, name=os.path.basename(fileDir)))

    # Send message on already opened connection
    mail.sendmail(email_from, mmsaddr, msg.as_string())


def snapAndSend(fileDir, servomotor, camera):
    imagelist = []
    for i in range(1, 4):
        if not turnMotor(servomotor, i):
            print "Motor turning function failed!!!"

        filestr = 'piccapture' + str(i) + '.jpg'
        camera.capture(filestr)
        img = open(fileDir + filestr, 'rb').read()
        imagelist.append(img)

    return imagelist, str(datetime.datetime.now())


def main():
    # WE NEED TRY/CATCH STATEMENTS FOR USER INPUTS

    # SET FILE DIRECTORY
    fileDir = "/home/pi/Desktop/CSE4709_Project/NATHAN/"

    # SETUP AND CONFIGURE PINS
    GPIO.setmode(GPIO.BOARD)

    print "What pin is the servomotor connected to?"
    servopin = int(raw_input())
    GPIO.setup(servopin, GPIO.OUT)

    print "What pin is the photosensor connected to?"
    photospin = int(raw_input())

    # SET SERVO TO USER DEFINED PIN
    smotor = GPIO.PWM(servopin, 50)
    smotor.start(0)

    # INITIALIZE PI CAMERA
    camera = picamera.PiCamera()

    # SET UP CONTACTS
    email_from = "Insert From-email address here"
    password = "Insert email password here"

    print "What is the destination email?"
    email_to = raw_input()

    print "What is your number?"
    mmsnumber = raw_input()

    options = {1: "@vzwpix.com",
               2: "@mms.att.net",
               3: "@tmomail.net",
               4: "@pm.sprint.com"}
    print "What is your carrier?"
    print "Choose one: \n 1. Verizon \n 2. AT&T \n 3. T-Mobile \n 4. Sprint"
    mmscarrier = int(raw_input())

    mmsaddr = mmsnumber + options[mmscarrier]

    try:
        while True:
            lightlevel = rc_time(photospin)

            if lightlevel < 200:
                imagelist, picdatetime = snapAndSend(fileDir, smotor, camera)
                sendGroupMsg(fileDir, email_to, email_from, password, mmsaddr, picdatetime, imagelist)

    except KeyboardInterrupt:

        # CLEAN UP
        smotor.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    main()
