from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

PIXEL_PER_METER = 10.0 / 0.3
RUN_SPEED_KPH = 15
RUN_SPEED_MPM = RUN_SPEED_KPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

class Monster_2():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.frame = 0
        self.dir = -1
        self.image = load_image('Image/monster1 animation.png')
        self.life = 3

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.x += self.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.x > 700:
            self.dir = -1
            self.x = 700
        elif self.x < 100:
            self.dir = 1
            self.x = 100

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(int(self.frame) * 30, 30, 25, 60, self.x, self.y, 45, 60)
        else:
            self.image.clip_composite_draw(int(self.frame) * 30, 30, 25, 60, 3.141592, 'v', self.x, self.y, 45, 60)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 20, self.x + 10, self.y + 10

    def handle_collision(self, other, group):
        if group == 'isaac:monster2':
            self.dir = self.dir * -1
        if group == 'tear:monster2':
            if self.life == 3: self.life = 2
            elif self.life == 2: self.life = 1
            elif self.life == 1:
                game_world.remove_object(self)