from tkinter import *
from tkinter import ttk
from tkinter import font
from gtts import gTTS
import os
import datetime
import speech_recognition as sr
import RPi.GPIO as GPIO
import time
import readchar
import smbus
import math
import threading

global endTime

TRIGGER_PIN = 22
ECHO_PIN    = 36
LED_PIN=15
Motor_R1_Pin = 16
Motor_R2_Pin = 18
Motor_L1_Pin = 37
Motor_L2_Pin = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(Motor_R1_Pin, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(Motor_R2_Pin, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(Motor_L1_Pin, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(Motor_L2_Pin, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(LED_PIN,GPIO.OUT)
GPIO.setup(TRIGGER_PIN,  GPIO.OUT)
GPIO.setup(ECHO_PIN,     GPIO.IN)
GPIO.output(TRIGGER_PIN, GPIO.LOW)
v = 343 # (331 + 0.6*20)
t = 0.5

address=0x48
bus=smbus.SMBus(1)
cmd=0x40

cmd1="come here"
cmd2="go away"
cmd3="set up"

    
def show_time():
    # Get the time remaining until the event
    remainder = endTime - datetime.datetime.now()
    # remove the microseconds part
    remainder = remainder - datetime.timedelta(microseconds=remainder.microseconds)
    if(remainder.seconds==0):
        root.destroy()
        while True:
            value=analogRead(0)
            print (value)
            
            if (value<200):
                thread1 = threading.Thread(target=music)
                thread2 = threading.Thread(target=led)
                
                thread2.setDaemon(False)
                thread1.start()
                thread2.start()
                
                
            else:
                print("LED is off")
                GPIO.output(LED_PIN,GPIO.LOW)
                break
            
            time.sleep(1)
             
    else:
        # Show the time left
        txt.set(remainder)
        # Trigger the countdown after 1000ms
        root.after(1000, show_time)

def music():
    os.system('omxplayer alarm_clock.mp3 > /dev/null 2>&1')
    time.sleep(0.1)
           
def led():
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(LED_PIN, GPIO.LOW)
    time.sleep(0.5)
    
            
        

def record():
    global audio
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        #listen for 1 seconds and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say something!")
        audio=r.listen(source)
        
def car():
    for i in range(10):
        photoresistor()
        time.sleep(0.1)
        distance = measure_average()
        print("Distance: %.1f (cm)" % distance)
        if(distance>30):
            forward()
            time.sleep(0.1)
        elif(distance<=15):
            stop()
            backward()
        else:
            turnLeft()
            turnRight()
            forward()
            
        time.sleep(0.1)
        
def stop():
    print("stop")
    GPIO.output(Motor_R1_Pin, False)
    GPIO.output(Motor_R2_Pin, False)
    GPIO.output(Motor_L1_Pin, False)
    GPIO.output(Motor_L2_Pin, False)

def backward():
    print("backward")
    GPIO.output(Motor_R1_Pin, False)
    GPIO.output(Motor_R2_Pin, True)
    GPIO.output(Motor_L1_Pin, False)
    GPIO.output(Motor_L2_Pin, True)
    time.sleep(t)
    stop()


def forward():
    print("forward")
    GPIO.output(Motor_R1_Pin, True)
    GPIO.output(Motor_R2_Pin, False)
    GPIO.output(Motor_L1_Pin, True)
    GPIO.output(Motor_L2_Pin, False)
    time.sleep(t)
    stop()


def turnRight():
    print("right")
    GPIO.output(Motor_R1_Pin, True)
    GPIO.output(Motor_R2_Pin, False)
    GPIO.output(Motor_L1_Pin, False)
    GPIO.output(Motor_L2_Pin, False)
    time.sleep(t)
    stop()

def turnLeft():
    GPIO.output(Motor_R1_Pin, False)
    GPIO.output(Motor_R2_Pin, False)
    GPIO.output(Motor_L1_Pin, True)
    GPIO.output(Motor_L2_Pin, False)
    time.sleep(t)
    stop()
         
def measure() :
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)# 10uS 
    GPIO.output(TRIGGER_PIN, GPIO.LOW)
    pulse_start = None
    pulse_end   = None

    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()

    t = pulse_end - pulse_start

    d = t * v
    d = d/2

    return d*100


def measure_average() :
    d1 = measure()
    time.sleep(0.05)
    d2 = measure()
    time.sleep(0.05)
    d3 = measure()
    distance = (d1 + d2 + d3) / 3
    return distance

def photoresistor():
    value=analogRead(0)
    print (value)
    if(value<200):
        print("LED is off")
        GPIO.output(LED_PIN,GPIO.LOW)
        time.sleep(0.1)
    else:
        print("LED is on")
        GPIO.output(LED_PIN,GPIO.HIGH)
        time.sleep(0.1)
        
    time.sleep(0.01)
    
    
def analogRead(chn):
    value=bus.read_byte_data(address,cmd+chn)
    return value

def analogWrite(value):
    bus.write_byte_data(address,cmd,value)


# recognize speech using Google Speech Recognition
try:
    while True:
        print("請選擇模式(1-鬧鐘，2-互動): ")
        ans=input()
        
        if ans=='1':
            # Set the end date and time for the countdown
            print("鬧鐘模式，請輸入:")
              # Use tkinter lib for showing the clock
    
            print("Month")
            mon=input()
            print("Day")
            day=input()
            print("Hour")
            hour=input()
            print("Minute")
            mins=input()

            endTime = datetime.datetime(2022, int(mon), int(day), int(hour), int(mins), 0)

            root = Tk()
            root.attributes("-fullscreen", True)
            root.configure(background='black')
            root.bind("x", quit)
            root.after(1000, show_time)
            

            fnt = font.Font(family='Helvetica', size=60, weight='bold')
            txt = StringVar()
            lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="red", background="black")
            lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

            root.mainloop()
            
        elif ans=='2':
            print("互動模式")
            while True:
                r=sr.Recognizer()
                record()
                time.sleep(0.7)
                print("Google Speech Recognition thinks you said:")
                print(r.recognize_google(audio, language='en-US'))
                if(r.recognize_google(audio, language='en-US')==cmd1):
                    os.system('omxplayer cat.mp3 > /dev/null 2>&1')
                    stop()
                    time.sleep(0.5)
                    for i in range(9):
                        turnRight()
                    time.sleep(1)
                elif(r.recognize_google(audio, language='en-US')==cmd2):
                    os.system('omxplayer cat.mp3 > /dev/null 2>&1')
                    car()
                    time.sleep(0.1)
                elif(r.recognize_google(audio, language='en-US')==cmd3):
                    stop()
                    break
                    
            time.sleep(0.01)
        
                
                
          
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
    
except sr.RequestError as e:
    print("No response from Google Speech Recognition service: {0}".format(e))
    GPIO.output(Motor_R1_Pin, False)
    GPIO.output(Motor_R2_Pin, False)
    GPIO.output(Motor_L1_Pin, False)
    GPIO.output(Motor_L2_Pin, False)

except KeyboardInterrupt:
    print("Exception: KeyboardInterrupt")

finally:
    GPIO.cleanup()



                             

    
