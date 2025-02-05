# Pin connection
#   Alarm
#       in -> 25

import machine
import time

# Alarm
a = [machine.Pin(i, machine.Pin.IN) for i in range(35)]
for aa in a:
    aa.value(1)
while True:
    time.sleep(1)
    pass

exit(0)

while True:
    a.value(1)
    time.sleep(30/1000)
    a.value(0)
    time.sleep(1000/1000)
