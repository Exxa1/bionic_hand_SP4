import hand_track_class
import time
import math

tracker_object = hand_track_class.Hand_track()
tracker_object.start() # Start handtracker
tracker_object.img_on() # Display image for user

position_time = time.time()
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


def calib():
    global position_time

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
                "thumb-rmcp": (math.dist(coords["thumb"], coords["ring_mcp"])/horizontal_dist - limits["min"]["thumb"]) / (limits["max"]["thumb"] - limits["min"]["thumb"]),
                "index-w": (math.dist(coords["index"], coords["wrist"])/vertical_dist - limits["min"]["index"]) / (limits["max"]["index"]-limits["min"]["index"]),
                "middle-w": (math.dist(coords["middle"], coords["wrist"])/vertical_dist - limits["min"]["middle"]) / (limits["max"]["middle"] - limits["min"]["middle"]),
                "ring-w": (math.dist(coords["ring"], coords["wrist"])/vertical_dist - limits["min"]["ring"]) / (limits["max"]["ring"] - limits["min"]["ring"]),
                "pinky-w": (math.dist(coords["pinky"], coords["wrist"])/vertical_dist - limits["min"]["pinky"]) / (limits["max"]["pinky"] - limits["min"]["pinky"])
            }

            # See when hand is closed (when pinky and ring tip is lower than ring mcp) - currently not in use
            is_partly_closed = coords["pinky"][1] > coords["ring_mcp"][1] and coords["ring"][1] > coords["ring_mcp"][1]
            # See when hand is fully closed
            is_fully_closed = is_partly_closed and coords["middle"][1] > coords["ring_mcp"][1] and coords["index"][1] > coords["ring_mcp"][1]

            send_message = True
            # Check if the hand position is correct
            if limits["min"]["rotate"] < (vertical_dist/horizontal_dist) < limits["max"]["rotate"]:
                # open - good to go
                tracker_object.text_off()
                position_time = time.time()
            elif is_fully_closed:
                # fully closed - good to go
                tracker_object.text_off()
                position_time = time.time()
            else:
                # incorrect hand position
                if time.time() - position_time > 1:
                    tracker_object.text_on()
                    tracker_object.set_text("Incorrect hand position")
                    send_message = False # Do not send message

            # Ensures each distance remains within range

            for distance in finger_distances:
                finger_distances[distance] = finger_distances[distance]*180
                if finger_distances[distance] > 180:
                    finger_distances[distance] = 180
                elif finger_distances[distance] < 0:
                    finger_distances[distance] = 0
                finger_distances[distance] = int(finger_distances[distance])
    else:
        finger_distances = { # setting distances between 0 and 1 independent of the distance from camera
                "thumb-rmcp": 180,
                "index-w": 180,
                "middle-w": 180,
                "ring-w": 180,
                "pinky-w": 180
            }
        send_message = False
    return finger_distances, send_message