from pico2d import *
import game_framework

class Monster_2():
    def __init__(self):
        self.x = 700
        self.y = 350
        self.frame = 0
        self.dir = -1
        self.image = load_image('Image/monster1 animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 6
        self.x += self.dir*2
        if self.x > 700:
            self.dir = -1
            self.x = 700
        elif self.x < 400:
            self.dir = 1
            self.x = 400

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(self.frame * 30, 30, 25, 60, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 30, 30, 25, 60, self.x, self.y)