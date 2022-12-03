from pico2d import *
import game_world

class BossTear:

    def __init__(self, x=700, y=400, velocity=1, v=1):
        BossTear.image = load_image('Image/boss_tear.png')
        self.x, self.y, self.velocity, self.v = x, y, velocity, v


    def draw(self):
        self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velocity
        self.y += self.v
        if self.x < 100 or self.x > 700 or self.y < 100 or self.y > 400:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, other, group):
        if group == 'boss_tear:red_isaac':
            game_world.remove_object(self)
