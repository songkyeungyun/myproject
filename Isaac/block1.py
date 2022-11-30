from pico2d import *
import game_world

class Block:
    def __init__(self):
        Block.image = load_image('Image/block.png')
        self.x = 0
        self.y = 0

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, other, group):
        pass