"""
MAIN
Subject module project in Computer Science
Semester: F2022
Authors: Azita Sofie Tadayoni, 68888
Emma Kathrine Derby Hansen, 71433
Alexander Kiellerup Swystun 72048
Áron Kuna 70492
"""
# Setting up libraries
from finger_positions import get_positions, stop_hand_tracker
from send_udp import send
import keyboard

# Main loop
while True:
# Calculate relative finger distances
        finger_distances, send_message = get_positions()

# SENDING UPD MESSAGE
        if send_message:
                send(finger_distances)

        if keyboard.is_pressed("q") or keyboard.is_pressed("x") or keyboard.is_pressed("Esc"):
                print("You pressed q")
                stop_hand_tracker()
                break