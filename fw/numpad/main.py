# Pin connection
#   Numpad
#       1 -> 13
#       2 -> 12
#       3 -> 14
#       4 -> 27
#       5 -> 26
#       6 -> 25
#       7 -> 33
#       8 -> 32
#   Leds
#       Red -> 4
#       Green -> 5

import machine
import time

# Numpad
p8 = machine.Pin(32, machine.Pin.IN) # 8
p7 = machine.Pin(33, machine.Pin.IN) # 7
p6 = machine.Pin(25, machine.Pin.IN) # 6
p5 = machine.Pin(26, machine.Pin.IN) # 5
p4 = machine.Pin(27, machine.Pin.OUT) # 4
p3 = machine.Pin(14, machine.Pin.OUT) # 3
p2 = machine.Pin(12, machine.Pin.OUT) # 2
p1 = machine.Pin(13, machine.Pin.OUT) # 1

# -8-     1   2   3   A
# -7-     4   5   6   B
# -6-     7   8   9   C
# -5-     *   0   #   D
#
#        -4- -3- -2- -1-

# Leds
lg = machine.Pin(5, machine.Pin.OUT)
lr = machine.Pin(4, machine.Pin.OUT)

CODE="159D"

buttons_str = [["1", "2", "3", "A"],
               ["4", "5", "6", "B"],
               ["7", "8", "9", "C"],
               ["*", "0", "#", "D"]]

buttons = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

old_buttons = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]

passin = ""

def validate():
    print(passin)
    if passin == CODE:
        lg.value(1)
    else:
        lr.value(1)

    time.sleep(0.5)
    lg.value(0)
    lr.value(0)


def read_column(line):
    if p5.value():
        buttons[3][line] = 1
    if p6.value():
        buttons[2][line] = 1
    if p7.value():
        buttons[1][line] = 1
    if p8.value():
        buttons[0][line] = 1
    

lr.value(0)
lg.value(0)
while True:
    old_buttons = buttons
    buttons = [[0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]

    p1.value(1)
    p2.value(0)
    p3.value(0)
    p4.value(0)
    read_column(3)
    
    p1.value(0)
    p2.value(1)
    p3.value(0)
    p4.value(0)
    read_column(2)
    
    p1.value(0)
    p2.value(0)
    p3.value(1)
    p4.value(0)
    read_column(1)
    
    p1.value(0)
    p2.value(0)
    p3.value(0)
    p4.value(1)
    read_column(0)

    if sum(sum(r) for r in buttons) > 1:
        continue

    for r in range(len(buttons)):
        for c in range(len(buttons[r])):
            if buttons[r][c] and not old_buttons[r][c]:
                if buttons_str[r][c] == "#":
                    validate()
                    passin = ""
                else:
                    passin += buttons_str[r][c]
                    lr.value(1)
                    time.sleep(0.01)
                    lr.value(0)

    
    time.sleep(0.06)
