import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led_pin = 18

GPIO.setup(led_pin, GPIO.OUT)

print("LED on")
GPIO.output(led_pin, GPIO.HIGH)
time.sleep(2)

print("LED off")
GPIO.output(led_pin, GPIO.LOW)

# Clean up GPIO settings
GPIO.cleanup()

