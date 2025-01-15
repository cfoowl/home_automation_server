from sqlalchemy.orm import Session
from app.models.device import Device
from app.services.modbus import Client 
from app.core.dependencies import get_db
import time

client_list = dict()

def init_client_list():
    db_generator = get_db()
    db = next(db_generator)
    try :
        devices = db.query(Device).all()
        for device in devices :
            ip = device.ip
            add_client_to_list(client_list, ip)
    finally :
        db_generator.close()

def add_client_to_list(client_list: dict, ip: str):
    client_list |= {ip : Client(ip)}

def sensor_polling():
    global client_list 
    local_client_list = client_list.copy()
    while True:
        try:
            for client_ip in local_client_list:
                client = local_client_list[client_ip]
                for sensor in client.sensors:
                    print(sensor.type)
                    print(client.read_register(sensor.type))
        except Exception as e:
            print(f"Modbus thread exception : {e}")
        time.sleep(5)
