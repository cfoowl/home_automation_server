# Pin connection
#   Alarm
#       in -> 25

import machine
import time

# Alarm
a = machine.Pin(25, machine.Pin.IN)
a.value(0)
exit(0)

while True:
    a.value(1)
    time.sleep(30/1000)
    a.value(0)
    time.sleep(60/1000)
