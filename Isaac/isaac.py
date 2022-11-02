from pico2d import *
import game_framework


# RD, LD, RU, LU, WD, SD, WU, SU = range(8)
#
# key_event_table = {
#     (SDL_KEYDOWN, SDLK_RIGHT): RD,
#     (SDL_KEYDOWN, SDLK_LEFT): LD,
#     (SDL_KEYUP, SDLK_RIGHT): RU,
#     (SDL_KEYUP, SDLK_LEFT): LU,
#     (SDL_KEYDOWN, SDLK_UP): WD,
#     (SDL_KEYDOWN, SDLK_DOWN): SD,
#     (SDL_KEYUP, SDLK_UP): WU,
#     (SDL_KEYUP, SDLK_DOWN): SU
# }
#
#
# next_state = {
#     IDLE: {RU: RUN, LU: RUN, RD: RUN, LD: RUN, TIMER: SLEEP, AU: AUTO},
#     RUN: {RU: IDLE, LU: IDLE, LD: IDLE, LD: IDLE, AU: AUTO},
#     SLEEP: {RU: RUN, LU: RUN, RD: RUN, LD: RUN},
#     AUTO: {AU: IDLE, RD: RUN, LD: RUN, RU: RUN, LU: RUN}
# }
class Isaac:
    def __init__(self):
        self.x = 400
        self.y = 255
        self.frame = 0
        self.dir_x = 0
        self.dir_y = 0
        self.image = load_image('Image/animation.png')
        self.isaac_image = load_image('Image/isaac.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir_x*5
        self.y += self.dir_y*5
        self.x = clamp(100, self.x, 700)
        self.y = clamp(100, self.y, 400)

    def draw(self):
        if self.dir_x == 1:
            self.image.clip_draw(self.frame * 49, 0, 45, 80, self.x, self.y)
        elif self.dir_x == -1:
            self.image.clip_composite_draw(self.frame * 50, 0, 45, 80, 3.141592, 'v', self.x, self.y, 45, 80)
        elif self.dir_y == -1 or self.dir_y == 1:
            self.image.clip_draw(self.frame * 49, 90, 50, 80, self.x, self.y)
        elif self.dir_x == 0:
            self.isaac_image.draw(self.x, self.y-10)