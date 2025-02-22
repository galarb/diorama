from Diorama import Diorama
from time import sleep
from machine import Pin
import _thread

# Define motor settings
encoder1_pin = 14
encoder2_pin = 12
in1_pin = 0
in2_pin = 4
wheel_size = 65

# Create a Diorama instance with motor configuration
diorama = Diorama(
    button1_pin=25, 
    button2_pin=26, 
    speedup_pin=32, 
    speeddown_pin=33, 
    neo_pin=5, 
    num_pix=62,
    encoder1_pin=encoder1_pin,
    encoder2_pin=encoder2_pin,
    in1_pin=in1_pin,
    in2_pin=in2_pin,
    wheel_size=wheel_size
)

# LED control task (Core 0)
def neotask():
    while True:
        if diorama.get_button1_state():
            diorama.rainbow()  # Active state LED effect
        else:
            diorama.heartbeat()  # Turn off LEDs when stopped

# Motor control and button handling (Core 1)
def main_task():
    while True:
        diorama.run()
        sleep(0.01)
        pass

# Start the LED task on Core 0
_thread.start_new_thread(neotask, ())

# Run motor control on Core 1
main_task()

