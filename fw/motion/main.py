# Pin connection
#   Motion sensor
#       out -> 22
#       !!! 5V power supply !!!
#   Leds
#       Red -> 4
#       Green -> 5

import machine
import time

# Motion sensor
m = machine.Pin(22, machine.Pin.IN)

# Leds
lg = machine.Pin(5, machine.Pin.OUT)
lr = machine.Pin(4, machine.Pin.OUT)

c = 0
while True:
    if m.value():
        lg.value(1)
        lr.value(0)
    else:
        lg.value(0)
        lr.value(1)
    time.sleep(0.1)
