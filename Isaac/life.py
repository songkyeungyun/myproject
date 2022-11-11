from pico2d import *
import game_world

class Life():
    def __init__(self):
        Life.image = load_image('Image/life3.png')
        self.x = 600
        self.y = 550

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass
