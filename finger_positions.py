"""
Subject module project in Computer Science
Semester: F2022
Authors: Azita Sofie Tadayoni, 68888
Emma Kathrine Derby Hansen, 71433
Alexander Kiellerup Swystun 72048
Áron Kuna 70492
"""

import hand_track_class
import time
import math

tracker_object = hand_track_class.Hand_track()
tracker_object.start() # Start handtracker
tracker_object.img_on() # Display image for user
tracker_object.set_text("Incorrect hand position")

position_time = time.time()
send_message = True

limits = {
    "min": {
        "thumb": 0.6,
        "index": 0.7,
        "middle": 0.6,
        "ring": 0.6,
        "pinky": 0.6,
        "rotate": 2.4
    },
    "max": {
        "thumb": 2.8,
        "index": 1.9,
        "middle": 2,
        "ring": 2,
        "pinky": 1.5,
        "rotate": 3.1
    }
}

def rel_distance(finger, compare_to, coord_dict, orientation):
    result = (math.dist(coord_dict[finger], coord_dict[compare_to])/orientation - limits["min"][finger]) / (limits["max"][finger] - limits["min"][finger])
    result *= 180
    if result > 180:
        result = 180
    elif result < 0:
        result = 0
    return int(result)

def get_positions():
    global position_time, send_message

    if tracker_object.hand_on_img: # When a hand is visible on image
            coords = {
                "thumb":(tracker_object.thumb_tip.x, tracker_object.thumb_tip.y),
                "index": (tracker_object.index_tip.x, tracker_object.index_tip.y),
                "index_mcp": (tracker_object.index_mcp.x, tracker_object.index_mcp.y),
                "middle": (tracker_object.middle_tip.x, tracker_object.middle_tip.y),
                "ring": (tracker_object.ring_tip.x, tracker_object.ring_tip.y),
                "ring_mcp": (tracker_object.ring_mcp.x, tracker_object.ring_mcp.y),
                "pinky": (tracker_object.pinky_tip.x, tracker_object.pinky_tip.y),
                "wrist": (tracker_object.wrist.x, tracker_object.wrist.y)
            }

            horizontal_dist = math.dist(coords["ring_mcp"], coords["index_mcp"])
            vertical_dist = math.dist(coords["wrist"],coords["ring_mcp"])

            finger_distances = { # setting distances between 0 and 1 independent of the distance from camera
                "thumb-rmcp": rel_distance("thumb", "ring_mcp", coords, horizontal_dist),
                "index-w": rel_distance("index", "wrist", coords, vertical_dist),
                "middle-w": rel_distance("middle", "wrist", coords, vertical_dist),
                "ring-w": rel_distance("ring", "wrist", coords, vertical_dist),
                "pinky-w": rel_distance("pinky", "wrist", coords, vertical_dist)
            }

            # See when hand is closed (when pinky and ring tip is lower than ring mcp) - currently not in use
            is_partly_closed = coords["pinky"][1] > coords["ring_mcp"][1] and coords["ring"][1] > coords["ring_mcp"][1]
            # See when hand is fully closed
            is_fully_closed = is_partly_closed and coords["middle"][1] > coords["ring_mcp"][1] and coords["index"][1] > coords["ring_mcp"][1]

            # Check if the hand position is correct
            if limits["min"]["rotate"] < (vertical_dist/horizontal_dist) < limits["max"]["rotate"] or is_fully_closed:
                # open - good to go
                send_message = True
                tracker_object.text_off()
                position_time = time.time()
            else:
                # incorrect hand position
                if time.time() - position_time > 1:
                    tracker_object.text_on()
                    send_message = False # Do not send message
    else:
        finger_distances = None
        send_message = False
    return finger_distances, send_message