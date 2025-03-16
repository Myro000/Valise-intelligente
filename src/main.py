import time
import cv2
from controle_moteur import move_forward, stop, turn_left, turn_right
from detection_obstacles import obstacle_detected
from human_tracking import get_user_position

def main():

    while True:
        # Vérifier s'il y a un obstacle
        if obstacle_detected():
            stop()
            time.sleep(0.5)
            continue  # Ne pas avancer si un obstacle est détecté


        from human_tracking import user_x1, user_x2, frame_width

        # Vérifier si une personne est détectée
        if user_x1 is None or user_x2 is None:
            stop()
            continue

        user_position = get_user_position(user_x1, user_x2, frame_width)

        if user_position == "gauche":
            turn_left()  # Faire tourner à gauche

        elif user_position == "droite":
            turn_right()  # Faire tourner à droite

        else:
            move_forward()

        time.sleep(0.1)  # Pause pour éviter une surcharge CPU

if __name__ == "__main__":
    main()
