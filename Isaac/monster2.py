from pico2d import *
import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

PIXEL_PER_METER = 10.0 / 0.3
RUN_SPEED_KPH = 25
RUN_SPEED_MPM = RUN_SPEED_KPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

class Monster_2():
    def __init__(self):
        self.x = 700
        self.y = 350
        self.frame = 0
        self.dir = -1
        self.image = load_image('Image/monster1 animation.png')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.x > 700:
            self.dir = -1
            self.x = 700
        elif self.x < 400:
            self.dir = 1
            self.x = 400

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 30, 30, 25, 60, self.x, self.y)
        else:
            self.image.clip_composite_draw(int(self.frame) * 30, 30, 25, 60, 3.141592, 'v', self.x, self.y, 25, 60)