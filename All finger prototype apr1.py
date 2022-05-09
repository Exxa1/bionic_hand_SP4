from turtle import distance

from cv2 import subtract
import hand_track_class
import math
import numpy as np
import socket
import time

#To use the hand tracker, you need to create a hand tracker object
tracker_object = hand_track_class.Hand_track()

tracker_object.start()

tracker_object.img_on()

while True:

    if tracker_object.hand_on_img: #TO SEE THESE PRINTED MAKE SURE YOUR HAND IS VISIBLE
        index_coord = (tracker_object.index_tip.x, tracker_object.index_tip.y)
        middle_coord = (tracker_object.middle_tip.x, tracker_object.middle_tip.y)
        ring_coord = (tracker_object.ring_tip.x, tracker_object.ring_tip.y)
        pinky_coord = (tracker_object.pinky_tip.x, tracker_object.pinky_tip.y)
        thumb_coord = (tracker_object.thumb_tip.x, tracker_object.thumb_tip.y)
        ring_mcp_coord = (tracker_object.ring_mcp.x, tracker_object.ring_mcp.y)
        index_mcp_coord = (tracker_object.index_mcp.x, tracker_object.index_mcp.y)
        wristList = (tracker_object.wrist.x, tracker_object.wrist.y)
        horizontal_distance = math.dist(ring_mcp_coord, index_mcp_coord)
        vertical_distance = math.dist(wristList, ring_mcp_coord)
        index_distance = (math.dist(index_coord, wristList)/vertical_distance - 0.7) / (1.9-0.7)
        middle_distance = (math.dist(middle_coord, wristList)/vertical_distance - 0.6) / (2 - 0.6)
        ring_distance = (math.dist(ring_coord, wristList)/vertical_distance - 0.6) / (2 - 0.6)
        pinky_distance = (math.dist(pinky_coord, wristList)/vertical_distance - 0.6) / (1.5 - 0.6)
        thumb_distance = (math.dist(thumb_coord, ring_mcp_coord)/horizontal_distance - 0.6) / (2.8 - 0.6)
        distance_touple= [index_distance, middle_distance, ring_distance, pinky_distance, thumb_distance]

        #wristList = a; ring_mcp_coord = b; index_mcp_coord = c; Surface of triangle: (b-a) X (c-a)
        # surface = np.cross(np.subtract(ring_mcp_coord, wristList), np.subtract(index_mcp_coord, wristList))
        # print(surface)

        is_partly_closed = pinky_coord[1] > ring_mcp_coord[1] and ring_coord[1] > ring_mcp_coord[1]
        is_fully_closed = is_partly_closed and middle_coord[1] > ring_mcp_coord[1] and index_coord[1] > ring_mcp_coord[1]
        # print(is_closed)

        if not is_partly_closed and 2.4 < (vertical_distance/horizontal_distance) < 3.1:
            print("open - good to go")
        elif is_partly_closed and 2.4 < (vertical_distance/horizontal_distance) < 3.1:
            print("closed - good to go")
        elif is_fully_closed:
            print("fully closed - good to go")
        else:
            print("nope")


        for i in range(5):
            distance_touple[i] = distance_touple[i]*180
            if distance_touple[i] > 180:
                distance_touple[i] = 180
            elif distance_touple[i] < 0:
                distance_touple[i] = 0
            distance_touple[i] = int(distance_touple[i])

        # print(vertical_distance/horizontal_distance)
        

        # SENDING UPD MESSAGE
        MESSAGE = "{:0>3d}:{:0>3d}:{:0>3d}:{:0>3d}:{:0>3d}".format(distance_touple[0],distance_touple[1], distance_touple[2], distance_touple[3], distance_touple[4])

        UDP_IP = "192.168.69.216"
        UDP_PORT = 4210

       # print ("UDP target IP:", UDP_IP)
       # print ("UDP target port:", UDP_PORT)
        print ("message:", MESSAGE)

        sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP

        sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
