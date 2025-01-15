from sqlalchemy.orm import Session
from app.models.device import Device
from app.models.sensor_data import SensorData
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
    
    while True:
        db_generator = get_db()
        db = next(db_generator)
        try:
            local_client_list = client_list.copy()
            for client_ip in local_client_list:
                client = local_client_list[client_ip]
                device_id = db.query(Device).filter(Device.ip == client_ip).first().id
                for sensor in client.sensors:
                    sensor_type = sensor.type
                    value = client.read_register(sensor.type)
                    new_data = SensorData(device_id=device_id, sensor_type=sensor_type, value=value[0])
                    db.add(new_data)
                    db.commit()
                    db.refresh(new_data)
        except Exception as e:
            print(f"Modbus thread exception : {e}")
        finally :
            db_generator.close()
        time.sleep(5)

def send_action(client_ip : str, action_id : int):
    client = client_list[client_ip]
    action = client.actions[action_id]
    client.write_register(action.sensor_type, action.value)