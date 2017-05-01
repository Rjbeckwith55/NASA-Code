#!/usr/bin/python3

import socket
import RPi.GPIO as GPIO
PORT=9500
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', PORT))
s.listen(1)
s.setsockopt(socket.IPPROTO_TCP , socket.TCP_NODELAY , 1 )
conn, addr = s.accept()

GPIO.setmode(GPIO.BCM) # BCM = GPIO pins
GPIO.setwarnings(False)
GPIO.setup(05, GPIO.OUT)
GPIO.setup(06, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

#this pwm setup might change to start button initializtion
#Channel, Frequency = 50Hz
Drive = GPIO.PWM(05, 50)        
Steer = GPIO.PWM(06, 50)
Auger = GPIO.PWM(13, 50)
Slide = GPIO.PWM(19, 50)
Tilt = GPIO.PWM(26, 50)
Convey = GPIO.PWM(21,50)

#50 is no motion
Drive.start(50)
Steer.start(50)
Auger.start(50)
Slide.start(50)
Tilt.start(50)
Convey.start(0)

augerCount = 1
tiltCount = 1
conveyorCount = 1

Pause = False
try:
	while True:
		info = conn.recv(6).decode()
		#Drive Command
		if info[:2] == 'DR':
			print info
			pwm = float(info[2:])
			Drive.ChangeDutyCycle(pwm)

		#Steer Command
		if info[:2] == 'ST':
			print info
			pwm = float(info[2:])
			Steer.ChangeDutyCycle(pwm)

		#Auger Command
		if info[:2] == 'AU':
			print info
			pwm = float(info[2:])
			augerCount = augerCount + 1
			if augerCount % 2 == 0:
				Auger.ChangeDutyCycle(pwm)
			else:
				Auger.ChangeDutyCycle(50)
				print "Auger off"

		#Ballscrew Slide Command      				
		if info[:2] == 'SL':
			print info
			pwm = float(info[2:])
			Slide.ChangeDutyCycle(pwm)
	
		#Tilt Command	
		if info[:2] == 'TI':
			print info
			tiltCount = tiltCount + 1
			pwm = float(info[2:])
			if tiltCount % 2 == 0:
				Tilt.ChangeDutyCycle(pwm)
			else:
				Tilt.ChangeDutyCycle(50)
				print "Tilt off"
			
		#Conveyor Command		
		if info[:2] == 'CO':
			print info
			conveyorCount = conveyorCount + 1
			if conveyorCount % 2 == 1:
				Convey.ChangeDutyCycle(90)
			else:
				Convey.ChangeDutyCycle(50)
				print "Conveyor Off"
		if info[:2] == "PA":
			pause(s,GPIO)
		if info[:2] == 'QU':
			print info
			quit(s,GPIO)
finally:
	quit(s,GPIO)
def pause(s,GPIO):
	Drive.ChangeDutyCycle(50)
	Convey.ChangeDutyCycle(50)
	Steer.ChangeDutyCycle(50)
	Tilt.ChangeDutyCycle(50)
	Auger.ChangeDutyCycle(50)
	Slide.ChangeDutyCycle(50)
	info = " "
	while info[:2]!="PA":
		info = conn.recv(6).decode()
def quit(s,GPIO):
	Drive.ChangeDutyCycle(50)
	Convey.ChangeDutyCycle(50)
	Steer.ChangeDutyCycle(50)
	Tilt.ChangeDutyCycle(50)
	Auger.ChangeDutyCycle(50)
	Slide.ChangeDutyCycle(50)
	s.close()
	GPIO.cleanup() 
	exit(0)