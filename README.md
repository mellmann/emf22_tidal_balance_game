# Balance
A simple balancing game for the TiDAL badge from EMF22.

## Game Dynamics

The game starts with a square box placed in the middle of the screen.
The box moves depending on the acceleromenetr values. 
This happens for instace when you tilt your bedge if you move it quickly.

Try to keep the box in the black middle area of the screen. If the box collides with 
the border, the border turns red and the game is lost.

## How To Play

### Alone

Practice your balance and keep the box in the middle. 
Try to walk around and move while balancing the box.

### With people

Play the game with other badge owners. 
Start at the same time and balance your badge while trying to make your apponents loose their balance.

## Future

In the future more chalanging tasks will be added.


## Implementation Remarks

* A Framebuffer is used to realize quick and flicker-free screen updates  
  https://docs.micropython.org/en/latest/library/framebuf.html
  
* NOTE: framebuffer has no methods to draw circles or triangles. For drawing them the file `gfx.py` is included  
  https://github.com/adafruit/micropython-adafruit-gfx/blob/master/gfx.py