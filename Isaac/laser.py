from pico2d import *
import game_world


class Laser:

    def __init__(self, x, y):
        Laser.image = load_image('Image/laser.png')
        self.x = x
        self.y = y

    def draw(self):
        self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10
