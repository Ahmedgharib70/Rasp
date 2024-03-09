import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led_pin = 18

GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        print("LED on")
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(1.0)  

        print("LED off")
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(1.5)  

except KeyboardInterrupt:
    
    GPIO.cleanup()

