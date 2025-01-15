# Exemple

# clients = {}
# ip = "1.1.1.1"
# clients[ip] = Client(ip)
#
# # Affiche True si tout est bon, False si la création du client à raté
# print(clients[ip].check_health())
#
# # Affiche la liste de capteurs
# print(clients[ip])
# 
# # Affiche la liste de capteurs
# sensors = clients[ip].list_peripherals()
# print(sensors)
#
# # Allume la LED
# clients[ip].write_register("LED_GREEN", 1)
#
# # Affiche la valeur du détecteur de mouvement
# print(clients[ip].read_register("MOTION_SENSOR"))

from pyModbusTCP.client import ModbusClient

Registers = {
    # R
    "MOTION_SENSOR": 0,
    "NUMPAD": 1,

    # RW
    "LED_RED" : 100,
    "LED_GREEN" : 101,
    "BUZZER" : 102,
}

class Action:
    def __init__(self, command_name: str, sensor_type : str, value : int):
        self.command_name = command_name
        self.sensor_type = sensor_type
        self.value = value
    def __repr__(self):
        ret = f"{self.command_name} : {self.sensor_type} : {self.value}"
        return ret


Actions = {
    "LED_RED" : [
            Action("Turn On Led Red", "LED_RED", 1),
            Action("Turn Off Led Red", "LED_RED", 0)
        ],
    "LED_GREEN" : [
            Action("Turn On Led Green", "LED_GREEN", 1),
            Action("Turn Off Led Green", "LED_GREEN", 0)
        ],
}



# Récupère la clé à partir de la valeur du dictionnaire
def get_register_name(r):
    return list(mydict.keys())[list(mydict.values()).index(r)]

class Sensor:
    def __init__(self, t):
        self.type = t

class Client:
    sensors = []
    actions = {}
    def __init__(self, ip):
        self.ip = ip
        self.client = ModbusClient(host=ip, port=502)
        if not self.client.open():
            print(f"Error with host or port params for {ip}")
            self.client = None
            return
        id_action = 0
        for t,v in Registers.items():
            if self.client.read_holding_registers(v, 1):
                self.sensors.append(Sensor(t))
                if t in Actions:
                    for action in Actions[t]:
                        self.actions[id_action] = action
                        id_action += 1

    def __del__(self):
        if self.client is not None:
            self.client.close()

    def __repr__(self):
        ret = f"Sensors ({len(self.sensors)}) : "
        for s in self.sensors:
            ret += str(s.type)
            ret += " "
        return ret

    # Pour réouvrir une connection planté
    def open(self):
        if not self.check_health():
            self.client = ModbusClient(host=self.ip, port=502)
            if not self.client.open():
                print(f"Error with host or port params for {self.ip}")
                self.client = None

    # Inutile normalement
    def close(self):
        if self.client is not None:
            self.client.close()

    # Retourn un tableau (possiblement vide) de clé (string) du dictionnaire Registers
    def list_peripherals(self):
        ret = []
        for s in self.sensors:
            ret.append(s.type)
        return ret
        
    def read_register(self, sensor_type):
        return self.client.read_holding_registers(Registers[sensor_type], 1)

    def write_register(self, sensor_type, value):
        return self.client.write_multiple_registers(Registers[sensor_type], [value])

    # Retorun True si tout est OK, False si la connection est fermé/planté
    def check_health(self):
        if self.client is None:
            return False
        return self.client.is_open
