"""
SEND UDP
Subject module project in Computer Science
Semester: F2022
Authors: Azita Sofie Tadayoni, 68888
Emma Kathrine Derby Hansen, 71433
Alexander Kiellerup Swystun 72048
Áron Kuna 70492
"""

import socket


UDP_IP = "192.168.101.216" # Changes every time!
UDP_PORT = 4210

sock = socket.socket(socket.AF_INET, # Internet
            socket.SOCK_DGRAM) # UDP

def send(finger_distances, sock = sock):
    # Formatting message for the arduino code
    MESSAGE = "{:0>3d}:{:0>3d}:{:0>3d}:{:0>3d}:{:0>3d}".format(finger_distances["index-w"],
                                                            finger_distances["middle-w"], 
                                                            finger_distances["ring-w"], 
                                                            finger_distances["pinky-w"], 
                                                            finger_distances["thumb-rmcp"])
    print ("message:", MESSAGE)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))