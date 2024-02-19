#Code is working (communicating between the 2 rpis & sending yaw and altitude) as of 15:00 19/02/24
import socket
import json
import time
import uuid

def get_mac_address():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = ':'.join(mac_num[i:i+2] for i in range(0, 11, 2))
    return mac

my_mac_address = get_mac_address()

local_ip = '0.0.0.0'
local_port = 14551
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((local_ip, local_port))

print("Follower script starting, waiting for commands...")

while True:
    try:
        data, addr = sock.recvfrom(1024)
        decoded_data = data.decode()
        command = json.loads(decoded_data)

        if command.get('mac_address') == my_mac_address:
            position_command = command['position']
            print(f"Received position command: {position_command}")
            # Here, implement logic to adjust position based on the command
            # This part depends on your drone's control API
        else:
            print("Command not intended for this drone.")
    except json.JSONDecodeError:
        print("Error decoding JSON data")
    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(1)
