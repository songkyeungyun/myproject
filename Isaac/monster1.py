from pico2d import *
import game_framework

class Monster_1():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.frame = 0
        self.dir = 1
        self.image = load_image('Image/monster2 animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 4
        self.x += self.dir*2
        if self.x > 400:
            self.dir = -1
            self.x = 400
        elif self.x < 100:
            self.dir = 1
            self.x = 100

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(self.frame * 33, 30, 25, 35, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 33, 30, 25, 35, self.x, self.y)