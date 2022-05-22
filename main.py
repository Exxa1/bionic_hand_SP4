# Setting up libraries
import socket
from calibration import calib

# Initiate variables
UDP_IP = "192.168.101.216" # Changes every time!
UDP_PORT = 4210

sock = socket.socket(socket.AF_INET, # Internet
            socket.SOCK_DGRAM) # UDP

# Main loop
while True:

# Calculate relative finger distances
        finger_distances, send_message = calib()

# SENDING UPD MESSAGE
        # Formatting message for the arduino code
        MESSAGE = "{:0>3d}:{:0>3d}:{:0>3d}:{:0>3d}:{:0>3d}".format(finger_distances["index-w"],
                                                                    finger_distances["middle-w"], 
                                                                    finger_distances["ring-w"], 
                                                                    finger_distances["pinky-w"], 
                                                                    finger_distances["thumb-rmcp"])
        if send_message:
            print ("message:", MESSAGE)
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
