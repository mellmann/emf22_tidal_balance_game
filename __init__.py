from tidal import *
from app import App

import accelerometer

from st7789 import color565
import framebuf
from .gfx import GFX

from random import random, seed, randint
from utime import sleep_us, ticks_cpu, ticks_us
import math

class Box(object):
    """Bouncing box."""

    def __init__(self, screen_width, screen_height, size, color):
        """Initialize box.
        Args:
            screen_width (int): Width of screen.
            screen_height (int): Width of height.
            size (int): Square side length.
            color (int): RGB565 color value.
        """
        self.size  = size
        self.w     = screen_width
        self.h     = screen_height
        self.color = color

        # start in the middle
        self.x = self.w / 2
        self.y = self.h / 2
        
        self.x_speed = 0
        self.y_speed = 0
        
        self.damping_factor = 0.9
        self.sensitivity    = 50
        self.friction       = 0.95

    def update_pos(self):
        """Update box position and speed."""

        # update speed by friction
        self.x_speed *= self.friction
        self.y_speed *= self.friction
        
        (ax, ay, az) = accelerometer.get_xyz()

        # update speed with new acceleration
        self.x_speed += ax*self.sensitivity/self.size
        self.y_speed -= ay*self.sensitivity/self.size
        
        # update position
        self.x += self.x_speed
        self.y += self.y_speed

        # collision
        if self.x < 0:
            self.x = 0
            self.x_speed = -self.x_speed * self.damping_factor
        elif self.x > (self.w - self.size):
            self.x = self.w - self.size
            self.x_speed = -self.x_speed * self.damping_factor
        if self.y < 0:
            self.y = 0
            self.y_speed = -self.y_speed * self.damping_factor
        elif self.y > (self.h - self.size):
            self.y = self.h - self.size
            self.y_speed = -self.y_speed * self.damping_factor

    def draw(self, buf):
        """Draw box."""
        x = int(self.x)
        y = int(self.y)
        size = self.size
        buf.fill_rect(x, y, size, size, self.color)



class BufferedDisplay:

    def __init__(self, display):
    
        self.display = display
        self.width   = display.width()
        self.height  = display.height()

        # offscreen buffer
        self.buffer = bytearray(self.width * self.height * 2)
        self.frame = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.RGB565)

        # additional graphics for drawing circles and triangles
        self.gfx = GFX(self.height, self.width, pixel = self.frame.pixel, hline=self.frame.hline, vline=self.frame.vline)
        
    def show(self):
        b = memoryview(self.buffer)
        
        # render display
        self.display.blit_buffer(b, 0, 0, self.width, self.height)
        
        # clear buffer
        self.frame.fill(0)

        

class MyApp(App):
    
    def on_activate(self):
        super().on_activate()

        self.buttons.on_press(JOY_CENTRE, self.reset)

        self.bdisplay = BufferedDisplay(display)
        
        led[0] = (0, 0, 0)
        led_power_on(True)
        
        # create the boxes
        self.reset()
        
        self.running = True
        
        #self.timer = self.periodic(40, self.update)
        self.update()
        
    def reset(self):
        # we ave only one box for now
        self.boxes = [Box(self.bdisplay.width - 1, self.bdisplay.height - 1, 20, self.radom_color())]
        
    def radom_color(self):
        return color565(randint(30, 256), randint(30, 256), randint(30, 256))
        
    def on_deactivate(self):
        #self.timer.cancel()
        led[0] = (0, 0, 0)
        led_power_on(False)
        super().on_deactivate()
        
    def update(self):

        if not self.is_active():
            return
        
        o = 20
        cx = self.bdisplay.height / 2
        cy = self.bdisplay.width / 2
        color = color565(0, 0, 255)
        led[0] = (0, 255, 0) # Green
        
        for b in self.boxes:
            b.update_pos()
            
            # check if the box collided with the frame
            if b.x + b.size > self.bdisplay.width-o or b.x < o or b.y + b.size > self.bdisplay.height-o or b.y < o:
                color = color565(0, 255, 0)
                led[0] = (255, 0, 0) # Red
                
        
        # the outer part indicated if the box collided with the frame
        self.bdisplay.frame.fill(color)
        # the inner part is black
        self.bdisplay.frame.fill_rect(o, o, self.bdisplay.width-o*2, self.bdisplay.height-o*2, BLACK)
        #self.bdisplay.gfx.circle(50, 50, 30, RED)
        
        led.write()
            
        for b in self.boxes:
            b.draw(self.bdisplay.frame)
                    
        # draw the buffer to the screen
        self.bdisplay.show()
        
        # asynchroneously call this method again in 1ms
        self.after(1, self.update)

        
            

# Set the entrypoint for the app launher
main = MyApp