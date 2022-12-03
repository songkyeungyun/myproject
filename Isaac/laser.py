from pico2d import *
import game_world
import time


class Laser:

    def __init__(self, x, y):
        Laser.image = load_image('Image/laser.png')
        self.x = 400
        self.y = y
        self.time = 0
        self.timer = 0
        self.cur_time = 0

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.cur_time = time.time()
        self.timer = self.cur_time - self.time
        if 2 < self.timer < 4:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 400, self.y - 30, self.x + 400, self.y + 30

    def handle_collision(self, other, group):
        if group == 'laser:red_isaac':
            pass
