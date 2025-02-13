import subprocess
import re
from sqlalchemy.orm import Session
from app.models.detected_device import DetectedDevices
from app.models.device import Device
from app.services.modbus import Client

scan_client_list = dict()

def filter_mac_addresses(string: str) -> bool:
    mac_regex = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return mac_regex.match(string)

def get_connected_clients() -> list:
    """
    Return a list of mac address currently connected to the Raspberry hotspot
    """
    try:
        result = subprocess.run(
            ["hostapd_cli", "all_sta"],
            capture_output=True,
            text=True,
            check=True
        )
        clients = parse_hostapd_cli_output(result.stdout)
        return clients
    except FileNotFoundError:
        print("hostapd_cli isn't installed or not found.")
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error during hostapd_cli execution : {e}")
        return []

def parse_hostapd_cli_output(output: list) -> list:
    """
    Parse hostapd_cli all_sta output to get only mac address
    """
    clients = []
    for line in output.splitlines():
        if filter_mac_addresses(line):
            clients.append(line)
    return clients

def get_dhcp_leases(file_path : str = "/var/lib/misc/dnsmasq.leases") -> dict:
    """
    Get every DHCP lease registered
    Return a dict like this :
    {
        mac : {
            "ip" : ip,
            "hostname" : hostname
        },
        ...
    }
    """
    clients = dict()
    try:
        with open(file_path, "r") as file:
            for line in file:
                parts = line.split()
                if len(parts) >= 5:
                    mac = parts[1]
                    ip = parts[2]
                    hostname = parts[3]
                    clients |= {mac : {"ip" : ip, "hostname" : hostname}}
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    return clients

def is_registered_Device_by_ip(db : Session, ip : str) -> bool:
    return db.query(Device).filter(Device.ip == ip).first() is not None

def create_detected_device_entry(db: Session, ip : str):
    global scan_client_list
    client_type = str()
    for sensor in scan_client_list[ip].sensors:
        client_type += sensor.type + " | "
    client_type = client_type[:-3]

    new_detected_device = DetectedDevices(ip=ip, type=client_type, device_metadata = {})
    db.add(new_detected_device)
    db.commit()
    db.refresh(new_detected_device)

def scan_devices(db : Session):
    global scan_client_list
    scan_client_list = dict()

    clients_hostapd = get_connected_clients()
    dhcp_leases = get_dhcp_leases()

    db.query(DetectedDevices).delete()
    db.commit()
    
    detected_device_ind = 0
    for mac_address in clients_hostapd:
        ip = dhcp_leases[mac_address]["ip"]
        client = Client(ip)
        if not client.check_health():
            continue
        scan_client_list |= {ip : client}
        print(scan_client_list[ip])
        if (not is_registered_Device_by_ip(db = db, ip = ip)):
            create_detected_device_entry(db = db, ip = ip)
            detected_device_ind += 1
    print(scan_client_list)
    return detected_device_ind

