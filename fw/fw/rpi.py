#!/bin/python3

from pyModbusTCP.client import ModbusClient
import random as rd
import modbus

# A modifier
clients_ip = ["10.3.141.228", "10.3.141.120"]

class Sensor:
    def __init__(self, t):
        self.type = t

class Device:
    sensors = []
    def __init__(self, ip):
        self.client = ModbusClient(host=ip, port=502)
        if not self.client.open():
            print(f"Error with host or port params for {ip}")
            self.client = None
            return
        for t,v in modbus.Registers.items():
            if self.client.read_holding_registers(v, 1):
                self.sensors.append(Sensor(v))

    def __del__(self):
        if self.client is not None:
            self.client.close()

    def __repr__(self):
        ret = f"Sensors ({len(self.sensors)}) : "
        for s in self.sensors:
            ret += str(s.type)
            ret += " "
        return ret

clients = [Device(ip) for ip in clients_ip]

for d in clients:
    print(d)

while True:
    s = input()
    if s == "r":
        for d in clients:
            reg = d.client.read_holding_registers(modbus.Registers["LED_RED"], 1)
            d.client.write_multiple_registers(modbus.Registers["LED_RED"], [1-reg[0]])
    elif s == "g":
        for d in clients:
            reg = d.client.read_holding_registers(modbus.Registers["LED_GREEN"], 1)
            d.client.write_multiple_registers(modbus.Registers["LED_GREEN"], [1-reg[0]])
