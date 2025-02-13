from sqlalchemy.orm import Session
from app.models.device import Device
from app.models.sensor_data import SensorData
from app.models.automation import Automation
from app.services.modbus import Client, Registers
from app.core.dependencies import get_db
from app.core.automation import check_condition
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
                client.open()
                device_id = db.query(Device).filter(Device.ip == client_ip).first().id
                automations_related = db.query(Automation).filter(Automation.sensor_id == device_id).all()
                for sensor in client.sensors:
                    try :
                        sensor_type = Registers[sensor.type]
                        if sensor_type < 100 :
                            value = client.read_register(sensor.type)[0]
                            new_data = SensorData(device_id=device_id, sensor_type=sensor.type, value=value)
                            db.add(new_data)
                            db.commit()
                            db.refresh(new_data)
                            match sensor_type:
                                case 1: # Numpad
                                    client.write_register(sensor.type, 0)

                            # Automation
                            for automation in automations_related:
                                if automation.sensor_type == sensor.type:
                                    if check_condition(condition=automation.condition, value=value):
                                        actuator_ip = db.query(Device).filter(Device.id == automation.actuator_id).first().ip
                                        send_action(client_ip=actuator_ip, action_id=automation.action_id)


                        
                    except :
                        print(f"Error when polling sensor {sensor.type} for device at IP {client_ip}")

        except Exception as e:
            print(f"Modbus thread exception : {e}")
        finally :
            db_generator.close()

        # You can add sleep between each poll
        #time.sleep(1)

def send_action(client_ip : str, action_id : int):
    client = client_list[client_ip]
    action = client.actions[action_id]
    client.write_register(action.sensor_type, action.value)
