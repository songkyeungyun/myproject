from pico2d import *
from tear import Tear
import game_world


RD, LD, RU, LU, WD, SD, WU, SU, SPACE = range(9)
event_name = ['RD', 'LD', 'RU', 'LU', 'TIMER', 'SPACE', 'WD', 'SD', 'WU', 'SU']

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

class IDLE:
    @staticmethod
    def enter(self, event):
        self.dir_x = 0
        self.dir_y = 0

    @staticmethod
    def exit(self, event):
        if SPACE == event:
            self.fire_ball()

    @staticmethod
    def do(self):
        self.frame = (self.frame + 1) % 8


    @staticmethod
    def draw(self):
        if self.dir_x == 0:
            self.isaac_image.draw(self.x, self.y - 10)


class RLRUN:
    def enter(self, event):
        if event == RD:
            self.dir_x += 1
        elif event == LD:
            self.dir_x -= 1
        elif event == RU:
            self.dir_x -= 1
        elif event == LU:
            self.dir_x += 1

    def exit(self, event):
        self.face_dir = self.dir_x
        if SPACE == event:
            self.fire_ball()

    def do(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir_x
        self.x = clamp(0, self.x, 800)

    def draw(self):
        if self.dir_x == 1:
            self.image.clip_draw(self.frame * 49, 0, 45, 80, self.x, self.y)
        elif self.dir_x == -1:
            self.image.clip_composite_draw(self.frame * 50, 0, 45, 80, 3.141592, 'v', self.x, self.y, 45, 80)

class UDRUN:
    def enter(self, event):
        if event == WD:
            self.dir_y += 1
        elif event == SD:
            self.dir_y -= 1
        elif event == WU:
            self.dir_y -= 1
        elif event == SU:
            self.dir_y += 1

    def exit(self, event):
        self.face_dir = self.dir_y
        if SPACE == event:
            self.fire_ball()

    def do(self):
        self.frame = (self.frame + 1) % 8
        self.y += self.dir_y
        self.y = clamp(100, self.y, 400)

    def draw(self):
        if self.dir_y == -1 or self.dir_y == 1:
            self.image.clip_draw(self.frame * 49, 90, 50, 80, self.x, self.y)


next_state = {
    IDLE: {RU: RLRUN, LU: RLRUN, RD: RLRUN, LD: RLRUN, WU: UDRUN, SU: UDRUN, WD: UDRUN, SD: UDRUN},
    RLRUN: {RU: IDLE, LU: IDLE, LD: IDLE, LD: IDLE, WU: IDLE, SU: IDLE, WD: IDLE, SD: IDLE},
    UDRUN: {RU: IDLE, LU: IDLE, LD: IDLE, LD: IDLE, WU: IDLE, SU: IDLE, WD: IDLE, SD: IDLE},
}
class Isaac:
    def __init__(self):
        self.x = 400
        self.y = 255
        self.frame = 0
        self.dir_x = 0
        self.dir_y = 0
        self.image = load_image('Image/animation.png')
        self.isaac_image = load_image('Image/isaac.png')

        self.event_que = []
        self.cur_state = IDLE
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

        if self.event_que:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state[self.cur_state][event]
            except KeyError:
                print('error:', self.cur_state.__name__, ' ', event_name[event])

            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def fire_ball(self):
        tear = Tear(self.x, self.y, self.face_dir * 2)
        game_world.add_object(tear, 1)
        print('fire ball')