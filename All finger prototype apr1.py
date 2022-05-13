# Setting up libraries
from cv2 import subtract
import hand_track_class
import math
import numpy as np
import socket
import time

#Initiate the tracker object
tracker_object = hand_track_class.Hand_track()
tracker_object.start() # Start handtracker
tracker_object.img_on() # Display image for user


position_time = time.time()

while True:

    if tracker_object.hand_on_img: # When a hand is visible on image
        #Coordinates for fingers
        index_coord = (tracker_object.index_tip.x, tracker_object.index_tip.y)
        middle_coord = (tracker_object.middle_tip.x, tracker_object.middle_tip.y)
        ring_coord = (tracker_object.ring_tip.x, tracker_object.ring_tip.y)
        pinky_coord = (tracker_object.pinky_tip.x, tracker_object.pinky_tip.y)
        thumb_coord = (tracker_object.thumb_tip.x, tracker_object.thumb_tip.y)
        ring_mcp_coord = (tracker_object.ring_mcp.x, tracker_object.ring_mcp.y)
        index_mcp_coord = (tracker_object.index_mcp.x, tracker_object.index_mcp.y)
        wristList = (tracker_object.wrist.x, tracker_object.wrist.y)
        # Calculating distances
        horizontal_distance = math.dist(ring_mcp_coord, index_mcp_coord)
        vertical_distance = math.dist(wristList, ring_mcp_coord)
        index_distance = (math.dist(index_coord, wristList)/vertical_distance - 0.7) / (1.9-0.7)
        middle_distance = (math.dist(middle_coord, wristList)/vertical_distance - 0.6) / (2 - 0.6)
        ring_distance = (math.dist(ring_coord, wristList)/vertical_distance - 0.6) / (2 - 0.6)
        pinky_distance = (math.dist(pinky_coord, wristList)/vertical_distance - 0.6) / (1.5 - 0.6)
        thumb_distance = (math.dist(thumb_coord, ring_mcp_coord)/horizontal_distance - 0.6) / (2.8 - 0.6)
        # Placing distances in a list
        distance_list= [index_distance, middle_distance, ring_distance, pinky_distance, thumb_distance]

        # See when hand is closed (when pinky and ring tip is lower than ring mcp)
        is_partly_closed = pinky_coord[1] > ring_mcp_coord[1] and ring_coord[1] > ring_mcp_coord[1]
        # See when hand is fully closed
        is_fully_closed = is_partly_closed and middle_coord[1] > ring_mcp_coord[1] and index_coord[1] > ring_mcp_coord[1]

        send_message = True
        # Check if the hand position is correct
        if not is_partly_closed and 2.4 < (vertical_distance/horizontal_distance) < 3.1:
            # print("open - good to go")
            tracker_object.text_off()
            position_time = time.time()
        elif is_partly_closed and 2.4 < (vertical_distance/horizontal_distance) < 3.1:
            # print("closed - good to go")
            tracker_object.text_off()
            position_time = time.time()
        elif is_fully_closed:
            # print("fully closed - good to go")
            tracker_object.text_off()
            position_time = time.time()
        else:
            if time.time() - position_time > 1:
                # print("nope")
                tracker_object.text_on()
                tracker_object.set_text("Incorrect hand position")
                send_message = False # Do not send message

        # Ensures each distance remains within range
        for i in range(5):
            distance_list[i] = distance_list[i]*180
            if distance_list[i] > 180:
                distance_list[i] = 180
            elif distance_list[i] < 0:
                distance_list[i] = 0
            distance_list[i] = int(distance_list[i])


        # SENDING UPD MESSAGE
        # Formatting message for the arduino code
        MESSAGE = "{:0>3d}:{:0>3d}:{:0>3d}:{:0>3d}:{:0>3d}".format(distance_list[0],distance_list[1], distance_list[2], distance_list[3], distance_list[4])

        UDP_IP = "192.168.101.216" # Changes every time!
        UDP_PORT = 4210

        sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP

        # Ready to send udp message
        if send_message:
            print ("message:", MESSAGE)
            sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
