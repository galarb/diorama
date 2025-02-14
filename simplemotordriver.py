from machine import Pin, PWM
import time 
import math
import random
recorded_values = []
recorded_valuesproc = []

class simplemotordriver:
    def __init__(self, encoder1_pin, encoder2_pin, in1_pin, in2_pin, wheel_size):
        self.encoder1 = Pin(encoder1_pin, Pin.IN)
        self.encoder1.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.encoder1_irq_handler)
        self.encoder2 = Pin(encoder2_pin, Pin.IN)

        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.pwm1 = PWM(self.in1)
        self.pwm2 = PWM(self.in2)
        self.pwm1.freq(1000)
        self.pwm2.freq(1000)
        self.wheel_size = wheel_size
        self.degrees = 0
        
        self.last_error = 0
        self.cum_error = 0
        self.previous_time = time.ticks_us()
        self.integral_flag = False
        

        #stop the motor hard
        self.pwm1.duty(1023)
        self.pwm2.duty(1023)    

        
    def encoder1_irq_handler(self, pin):
        encoder1_state = self.encoder1.value()
        encoder2_state = self.encoder2.value()
        
        if encoder1_state == encoder2_state:
            self.degrees += 1
        else:
            self.degrees -= 1
        if self.degrees > 20000:
            degrees = 0
        #print("Degrees: ", self.degrees)

    def motgo(self, speed):
        pwm_value = int(min(max(abs(speed), 0), 100) * 10.23)  # Map -100 to 100 to 0 to 1023

        if speed > 0:
            # Forward direction
            self.pwm1.duty(pwm_value)
            self.pwm2.duty(0)
        elif speed < 0:
            # Reverse direction
            self.pwm1.duty(0)
            self.pwm2.duty(pwm_value)
        else:
            # Stop the motor
            self.pwm1.duty(0)
            self.pwm2.duty(0)    

    
    def stophard(self):
            self.pwm1.duty(1023)
            self.pwm2.duty(1023)
            
    def PIDcalc(self, inp, sp, kp, ki, kd, color):
        current_time = time.ticks_us()
        elapsed_time = (current_time - self.previous_time) / 1000000.0

        # Ensure elapsed_time is positive to avoid division by zero
        if elapsed_time <= 0:
            if self.last_error != 0:
                return self.last_error
            else:
                return 0

        # Calculate error
        error = sp - inp

        # Reset integral term if error changes direction
        if error * self.last_error < 0:
            self.integral_flag = True
            self.cum_error = 0
        else:
            self.integral_flag = False

        # Update integral only if not flagged
        if not self.integral_flag:
            self.cum_error += error * elapsed_time

        # Calculate derivative and output
        rate_error = (error - self.last_error) / elapsed_time
        out = kp * error + ki * self.cum_error + kd * rate_error

        # Save current error and time for next iteration
        self.last_error = error
        self.previous_time = current_time

        # Clamp output to motor limits
        out = max(-254, min(254, out))
        #recorded_values.append(out)  # Record the value

        
        
        # Return PID output
        return out


    
    
    

    def godegrees(self, angle, times):
        for _ in range(times):
            motspeed = self.PIDcalc(angle, self.degrees, 1, 1, 0)
            motspeed = max(-254, min(254, motspeed))  # Clamp the speed to [-254, 254]
            self.motgo(motspeed)
    
    def test(self,times):
        for _ in range(times):
            motspeed = self.PIDcalc(90, self.degrees, 1, 0, 0, color565(255, 255, 0))
            #motspeed = max(-254, min(254, motspeed))
            recorded_valuesproc.append(int(motspeed))
        print("Recorded PIDcalc out:", recorded_values)
        print("Recorded processed:", recorded_valuesproc)
    
    def godegreesp(self, angle, times, kp, ki, kd, color, line_index, plotflag=True):
        for _ in range(times):
            motspeed = self.PIDcalc(angle, self.degrees, kp, ki, kd, color)
            motspeed = max(-254, min(254, motspeed))
            self.motgo(motspeed)
            recorded_valuesproc.append(int(motspeed))
        self.stophard()
        #print('reached ', self.degrees, 'degrees')
        # Print all recorded values at the end
        #print("Recorded processed:", recorded_valuesproc)
    def recorded_v(self):
        return recorded_valuesproc
        
    def gomm(self, distance, times):
        deg = (distance / (self.wheel_size * math.pi)) * 360
        self.godegrees(deg, times)
        dist_covered = (self.degrees * self.wheel_size * math.pi) / 360.0
        return dist_covered

    def gommp(self, distance, times, kp, ki, kd):
        deg = (distance / (self.wheel_size * math.pi)) * 360
        self.godegreesp(deg, times, kp, ki, kd)
        dist_covered = (self.degrees * self.wheel_size * math.pi) / 360.0

        return dist_covered
    def motang(self):
        return self.degrees
    
    

