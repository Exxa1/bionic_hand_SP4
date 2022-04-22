from turtle import distance
import hand_track_class
import math
import socket
import time

#To use the hand tracker, you need to create a hand tracker object
tracker_object = hand_track_class.Hand_track()

tracker_object.start()

tracker_object.img_on()

tempmax = 0
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
        index_distance = math.dist(index_coord, wristList)
        middle_distance = math.dist(middle_coord, wristList)
        ring_distance = math.dist(ring_coord, wristList)
        pinky_distance = math.dist(pinky_coord, wristList)
        thumb_distance = math.dist(thumb_coord, ring_mcp_coord)
        horizontal_distance = math.dist(ring_mcp_coord, index_mcp_coord)
        vertical_distance = math.dist(wristList, ring_mcp_coord)
        distance_touple= [index_distance, middle_distance, ring_distance, pinky_distance, thumb_distance]
        
        # FINDING MAX AND MIN VALUES
        if (pinky_distance/vertical_distance) > tempmax:
            tempmax = pinky_distance/vertical_distance
        print(tempmax)

        # for i in range(5):
        #     if distance_touple[i] > 180:
        #         distance_touple[i] = 180
        #     distance_touple[i] = int(distance_touple[i])
        

        # while True:
        #     tempmax = 0
        #     if (ring_distance/vertical_distance) > tempmax:
        #         tempmax = index_distance/vertical_distance
        #     print(tempmax)

        # # SENDING UPD MESSAGE
    #     MESSAGE = "{:0>3d}:{:0>3d}:{:0>3d}:{:0>3d}:{:0>3d}".format(distance_touple[0],distance_touple[1], distance_touple[2], distance_touple[3], distance_touple[4])

    #     UDP_IP = "192.168.48.216"
    #     UDP_PORT = 4210

    #    # print ("UDP target IP:", UDP_IP)
    #    # print ("UDP target port:", UDP_PORT)
    #    # print ("message:", MESSAGE)

    #     sock = socket.socket(socket.AF_INET, # Internet
    #                 socket.SOCK_DGRAM) # UDP

    #     sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
