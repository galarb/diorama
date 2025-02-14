from Diorama import Diorama
from time import sleep
from machine import Pin

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
    num_pix=8,
    encoder1_pin=encoder1_pin,
    encoder2_pin=encoder2_pin,
    in1_pin=in1_pin,
    in2_pin=in2_pin,
    wheel_size=wheel_size
)



# Main Loop
for _ in range(200):
    diorama.run()
    sleep(0.1)

