from pico2d import *
import game_framework

class Tear:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.tear_image = load_image('Image/tear.png')
        self.item = None
        self.speed = [0, 0]

    def update(self):
        if self.x > 700 or self.x < 100 or self.y > 400 or self.y < 100:
            self.item = None
            self.speed[0] = 0
            self.speed[1] = 0
        pass
    def draw(self):
        if self.item == 'tear':
            self.tear_image.draw(self.x, self.y)
        self.x += self.speed[0]
        self.y += self.speed[1]