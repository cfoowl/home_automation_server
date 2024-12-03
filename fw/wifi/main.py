import network
import machine
import time
from umodbus.tcp import ModbusTCP

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

register_definitions = {
    # Coil, RW, bits
    "COILS": {
        "EXAMPLE_COIL": {
            "register": 1,
            "len": 1,
            "val": 1
        }
    },
    # Holding register, RW, 16 bit words
    "HREGS": {
        "EXAMPLE_HREG": {
            "register": 2,
            "len": 1,
            "val": 19
        }
    },
    # Discrete input, R, bits
    "ISTS": {
        "EXAMPLE_ISTS": {
            "register": 3,
            "len": 1,
            "val": 0
        }
    },
    # Input register, R, 16 bit words
    "IREGS": {
        "EXAMPLE_IREG": {
            "register": 4,
            "len": 1,
            "val": 60001
        }
    }
}

# use the defined values of each register type provided by register_definitions
client.setup_registers(registers=register_definitions)

client.add_hreg(
    address=10,
    value=10,
    on_set_cb=set_cb,
    on_get_cb=get_cb
)

while True:
    try:
        result = client.process()
    except KeyboardInterrupt:
        print(local_ip)
    except Exception as e:
        print('Exception during execution: {}'.format(e))
