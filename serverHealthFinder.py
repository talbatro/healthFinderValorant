# Server (Computer - Sending data)

import socket
import time
import numpy as np
import pytesseract
import math
import cv2
from mss import mss
import keyboard
from datetime import datetime

# Function Definitions --------------------------------------------------

# convert image to text with ocr
def ocr_core(img):
    config = "--psm 6"
    text = pytesseract.image_to_string(img, config=config)
    return text

# image processing
def get_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def thresholding(img):
    return cv2.threshold(img, 190, 255, cv2.THRESH_BINARY_INV)[1]

def remove_noise(img):
    return cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

# scan text to return only numeric values   
def scan(text):
    d = ""
    for i in range(len(text)):
        if text[i].isnumeric():
            d += text[i]
    return d

# write values + timestamp to txt file
def writeDataToFile(value):
    with open('valuesTimestamp.txt', 'w') as f:
        for item in value:
            f.write("%s\n" % item)

# Main Program Loop --------------------------------------------------

def main_loop():

    # Socket connection initialization -------------------------------
    
    HOST = '192.168.43.49'  # IP adress (should be same as client)
    PORT = 65436  # Port number (should be same as client)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    print("Connection/Search launched...")

    # initialize variables
    oldHealth = "100"
    fileValues = []

    while True:
        
        sct_img = sct.grab(bounding_box)

        frame = np.array(sct_img)
        
        frame = remove_noise(frame)
        frame = get_grayscale(frame)
        frame = thresholding(frame)

        newHealth = ocr_core(frame)
        newHealth = scan(newHealth)

        if newHealth != oldHealth:

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            
            fileValues.append([newHealth, current_time])

            oldHealth = newHealth

            # encode data and send it to client
            value = str(newHealth).encode('utf-8')
            s.sendall(value)

        # stop program with 'm' 
        if keyboard.is_pressed('m'):
            writeDataToFile(fileValues)
            s.close()
            break
        else:
            pass

# tell where tesseract OCR is located (download it if not already there)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# define size and location of window to be used
height = 1080
width = 1920
[x, y] = 560, height - 90
[h, w] = 70, 90
bounding_box = {'top': y, 'left': x, 'width': w, 'height': h}

# launch "Multiple ScreenShots" module
sct = mss()

# start program with "p"
while True:
        if keyboard.is_pressed('p'):
            break
        else:
            pass

main_loop()
