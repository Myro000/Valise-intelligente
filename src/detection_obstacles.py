import RPi.GPIO as GPIO
import time

TRIG, ECHO = 22, 23

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        end_time = time.time()

    distance = (end_time - start_time) * 34300 / 2  # Conversion en cm
    return distance

def obstacle_detected():
    distance = get_distance()
    return distance < 40  # Détecte un obstacle si < 40 cm


