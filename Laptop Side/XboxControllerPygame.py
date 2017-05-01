#Nasa-bot drive code written in pygame
import time
import socket
import pygame

"""Packet Meanings:
	DR = Drive
	ST = Steer(Actuator)
	AU = Auger
	TI = Tilt(Actuators)
	SL = BallsScrew Slide
	CO = Conveyor
	"""

def stop():
        pygame.joystick.quit()
        pygame.quit()
        print("Clean exit")
        

def main():
    print("main")
    #Control upadate frequency
    CLOCK = pygame.time.Clock()
    clock_speed = 20

    #vars for if joystick is connected and program is running
    joystick_connect = True
    running = True

    #Establish socket connections
    HOST = '192.168.1.18'
    PORT = 9500
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print("Connection to " + HOST + " was successful")

    pygame.init()
    #use first joystick connected since only
    #one xbox remote is used
    joystick = pygame.joystick.Joystick(0)
    print("joystick")
    #initailize joystick
    joystick.init()
    pwmst = 50.0
    pwmdr = 50.0
    #Bools for motion
    SlR = True
    SlL = True
    
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYAXISMOTION:
                
                #Steering command on the top left axis left and right direction
                if joystick.get_axis(0) > .1 or joystick.get_axis(0) < -.1:
                    pwmst = (-(joystick.get_axis(0)) + 1) / .02
                    pwmst = round(pwmst,0)
                    if pwmst > 90:
                        pwmst = 90.0
                    elif pwmst < 10:
                        pwmst = 10.0
                    Str="ST"
                    Send(pwmst,s,Str)
                elif joystick.get_axis(0) < .1 and joystick.get_axis(0) > -.1 and pwmst != 50.0:
                    pwmst=50.0
                    Str="ST"
                    Send(pwmst,s,Str)

                #Conveyor Belt control using the X button
                if joystick.get_button(2) != 0:
                    Str = "CO"
                    Send(90.0,s,Str)

               #Auger control using the A button
                if joystick.get_button(0) != 0:
                    Str = "AU"
                    Send(40.0,s,Str)
                
                #Auger control using B button
                if joystick.get_button(1) != 0:
                    Str = "AU"
                    Send(60.0,s,Str)
                
                #Ballscrew slide using the left stick Left
                if joystick.get_axis(2) > .1:
                    Str = "SL"
                    Send(70.0,s,Str)
                    SlL = True
                elif joystick.get_axis(2) < .1 and Sl:
                    SlL = False
                    Str = "SL"
                    Send(50.0,s,Str)

                #Ballscrew slide using right stick Right
                if joystick.get_axis(2) < -.5:
                    Str = "SL"
                    Send(30.0,s,Str)
                    SlR = True
                elif joystick.get_axis(2) > -.1 and Sl:
                    Str = "SL"
                    SlR = False
                    Send(50.0,s,Str)

                #Tilt using left bumper
                if joystick.get_button(4) != 0:
                    Str = "TI"
                    Send(10.0,s,Str)

                #Tilt using right bumper
                if joystick.get_button(5) != 0:
                    Send(90.0,s,Str)
                
                #Drive command using top left stick up and down
                if joystick.get_axis(1) < -.1 or joystick.get_axis(1) > .1:
                    pwmdr = (joystick.get_axis(1) + 1) / .02      
                    pwmdr = round(pwmdr,0)
                    if pwmdr > 90:
                        pwmdr = 90.0
                    elif pwmdr < 10:
                        pwmdr = 10.0
                    Str = "DR"
                    Send(pwmdr,s,Str)
                elif joystick.get_axis(1) < .1 and joystick.get_axis(1) > -.1 and pwmdr != 50.0:
                    Str = "DR"
                    pwmdr = 50.0
                    Send(pwmdr,s,Str)

                #Exit program if start button is pressed
                if joystick.get_button(7):
                    running = False
                #Pause the program when select is pressed
                if joystick.get_button(6):
                    Str="PA"
                    print ("Paused press select again to unpause")
                    Send(50.0,s,Str)

    print("Stopping")
    msg = "QU" + str(50.0)
    s.send(msg)
    s.close()
    stop()
def Send(pwm,s,Str):
    msg = Str + str(pwm)
    print(msg)
    send = msg.encode()
    s.send(send)


   
main()
