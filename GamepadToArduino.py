from inputs import get_gamepad
import socket

arduino = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
arduino.connect(('192.168.0.66', 80))

class GPData:
    def __init__(self):
        self.leftTrigger = 0
        self.rightTrigger = 0
        self.JS_x = 0

data = GPData()
lastSent = ""

while 1:
    events = get_gamepad()
    for event in events:
        #print(event.code, event.state) 
        if(event.code == "ABS_RZ" and event.state == 255):
            print("Right trigger pressed")
            data.rightTrigger = 1

        elif(event.code == "ABS_RZ" and event.state == 0):
            print("Right trigger released")
            data.rightTrigger = 0

        elif(event.code == "ABS_Z" and event.state == 255):
            print("Left trigger pressed")
            data.leftTrigger = 1

        elif(event.code == "ABS_Z" and event.state == 0):
            print("Left trigger released")
            data.leftTrigger = 0

        elif(event.code == "ABS_X" and event.state > 0):
            print("JS Right")
            data.JS_x = 1

        elif(event.code == "ABS_X" and event.state < 0):
            print("JS Left")
            data.JS_x = -1

        elif(event.code == "ABS_X" and event.state == 0):
            print("JS Center")
            data.JS_x = 0


    strData = ""
    my_bytes = bytearray()

    #String data format BFLR (Backwards, forwards, left, right) 

    strData += str(data.leftTrigger) + str(data.rightTrigger)

    if(data.JS_x == 1):
        strData += "01"
    elif((data.JS_x == -1)):
        strData += "10"
    else:
        strData += "00"

    for x in strData:
        my_bytes.append(ord(x))

    if(strData != lastSent):
        arduino.sendall(my_bytes)
        lastSent = strData
    