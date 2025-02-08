from machine import Pin, ADC, TouchPad

from time import sleep

class Button:
    def __init__(self, button1_pin, button2_pin, speedup_pin, speeddown_pin):
        self.button1 = Pin(button1_pin, Pin.IN, Pin.PULL_UP)
        self.prev_button1_state = self.button1.value()  # Store initial state
        self.button2 = Pin(button2_pin, Pin.IN, Pin.PULL_UP)
        self.prev_button2_state = self.button2.value()  # Store initial state
        self.button1.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.button1_irq_handler)
        self.button2.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.button2_irq_handler)

        self.stat1 = False  # Initialize button states
        self.stat2 = False      # Custom Handlers for Each Button
        self.speedup = TouchPad(speedup_pin)
        self.speeddown = TouchPad(speeddown_pin)
        

    def button1_irq_handler(self, Pin):
        self.stat1 = not self.stat1  # Toggle button state
        #print("Button 1 Clicked!")
        pass
    def button2_irq_handler(self, Pin):
        self.stat2 = not self.stat2  # Toggle button state
        #print("Button 2 Clicked!")


    def get_button1_state(self):
        return self.stat1
    def get_button2_state(self):
        return self.stat2
    def gettouchup(self):
        val = self.speedup.read()
        if val < 200:
            return True
        else:
            return False
    def gettouchdown(self):
        val = self.speeddown.read()
        if val < 200:
            return True
        else:
            return False

