from machine import Pin, ADC, TouchPad
import neopixel
from time import sleep, ticks_ms
from simplemotordriver import simplemotordriver
import math
class Diorama:
    def __init__(self, button1_pin, button2_pin, speedup_pin, speeddown_pin, neo_pin, num_pix,
                 encoder1_pin, encoder2_pin, in1b_pin, in2b_pin, in1d_pin, in2d_pin, wheel_size):
        self.button1 = Pin(button1_pin, Pin.IN, Pin.PULL_UP)
        self.button2 = Pin(button2_pin, Pin.IN, Pin.PULL_UP)
        self.button1.irq(trigger=Pin.IRQ_FALLING, handler=self.button1_irq_handler)
        self.button2.irq(trigger=Pin.IRQ_FALLING, handler=self.button2_irq_handler)

        self.stat1 = False
        self.stat2 = False
        self.speedup = TouchPad(Pin(speedup_pin))
        self.speeddown = TouchPad(Pin(speeddown_pin))
        self.last_interrupt_time1 = 0
        self.last_interrupt_time2 = 0
        self.debounce_time = 300  # 300 ms debounce time
        
        self.speed = 60  # Default Speed
        
        # NeoPixel Strip Initialization
        self.num_pix = num_pix
        self.strip = neopixel.NeoPixel(Pin(neo_pin), num_pix)
        self.set_leds(0, 0, 0)  # Turn off LEDs on start

        # Motor Driver Setup from Arguments
        self.base = simplemotordriver(
            encoder1_pin=encoder1_pin,
            encoder2_pin=encoder2_pin,
            in1_pin=in1b_pin,
            in2_pin=in2b_pin,
            wheel_size=wheel_size,
        )
        self.disk = simplemotordriver(
            encoder1_pin=2,
            encoder2_pin=15,
            in1_pin=in1d_pin,
            in2_pin=in2d_pin,
            wheel_size=wheel_size,
        )
        self.base.stophard()
        self.disk.stophard()
    # ---- IRQ Handlers with Debounce ----
    def button1_irq_handler(self, pin):
        current_time = ticks_ms()
        if current_time - self.last_interrupt_time1 > self.debounce_time:
            self.last_interrupt_time1 = current_time
            self.stat1 = not self.stat1  # Toggle state

    def button2_irq_handler(self, pin):
        current_time = ticks_ms()
        if current_time - self.last_interrupt_time2 > self.debounce_time:
            self.last_interrupt_time2 = current_time
            self.stat2 = not self.stat2  # Toggle state

    # ---- Button State Getters ----
    def get_button1_state(self):
        return self.stat1

    def get_button2_state(self):
        return self.stat2

    # ---- Touch Sensor Handlers ----
    def gettouchup(self):
        return self.speedup.read() < 200

    def gettouchdown(self):
        return self.speeddown.read() < 200

    # ---- LED Control ----
    def set_leds(self, r, g, b):
        for i in range(self.num_pix):
            self.strip[i] = (r, g, b)
        self.strip.write()
    
    def set_color(self, r, g, b):
        """Set all pixels to the same color."""
        for i in range(self.num_pix):
            self.strip[i] = (r, g, b)
        self.strip.write()
    
    def rainbow(self):
        for color in range(255):
            for pixel in range(self.num_pix):
                pixel_index = (pixel * 256 // self.num_pix) + color * 10
                self.strip[pixel] = self.colorwheel(pixel_index & 255)
            self.strip.write()
            sleep(0.001) 

    def heartbeat(self, r=255, g=0, b=0, fade_speed=0.1):
        """Creates a low-intensity slow fade-in and fade-out effect for NeoPixels."""
        min_brightness = 0
        max_brightness = 80  # Keep intensity low

        # Fade in
        for i in range(0, 100, 10):  # Steps of 10 for fewer iterations
            intensity = int(max_brightness * (math.sin(math.radians(i))**2))
            self.set_color(
                int((r * intensity) / 255),
                int((g * intensity) / 255),
                int((b * intensity) / 255)
            )
            sleep(fade_speed)

        # Fade out
        for i in range(100, -1, -10):
            intensity = int(max_brightness * (math.sin(math.radians(i))**2))
            self.set_color(
                int((r * intensity) / 255),
                int((g * intensity) / 255),
                int((b * intensity) / 255)
            )
            sleep(fade_speed)
        
    def colorwheel(self, pos):
        """Returns an RGB color based on a 0-255 position on the color wheel."""
        pos = pos % 256  # Ensure value is always between 0-255
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)  # Red → Green
        elif pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)  # Green → Blue
        else:
            pos -= 170
            return (pos * 3, 0, 255 - pos * 3)  # Blue → Red 

    def stripup(self):
        self.set_leds(0, 0, 0)
        for i in range(self.num_pix):
            self.strip[i] = (0, 255, 0)
            self.strip.write()
            sleep(0.01)
            self.strip[i - 1] = (0, 0, 0)
            self.strip.write()

    def stripdown(self):
        self.set_leds(0, 0, 0)
        for i in range(self.num_pix - 1, -1, -1):
            self.strip[i] = (255, 0, 0)
            self.strip.write()
            sleep(0.02)
            self.strip[i] = (0, 0, 0)

    # ---- Speed Control ----
    def setspeed(self):
        if self.gettouchup():
            self.speed = min(100, self.speed + 10)
            self.stripup()
        if self.gettouchdown():
            self.speed = max(0, self.speed - 10)
            self.stripdown()
        print('speed= ',self.speed)
        return self.speed

    # ---- Run Function ----
    def run(self):
        if self.get_button1_state():
            print('Activated - Speed:', self.speed)
            self.base.motgo(self.setspeed())
            self.disk.motgo(self.setspeed())
            #self.rainbow()
        else:
            print('Stopped')
            self.base.stophard()
            #self.heartbeat()  # Add heartbeat effect

    # ---- Go to a Specific Angle ----
    def godeg(self, deg):
        self.base.godegreesp(deg, 1000, 1, 0, 0, 0, 0, plotflag=False)
    def motgo(self, spee):
        self.base.motgo(spee)

