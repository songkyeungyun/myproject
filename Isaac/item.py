from pico2d import *
import game_world


class Item:
    def __init__(self):
        Item.image = load_image('Image/item.png')
        self.x = 400
        self.y = 280

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - 15, self.y - 23, self.x + 15, self.y + 20

    def handle_collision(self, other, group):
        if group == 'isaac:item':
            game_world.remove_object(self)