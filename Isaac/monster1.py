from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

PIXEL_PER_METER = 10.0 / 0.3
RUN_SPEED_KPH = 20
RUN_SPEED_MPM = RUN_SPEED_KPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

import monster2
class Monster_1():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.frame = 0
        self.dir = 1
        self.image = load_image('Image/monster2 animation.png')
        self.life = 3

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.x > 700:
            self.dir = -1
            self.x = 700
        elif self.x < 100:
            self.dir = 1
            self.x = 100

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 33, 30, 25, 35, self.x, self.y, 35, 35)
        else:
            self.image.clip_composite_draw(int(self.frame) * 33, 30, 25, 35, 3.141592, 'v', self.x, self.y, 35, 35)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, other, group):

        if group == 'isaac:monster1':
            self.dir = self.dir * -1
        if group == 'tear:monster1':
            if self.life == 3:
                self.life = 2
            elif self.life == 2:
                self.life = 1
            elif self.life == 1:
                game_world.remove_object(self)
