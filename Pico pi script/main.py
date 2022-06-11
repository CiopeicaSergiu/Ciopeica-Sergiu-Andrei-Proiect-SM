from machine import Pin, UART
from time import sleep

led7 = Pin(6, Pin.OUT)
led6 = Pin(7, Pin.OUT)
led5 = Pin(8, Pin.OUT)
led4 = Pin(9, Pin.OUT)

led3 = Pin(10, Pin.OUT)
led2 = Pin(11, Pin.OUT)
led1 = Pin(12, Pin.OUT)
led0 = Pin(13, Pin.OUT)

leds = [led7, led6, led5, led4, led3, led2, led1, led0]
leds1 =leds[0:int(len(leds)/2)]
leds2 =leds[int(len(leds)/2):]
ser = UART(1, 9600) 
while 1:
    msg = ser.read(20)
    if msg!= None and len(msg) >3:
        myStr = msg.decode("utf-8")
        print(len(myStr))
        [status, action] = myStr.replace("\n", "").split(':')                        
        if status.lower() == "quit":
            break
        elif status.lower() == "error":
            print(action)
            if action !="":
                nr = int(action)
                c2 = nr%10
                if c2 !=nr:
                    c1 = int(nr/10)
                else:
                    c1=-1
                print(c1)
                print(c2)
                for j in range(0, 5):
                    if c1 != -1:
                        b = str(bin(c1))[2:]
                        myDiff = 4-len(b)
                        for i in range(0, len(b)):
                            if bool(int(b[i])) == True:
                                leds1[i+myDiff].high()

         
                    b = str(bin(c2))[2:]
                    myDiff = 4-len(b)
                    for i in range(0, len(b)):
                        if bool(int(b[i])) == True:
                            leds2[i-myDiff].high()
                    sleep(1)
                    for i in range(0, len(leds)):
                        leds[i].low()
                    sleep(0.2)
        elif status.lower() == "stairs":
            for i in range(len(leds)-1, -1, -1):
                leds[i].high()
                sleep(0.2)
                leds[i].low()

        elif status.lower() == "counter":
            c1 = int(action)
            for a in range(1, c1+1):
                b = str(bin(a))[2:]
                someDif = 8 - len(b)
                
                for i in range(len(b)-1, -1, -1):
                    if bool(int(b[i])) == True:
                        leds[i+someDif].high()
                
                sleep(0.5)
                
                for i in range(0, len(leds)):
                    leds[i].low()
        elif status.lower() == "led":
            c1 = int(action)
            if 0<=c1 and c1 <len(leds):
                print('Led: '+str(c1)+"high")
                leds[len(leds)-c1-1].high()
                sleep(1)
                leds[len(leds)-c1-1].low()
        msg = None


        
    



