"""
Subject module project in Computer Science
Semester: F2022
Authors: Azita Sofie Tadayoni, 68888
Emma Kathrine Derby Hansen, 71433
Alexander Kiellerup Swystun 72048
Áron Kuna 70492
"""
# Setting up libraries
from finger_positions import get_positions
from send_udp import send

# Main loop
while True:
# Calculate relative finger distances
        finger_distances, send_message = get_positions()

# SENDING UPD MESSAGE
        if send_message:
                send(finger_distances)