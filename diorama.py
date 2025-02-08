from simplemotordriver import simplemotordriver
from  Button import Button
from time import sleep
defaultspeed = 60
speed = defaultspeed  # Make speed persistent

disk = simplemotordriver(
            encoder1_pin= 14,
            encoder2_pin=12,
            in1_pin=0,
            in2_pin=4,
            wheel_size=65,
)

buttons = Button(25, 26, 32, 33)#start/stop, generalpurpose, touchup, touchdown
def setspeed():
    global speed  # Ensure speed updates persistently
    if buttons.gettouchup():
        speed += 10
    if buttons.gettouchdown():
        speed -= 10
    speed = max(0, min(speed, 250))  # Ensure speed is within 0-100
    return speed

for _ in range(200):
    sleep(0.1)
    if buttons.get_button1_state():#activate diorama
        print('Activated - Speed:', speed)
        disk.motgo(setspeed())
    else:#stop diorama
        print('stopped')
        sleep(1)
        disk.stophard()
        

