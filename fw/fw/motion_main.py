import network
import machine
import time
from umodbus.tcp import ModbusTCP
import modbus

sta_if = network.WLAN(network.WLAN.IF_STA)

def do_connect():
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('raspi-webgui', 'ChangeMe')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ipconfig('addr4'))

def set_cb(reg_type, address, val):
    print(f"Setting {reg_type} at {address} to {val}")

def get_cb(reg_type, address, val):
    print(f"Getting {reg_type} at {address} : {val}")

local_ip = sta_if.ifconfig()[0]
if local_ip == "0.0.0.0":
    do_connect()


local_ip = sta_if.ifconfig()[0]
tcp_port = 502      # port to listen for requests/providing data

client = ModbusTCP()

# check whether client has been bound to an IP and a port
if not client.get_bound_status():
    client.bind(local_ip=local_ip, local_port=tcp_port)

client.add_hreg(
    address=modbus.Registers["MOTION_SENSOR"],
    value=0,
    on_set_cb=set_cb,
    on_get_cb=get_cb
)

while True:
    try:
        # Motion sensor
        m = machine.Pin(22, machine.Pin.IN)

        # Leds
        #lg = machine.Pin(5, machine.Pin.OUT)
        #lr = machine.Pin(4, machine.Pin.OUT)

        c = 0
        while True:
            client.set_hreg(modbus.Registers["MOTION_SENSOR"], m.value())
            time.sleep(0.1)
            result = client.process()
    except KeyboardInterrupt:
        print(local_ip)
    except Exception as e:
        print('Exception during execution: {}'.format(e))
