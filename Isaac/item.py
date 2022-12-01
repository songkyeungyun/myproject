from pico2d import *
import game_world
import time

class Item:
    def __init__(self):
        Item.image = load_image('Image/item.png')
        self.bgm = load_music('music/pickup.mp3')
        self.bgm.set_volume(50)
        self.x = 400
        self.y = 250
        self.time = time.time()
        self.cur_time = 0
        self.timer = 0

    def draw(self):
        self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())

    def update(self):
        self.cur_time = time.time()
        self.timer = self.cur_time - self.time
        if self.timer <= 2:
            self.y += 0.1
        elif 2< self.timer <= 4:
            self.y -= 0.1
        elif 4 < self.timer <=6:
            self.y += 0.1
        else:
            self.y -= 0.1
        pass

    def get_bb(self):
        return self.x - 15, self.y - 23, self.x + 15, self.y + 20

    def handle_collision(self, other, group):
        if group == 'isaac:item':
            self.bgm.play()
            game_world.remove_object(self)