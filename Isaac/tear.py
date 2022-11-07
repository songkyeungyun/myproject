from pico2d import *

import game_world

class Tear:
    image = None

    def __init__(self, x=700, y=400, velocity=1, v=1):
        if Tear.image == None:
            Tear.image = load_image('Image/tear.png')
        self.x, self.y, self.velocity, self.v = x, y, velocity, v

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity
        self.y += self.v
        if self.x < 100 or self.x > 700  or self.y < 100 or self.y > 400 :
            game_world.remove_object(self)