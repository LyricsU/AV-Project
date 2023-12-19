# Leader Drone Script
from pymavlink import mavutil
import socket
import json
import time
import math
print("Connecting to MAVLInk via TCP...")

# Connect to the Pixhawk
master = mavutil.mavlink_connection('tcp:localhost:14551')

print("MAVLink connection estalished")
# Setup UDP socket for sending data
follower_ip = '192.168.2.109'  # Replace with the IP of the follower drone
follower_port = 14551
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:
    print("Waiting for heartbeat")
    # Wait for a heartbeat message to confirm connection
    master.wait_heartbeat()
    print("Heartbeat Recived.")

    # Request data streams
    master.mav.request_data_stream_send(master.target_system, master.target_component, mavutil.mavlink.MAV_DATA_STREAM_ALL, 1, 1)

    # Fetch attitude and GPS data
    attitude = master.recv_match(type='ATTITUDE', blocking=True)
    hud_data = master.recv_match(type='VFR_HUD', blocking=True)

    if attitude and hud_data:
        yaw_radians = attitude.yaw
        yaw_degrees = math.degrees(yaw_radians) #converting from rads to deg
        altitude = hud_data.alt   # Convert from mm to meters

        # Prepare data to send
        data = json.dumps({'altitude': altitude, 'yaw': yaw_degrees})

        # Send data to follower
        sock.sendto(data.encode(), (follower_ip, follower_port))
        #conf. data was sent
        print(f"Sent data to follower: {data}")

    time.sleep(1)
