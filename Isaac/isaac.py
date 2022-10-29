from pico2d import *
import game_framework

class Isaac:
    def __init__(self):
        self.x = 400
        self.y = 255
        self.frame = 0
        self.dir_x = 0
        self.dir_y = 0
        self.image = load_image('Image/animation.png')
        self.isaac_image = load_image('Image/isaac.png')
        self.head_image = load_image('Image/1png.png')
        self.head_1_image = load_image('Image/2.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir_x*5
        self.y += self.dir_y*5
        if self.x > 700:
            self.x = 700
        if 245 <= self.y <= 285:
            if self.x < 70:
                self.x = 70
        elif self.x < 100:
            self.x = 100
        if 380 <= self.x <= 420:
            if self.y < 80:
                self.y = 80
            elif self.y > 430:
                self.y = 430
        elif self.y < 100:
            self.y = 100
        elif self.y > 400:
            self.y = 400

    def draw(self):
        if self.dir_x == 1:
            self.image.clip_draw(self.frame * 49, 0, 45, 80, self.x, self.y)
        elif self.dir_x == -1:
            self.image.clip_composite_draw(self.frame * 50, 0, 45, 80, 3.141592, 'v', self.x, self.y, 45, 80)
        elif self.dir_y == -1 or self.dir_y == 1:
            self.image.clip_draw(self.frame * 49, 90, 50, 80, self.x, self.y)
        elif self.dir_x == 0:
            self.isaac_image.draw(self.x, self.y-10)