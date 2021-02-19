# Client (Raspberry Pi - Requesting Data)

# import the necessary packages
import time
import RPi.GPIO as GPIO
import math
import pygame
import os
from time import sleep
import sys
import socket

# Initialization --------------------------------------------

# initialize button
BUTTON_GPIO = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pressed = False

# initialize relay (on/off)
onOff = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(onOff, GPIO.OUT)

# initialize relay (intensity)
Intensity = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(Intensity, GPIO.OUT)

# Function Definitions ---------------------------------------

def relay_on(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn relay on

def relay_off(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn relay off

def relay_OnOff():
    relay_on(onOff)
    time.sleep(0.1)
    relay_off(onOff)
    time.sleep(0.1)
    relay_on(onOff)

def relay_Intensity(intens):
    for i in range(intens):
        relay_on(Intensity)
        time.sleep(0.1)
        relay_off(Intensity)
        time.sleep(0.1)

def healthToIntensity(life, save):
    life = int(life)
    count = 0
    #determine the intensity
    for i in range(100,0,-20):
        count +=1
        if life==100:
            intensity=0
        if life>i-20 and life<=i:
            intensity=count

    if save<=intensity:
        relay_Intensity(intensity-save)
    else:
        relay_OnOff()
        time.sleep(0.1)
        relay_OnOff()
        relay_Intensity(intensity)

    return intensity


def main_loop():
    save_val = 0
    HOST =  '192.168.43.49'
    PORT = 65436  # Port (same as Client)
    print("Listening on " + str(HOST) + ":" + str(PORT))
    relay_OnOff()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                #detect button, changes state of electical box
                if not GPIO.input(BUTTON_GPIO):
                     relay_OnOff()

                if data.decode() != "":
                    health = data.decode('utf-8')
                    try:
                        save_val = healthToIntensity(health,save_val)
                    except:
                        continue
    
main_loop()

