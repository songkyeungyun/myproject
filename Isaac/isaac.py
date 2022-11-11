from pico2d import *
from tear import Tear
from redtear import RedTear
import game_world
import game_framework
import time

from life import Life
import Stage.stage1_state as stage1_state

NULL, RD, LD, RU, LU, WD, SD, WU, SU, SPACE = range(10)
event_name = ['Null','RD', 'LD', 'RU', 'LU', 'SPACE', 'WD', 'SD', 'WU', 'SU']

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_RIGHT): RD,
    (SDL_KEYDOWN, SDLK_LEFT): LD,
    (SDL_KEYUP, SDLK_RIGHT): RU,
    (SDL_KEYUP, SDLK_LEFT): LU,
    (SDL_KEYDOWN, SDLK_UP): WD,
    (SDL_KEYDOWN, SDLK_DOWN): SD,
    (SDL_KEYUP, SDLK_UP): WU,
    (SDL_KEYUP, SDLK_DOWN): SU
}

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class IDLE:
    @staticmethod
    def enter(self, event):
        self.dir_x = 0
        self.dir_y = 0

    @staticmethod
    def exit(self, event):
        if SPACE == event:
            self.attack()

    @staticmethod
    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8


    @staticmethod
    def draw(self):
        if self.dir_x == 0:
            self.isaac_image.draw(self.x, self.y - 10)


class RUN:
    def enter(self, event):
        if event == RD:
            self.key[1] = True
            self.dir_x = 1
        if event == LD:
            self.key[0] = True
            self.dir_x = -1
        if event == RU:
            self.key[1] = False
        if event == LU:
            self.key[0] = False

        if event == WD:
            self.key[3] = True
            self.dir_y = 1
        if event == SD:
            self.key[2] = True
            self.dir_y = -1
        if event == WU:
            self.dir_y = 0
            self.key[3] = False
        if event == SU:
            self.dir_y = 0
            self.key[2] = False

        for key in self.key:
            if key is True: return

        if self.dir_x == 0:
            self.face_diry = self.dir_y
        elif self.dir_y == 0:
            self.face_dirx = self.dir_x
        self.add_event(NULL)

    def exit(self, event):
        if SPACE == event:
            self.attack()


    def do(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        self.x += self.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        self.y += self.dir_y * RUN_SPEED_PPS * game_framework.frame_time
        if 245 < self.y < 285:
            self.x = clamp(70, self.x, 730)
        else:
            self.x = clamp(100, self.x, 700)
        if 380 < self.x < 420:
            self.y = clamp(80, self.y, 420)
        else:
            self.y = clamp(100, self.y, 400)

    def draw(self):
        if self.dir_x == 1:
            self.image.clip_draw(int(self.frame) * 49, 0, 45, 80, self.x, self.y)
        elif self.dir_x == -1:
            self.image.clip_composite_draw(int(self.frame) * 50, 0, 45, 80, 3.141592, 'v', self.x, self.y, 45, 80)
        elif self.dir_y == -1 or self.dir_y == 1:
            self.image.clip_draw(int(self.frame) * 49, 90, 50, 80, self.x, self.y)
        elif self.dir_x == 0:
            self.isaac_image.draw(self.x, self.y - 10)


next_state = {
    IDLE: {RU: RUN, RD: RUN,
           LU: RUN, LD: RUN,
           WU: RUN, WD: RUN,
           SU: RUN, SD: RUN,
           NULL: IDLE, SPACE: IDLE},
    RUN: {RU: RUN, RD: RUN,
           LU: RUN, LD: RUN,
           WU: RUN, WD: RUN,
           SU: RUN, SD: RUN,
           NULL: IDLE, SPACE: RUN},
}

PIXEL_PER_METER = 10.0 / 0.3
RUN_SPEED_KPH = 20
RUN_SPEED_MPM = RUN_SPEED_KPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER


class Isaac:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.dir_x = 0
        self.dir_y = 0
        self.face_dirx = 0
        self.face_diry = 0
        self.life = 3
        self.change = False
        if self.change == False:
            self.image = load_image('Image/animation.png')
        else:
            self.image = load_image('Image/red_animation.png')
        self.time = 0
        self.cur_time = 0
        self.timer = 0

        self.pick = False
        self.red = False

        self.isaac_image = load_image('Image/isaac.png')

        self.key = [False, False, False, False]# 0=left 1=right 2=down 3=up

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)
        self.cur_time = time.time()
        self.timer = self.cur_time - self.time
        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print('error:', self.cur_state.__name__, ' ', event_name[event])

            self.cur_state.enter(self, event)
        if self.timer < 1:
            self.pick = True
        else:
            self.red = True
            self.pick = False


    def draw(self):
        self.cur_state.draw(self)
        # draw_rectangle(*self.get_bb())

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def attack(self):
        if self.change == False:
            if self.dir_x == 0 and self.dir_y == 0:
                tear = Tear(self.x, self.y, self.face_dirx, self.face_diry)
            elif self.dir_y == 0:
                tear = Tear(self.x, self.y, self.dir_x, 0)
            elif self.dir_x == 0:
                tear = Tear(self.x, self.y, 0, self.dir_y)
            else:
                tear = Tear(self.x, self.y, self.dir_x, 0)

            game_world.add_object(tear, 1)
            game_world.add_collision_group(tear, stage1_state.monster1, 'tear:monster1')
            game_world.add_collision_group(tear, stage1_state.monster2, 'tear:monster2')
        if self.change == True:
            if self.dir_x == 0 and self.dir_y == 0:
                redtear = RedTear(self.x, self.y, self.frame, self.frame)
            elif self.dir_y == 0:
                redtear = RedTear(self.x, self.y, self.frame, 0)
            elif self.dir_x == 0:
                redtear = RedTear(self.x, self.y, 0, self.frame)
            else:
                redtear = RedTear(self.x, self.y, self.frame, 0)

            game_world.add_object(redtear, 1)
            game_world.add_collision_group(redtear, stage1_state.monster1, 'redtear:monster1')
            game_world.add_collision_group(redtear, stage1_state.monster2, 'redtear:monster2')

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 25, self.y + 30

    def handle_collision(self, other, group):
        if group == 'isaac:monster1':
            if self.life == 3:
                Life.image = load_image('Image/life2.png')
                self.life = 2
            elif self.life == 2:
                Life.image = load_image('Image/life1.png')
                self.life = 1
        if group == 'isaac:monster2':
            if self.life == 3:
                Life.image = load_image('Image/life2.png')
                self.life = 2
            elif self.life == 2:
                Life.image = load_image('Image/life1.png')
                self.life = 1
        if group == 'isaac:item':
            self.time = time.time()
            self.image = load_image('Image/red_animation.png')
            self.change = True