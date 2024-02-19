#Code is working (communicating between the 2 rpis & sending yaw and altitude) as of 15:02 19/02/24
import socket
import json
import time
import math
from pymavlink import mavutil

print("Connecting to MAVLink via TCP...")

# Connect to the Pixhawk
master = mavutil.mavlink_connection('tcp:localhost:14551')

print("MAVLink connection established")

# Setup UDP socket for sending data
broadcast_ip = '192.168.2.255'  # Assuming broadcast; replace as needed
follower_port = 14551
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# List of follower drones, identified by some unique attribute (e.g., MAC address)
followers = ["drone2_mac_address", "drone3_mac_address"]

while True:
    print("Waiting for heartbeat")
    master.wait_heartbeat()
    print("Heartbeat Received.")

    master.mav.request_data_stream_send(master.target_system, master.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 1, 1)
    attitude = master.recv_match(type='ATTITUDE', blocking=True)
    hud_data = master.recv_match(type='VFR_HUD', blocking=True)

    if attitude and hud_data:
        # Generate and send instructions for each follower
        for index, follower_mac in enumerate(followers):
            # Example command structure: stay 5 meters behind the leader, with additional lateral offset for drone 3
            command = {
                'mac_address': follower_mac,
                'position': {
                    'behind': 5,
                    'right': 1 if index == 1 else 0,  # Adding a lateral offset for the second follower
                }
            }

            data = json.dumps(command)
            sock.sendto(data.encode(), (broadcast_ip, follower_port))
            print(f"Sent command to {follower_mac}: {data}")

    time.sleep(1)
