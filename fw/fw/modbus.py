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
# # Affiche la valeur du détécteur de mouvement
# print(clients[ip].read_register("MOTION_SENSOR"))


Registers = {
    # R
    "MOTION_SENSOR": 0,
    "NUMPAD": 1,

    # RW
    "LED_RED" : 100,
    "LED_GREEN" : 101,
    "BUZZER" : 102,
}

# Récupère la clé à partir de la valeur du dictionnaire
def get_register_name(r):
    return list(mydict.keys())[list(mydict.values()).index(r)]

class Sensor:
    def __init__(self, t):
        self.type = t

class Client:
    sensors = []
    def __init__(self, ip):
        self.ip = ip
        self.client = ModbusClient(host=ip, port=502)
        if not self.client.open():
            print(f"Error with host or port params for {ip}")
            self.client = None
            return
        for t,v in modbus.Registers.items():
            if self.client.read_holding_registers(v, 1):
                self.sensors.append(Sensor(t))

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
        return self.client.read_holding_registers(modbus.Registers[sensor_type], 1)

    def write_register(self, sensor_type, value):
        return self.client.write_multiple_registers(modbus.Registers[sensor_type], [value])

    # Retorun True si tout est OK, False si la connection est fermé/planté
    def check_health(self):
        if self.client is None:
            return False
        return self.client.is_open
