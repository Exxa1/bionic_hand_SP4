



import cv2 # pip install opencv-python
import mediapipe as mp # pip install mediapipe
import threading
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

class Hand_track:

    #Initialize object
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.index_tip = None
        self.middle_tip = None
        self.ring_tip = None
        self.pinky_tip = None
        self.thumb_tip = None
        self.ring_mcp = None
        self.wrist = None
        self.index_mcp = None
        self.is_pinch = False
        self.click_sensitivity = 0.05    #Sensitivity of the check_if_click function. Higher value -> more sensitive -> easier to click
        self.hand_on_img = False
        self.img_state = 0                # 0 is off, 1 is on, 2 is closing window
        self.stop_thread = False
        self.img_with_hand = None
        self.text_on_img = False
        self.text = "Hello World!"
        

    def start(self):
        def loop():
            with mp_hands.Hands(
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
                        self.check_if_pinch()
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
                            font                   = cv2.FONT_HERSHEY_SIMPLEX
                            bottomLeftCornerOfText = (100,100)
                            fontScale              = 1
                            fontColor              = (0,0,255)
                            thickness              = 3
                            lineType               = 2 
                            cv2.putText(image, self.text,  
                                bottomLeftCornerOfText, 
                                font, 
                                fontScale,
                                fontColor,
                                thickness,
                                lineType)

                        #Displaying image
                        cv2.imshow('MediaPipe Hands', image)

                        self.img_with_hand = image
                        if cv2.waitKey(5) & 0xFF == 27:
                            break
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

    def check_if_pinch(self):
        if abs(self.index_tip.x - self.thumb_tip.x) < self.click_sensitivity and abs(self.index_tip.y - self.thumb_tip.y) < self.click_sensitivity and abs(self.index_tip.z - self.thumb_tip.z) < self.click_sensitivity:
            self.is_pinch = True
        else:
            self.is_pinch = False
    
    

    #NOT YET EXPLAINED IN HOW TO USE
    def is_inside_box(self, box_x0, box_y0, box_x1, box_y1):
        if self.window_width == None:
            raise Exception("Set widow size with the set_window_size(self, width, height) method")
        else:
            index_x = (1-self.index_tip.x)*self.window_width
            index_y = self.index_tip.y*self.window_width
            within_box = index_x > box_x0 and index_x < box_x1 and index_y > box_y0 and index_y < box_y1
            return within_box
        
    def set_window_size(self, width, height):
        self.window_width = width
        self.window_height = height
    
    def get_relative_index_pos(self):
        if self.window_width != None:
            index_x = (1-self.index_tip.x)*self.window_width
            index_y = self.index_tip.y*self.window_width
            return index_x, index_y
        else:
            raise Exception("Set widow size with the set_window_size(self, width, height) method")
