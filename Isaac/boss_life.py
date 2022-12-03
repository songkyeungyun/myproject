from pico2d import *
import game_world

class BossLife():
    def __init__(self):
        BossLife.image = load_image('Image/boss life.png')
        self.x = 400
        self.y = 480

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

