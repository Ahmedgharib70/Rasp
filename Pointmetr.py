from gpiozero import PWMLED, MCP3008
from time import sleep
import time
pot = MCP3008(1)
led = PWMLED(18)

while True:
    if pot.value < 0.02:
        led.value = 0
    else:
        led.value = pot.value

    print(pot.value)
    sleep(1.0)

