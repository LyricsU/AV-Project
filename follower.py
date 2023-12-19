import socket
import json
import time

# Setup UDP socket for receiving data
local_ip = '0.0.0.0'  # Listen on all available IPs
local_port = 14551    # The port should match the port used by the leader drone to send data
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((local_ip, local_port))

print("follower script starting waiting for data from leader...") 

while True:
    try:
        # Receive data from leader
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print(f"recieved data:{data.decode()}")

        # Decode the received data
        decoded_data = data.decode()
        print(f"Received data: {decoded_data}")

        # Convert the data from JSON format
        data_dict = json.loads(decoded_data)

        # Extract altitude and yaw
        altitude = data_dict['altitude']
        yaw = data_dict['yaw']

        # TODO: Add logic to act on received altitude and yaw
        # This part will depend on what I want the follower drone to do with the received data

        # For example, print the values
        print(f"Recieved Altitude: {altitude}, Yaw: {yaw}")
        
    except json.JSONDecodeError:
        print("Error decoding JSON data")
    except Exception as e:
        print(f"An error occurred: {e}")

    time.sleep(1)
