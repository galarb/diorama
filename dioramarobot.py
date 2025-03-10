from Diorama import Diorama
from time import sleep
from machine import Pin
import _thread

# Create a Diorama instance with motors configuration
diorama = Diorama(
    button1_pin=25, 
    button2_pin=26, 
    speedup_pin=33, 
    speeddown_pin=32, 
    neo_pin=5, 
    num_pix=62,
    encoder1_pin=12,
    encoder2_pin=14,
    in1b_pin=16,#base
    in2b_pin=17,
    in1d_pin=0,#disk
    in2d_pin=4,
    wheel_size=65
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
        diorama.motgo(90)
        diorama.run()
        sleep(0.01)

# Start the LED task on Core 0
_thread.start_new_thread(neotask, ())

# Run motor control on Core 1
main_task()

