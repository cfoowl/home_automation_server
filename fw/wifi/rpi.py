#!/bin/python3

from pyModbusTCP.client import ModbusClient
import random as rd

c = ModbusClient(host="10.3.141.228", port=502)

# open the socket for 2 reads then close it.
if not c.open():
    print("Error with host or port params")
    exit()

print("Reading registers...")
regs_list_1 = c.read_input_registers(4, 1)
regs_list_2 = c.read_discrete_inputs(3, 1)
regs_list_3 = c.read_holding_registers(2, 1)
regs_list_4 = c.read_coils(1, 1)
print(regs_list_1)
print(regs_list_2)
print(regs_list_3)
print(regs_list_4)
print()

print("Writing registers...")
rd.seed()
c.write_multiple_coils(1, [bool(rd.randint(0,1))])
c.write_multiple_registers(2, [rd.randint(0,200)])
print()

print("Reading registers...")
regs_list_1 = c.read_input_registers(4, 1)
regs_list_2 = c.read_discrete_inputs(3, 1)
regs_list_3 = c.read_holding_registers(2, 1)
regs_list_4 = c.read_coils(1, 1)
print(regs_list_1)
print(regs_list_2)
print(regs_list_3)
print(regs_list_4)
print()

print("Test new register ...")
regs_list_5 = c.read_holding_registers(10, 1)
c.write_multiple_registers(10, [rd.randint(0,200)])
regs_list_6 = c.read_holding_registers(10, 1)
print(f"{regs_list_5} -> {regs_list_6}")

c.close()
