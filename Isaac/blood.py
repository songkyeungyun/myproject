from pico2d import *
import game_world

class Blood():
    def __init__(self):
        Blood.image = load_image('Image/blood.png')
        self.x = 0
        self. y = 0

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass