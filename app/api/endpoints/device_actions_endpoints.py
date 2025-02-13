from sqlalchemy.orm import Session
from app.core.modbus_thread import client_list, send_action
from app.services.modbus import Client, Action
from app.api.endpoints.device_endpoints import get_device_by_id_endpoint

def get_device_actions_by_id_endpoint(db: Session, device_id: int):
    device = get_device_by_id_endpoint(db, device_id)
    client = client_list[device.ip]
    ret = list()
    for action_id in client.actions:
        ret.append({"id" : action_id, "command_name" : client.actions[action_id].command_name})
    return ret

def post_device_actions_by_id_endpoint(db: Session, device_id: int, action_id : int):
    device = get_device_by_id_endpoint(db, device_id)
    send_action(device.ip, action_id)