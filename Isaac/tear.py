from pico2d import *

import game_world

class Tear:
    image = None

    def __init__(self, x=800, y=300, velocity=1):
        if Tear.image == None:
            Tear.image = load_image('tear.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity
        if self.x < 120 or self.x > 700 - 20 or self.y < 120 or self.y > 400 - 20:
            game_world.remove_object(self)