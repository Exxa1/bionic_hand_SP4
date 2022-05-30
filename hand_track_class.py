"""
HAND TRACKER CLASS
Subject module project in Computer Science
Semester: F2022
Authors: Azita Sofie Tadayoni, 68888
Emma Kathrine Derby Hansen, 71433
Alexander Kiellerup Swystun 72048
Áron Kuna 70492

This code is inspired by the
Interactive Digital Systems exam turn in assignment from 2021 autumn semester by Aron Kuna
Exam code: U25233
Github page of the code used: https://github.com/esbendg/IDS-HandIn/blob/master/hand_track_class.py
"""

import cv2 # pip install opencv-python
import mediapipe as mp # pip install mediapipe
import threading
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class Hand_track:

    #Initialize object
    def __init__(self):
        self.hand_on_img = False

        self.thumb_tip = None
        self.index_tip = None
        self.middle_tip = None
        self.ring_tip = None
        self.pinky_tip = None
        self.ring_mcp = None
        self.index_mcp = None
        self.wrist = None

        self.text_on_img = False
        self.text = None
        self.text_style = {
            "font"                   : cv2.FONT_HERSHEY_SIMPLEX,
            "bottom_left_corner" : (100,100),
            "font_scale"              : 1,
            "font_color"              : (0,0,255),
            "thickness"              : 3,
            "line_type"               : 2
        }

        self.cap = cv2.VideoCapture(0)
        self.img_state = 0                # 0 is off, 1 is on, 2 is closing window
        self.stop_thread = False
        

    def start(self):
        def loop():
            with mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                model_complexity=0,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
                while self.cap.isOpened():
                    success, image = self.cap.read()
                    if not success:
                        print("Ignoring empty camera frame.")
                        continue

                    image.flags.writeable = False
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = hands.process(image)
                    if results.multi_hand_landmarks:
                        self.hand_on_img = True
                        self.index_tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        self.middle_tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                        self.ring_tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                        self.pinky_tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.PINKY_TIP]
                        self.thumb_tip = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.THUMB_TIP]
                        self.ring_mcp = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                        self.wrist = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.WRIST]
                        self.index_mcp = results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    else: self.hand_on_img = False
                    
                    if self.img_state == 1:
                        # Draw the hand annotations on the image.
                        image.flags.writeable = True
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        if results.multi_hand_landmarks:
                            for hand_landmarks in results.multi_hand_landmarks:
                                mp_drawing.draw_landmarks(
                                    image,
                                    hand_landmarks,
                                    mp_hands.HAND_CONNECTIONS,
                                    mp_drawing_styles.get_default_hand_landmarks_style(),
                                    mp_drawing_styles.get_default_hand_connections_style())
                        # Flip the image horizontally for a selfie-view display.
                        image = cv2.flip(image, 1)
                        
                        #Text on image
                        if self.text_on_img: 
                            cv2.putText(image, self.text,  
                                self.text_style["bottom_left_corner"], 
                                self.text_style["font"], 
                                self.text_style["font_scale"],
                                self.text_style["font_color"],
                                self.text_style["thickness"],
                                self.text_style["line_type"])

                        #Displaying image
                        cv2.imshow('MediaPipe Hands', image)
                        (cv2.waitKey(5) & 0xFF == 27) # This line is neccessary for the image to show up

                    elif self.img_state == 2:                                     #Close the window then set showImg to 0 (off)
                            try:
                                cv2.destroyWindow('MediaPipe Hands')
                            except: pass
                            self.img_state = 0
                    if self.stop_thread:
                        break

        self.thread = threading.Thread(target = loop)
        self.thread.start()

    def stop(self):
        self.stop_thread = True
        self.thread.join()
        self.cap.release()
    
    def img_on(self):
            self.img_state = 1
    def img_off(self):
            self.img_state = 2

    def set_text(self, text_to):
        self.text = text_to
    def text_on(self):
        self.text_on_img = True
    def text_off(self):
        self.text_on_img = False