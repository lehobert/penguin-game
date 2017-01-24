# A way to add animation to tkinter

# Combining classes AnimationCanvas and AnimatedObject into one module

# New version 19 April 2015:
# disable the start method when going
# add accelerate and decelerate methods

# Rhys Price Jones 7 April 2015

# AnimationCanvas extends tk.Canvas.  
# It allows you to add as many AnimatedObjects as you like with addItem()
# remove them with removeItem()
# start() and stop() are provided to start and stop the animation easily.
# The animate() method causes all the AnimatedObjects to start moving

import Tkinter as tk

DEFAULT_SPEED = 40 # Default 25 fps; Smaller for faster, 40 means 1 frame per 40ms == 25 fps

class AnimationCanvas(tk.Canvas):
    items = []
    
    def __init__(self, root, **kwargs):
        tk.Canvas.__init__(self, root, **kwargs)
        self.root = root
        self.speed = DEFAULT_SPEED   
        self.going = False
        
    def addItem(self, item):
        self.items.append(item)            
 
    def removeItem(self, item):
        self.items.remove(item)  
                       
    def start(self):
        if self.going: pass        # Don't start another timer if we're already going
        else:
            self.going = True
            self.after(0, self.animate())

    def accelerate(self):
        self.speed = int(round(self.speed * .70))     # decrease time between frames by 5%
        
    def decelerate(self):
        self.speed = int(round(self.speed*1.30))     # increase time between frames by 5%
        

    def animate(self):
        for item in self.items:
            item.move()
        if self.going:
            self.after(self.speed, self.animate)       # next update after SPEED milliseconds
             
    def stop(self):
        self.going = False
        self.speed = DEFAULT_SPEED 
 
    
# Class AnimatedObject is anything that can be added to a tkinter Canvas
# If it has a move() method, then  it can be added to an AnimationCanvas and animated


class AnimatedObject:       
                        
    def move(self):
        raise NotImplementedError('*move* method needs to be implemented in class inheriting from AnimatedObject.')
