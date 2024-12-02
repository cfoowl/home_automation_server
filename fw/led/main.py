import machine
import time
led = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(5, machine.Pin.OUT)
while True:
    led.value(1)
    led2.value(0)
    time.sleep(1)
    led.value(0)
    led2.value(1)
    time.sleep(1)
