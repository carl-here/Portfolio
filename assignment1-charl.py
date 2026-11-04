# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 11:45:14 2026

@author: charl
"""
import math
import pyglet
import random
from pyglet import shapes


class ShapesDemo(pyglet.window.Window):
    
    def __init__(self, width, height):
        super().__init__(width, height, "Shapes")
        self.time = 0
        self.batch = pyglet.graphics.Batch()
        
        r = random.uniform(25, 100)
        x = random.uniform(r, 1280-r)
        y = random.uniform(r, 720-r)
               
        self.circle = shapes.Circle(x, y, r, color=(224, 136, 206, 255), batch=self.batch)
       
        # Set initial velocity and angle for movement
        speed = random.uniform(300, 700)
        angle = random.uniform(0.1, 2 * math.pi) #0.1 gives less chance of ball direction in a straight horizontal line.
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        
    def on_draw(self):
        """Clear the screen and draw shapes"""
        self.clear()
        self.batch.draw()
        
    def update(self, delta_time):
        """Animate the shapes"""
    # Oppdater posisjon basert på hastighet og tid
        self.circle.x += self.vx * delta_time
        self.circle.y += self.vy * delta_time
        
        radius = self.circle.radius
        width, height = self.get_size()
        
        # Kollisjon med høyre og venstre vegg
        if self.circle.x + radius >= width or self.circle.x + 0 <= radius:
            self.vx = -self.vx 
        
        # Kollisjon med øvre og nedre vegg
        if self.circle.y + radius >= height or self.circle.y + 0 <= radius:
            self.vy = -self.vy #ganger det ene tallet med minus for å endre fortegn på svaret



if __name__ == "__main__":
    demo = ShapesDemo(1280, 720)
    pyglet.clock.schedule_interval(demo.update, 1/60) #seconds (time) between intervals
    pyglet.app.run()