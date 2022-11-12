from pico2d import *
import game_framework
import Stage.stage0_state as stage0_state
import game_world
import pick_item

from isaac import Isaac
from life import Life
from item import Item

isaac = None
stage = None
item = None
life = None

class Stage:
    def __init__(self):
        self.image = load_image('Image/stage2.png')

    def draw(self):
        self.image.draw(400, 300)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            isaac.handle_event(event)

def enter():
    global isaac, stage, life, item
    isaac = Isaac(400, 120)
    stage = Stage()
    item = Item()
    life = Life()
    game_world.add_object(life, 1)
    game_world.add_object(item, 1)
    game_world.add_object(isaac, 1)
    game_world.add_collision_group(isaac, item, 'isaac:item')

    pass

def exit():
    game_world.clear()


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            a.handle_collision(b, group)
            b.handle_collision(a, group)
    if isaac.y <= 80 and 380 <= isaac.x <= 420:
        isaac.dir_x = 0
        isaac.dir_y = 0
        game_framework.pop_state()
    if isaac.change == 2:
        isaac.change = 3
        game_framework.push_state(pick_item)




def draw_world():
    stage.draw()
    for game_object in game_world.all_objects():
        game_object.draw()

# 게임 월드 렌더링
def draw():
    clear_canvas()
    draw_world()
    update_canvas()

def pause():
    game_world.remove_object(isaac)
    game_world.remove_object(item)
    pass

def resume():
    game_world.add_object(isaac, 1)
    isaac.image = load_image('Image/red_animation.png')
    isaac.isaac_image = load_image('Image/red_isaac.png')
    pass

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True


def test_self():
    import sys
    this_module = sys.modules['__main__']
    pico2d.open_canvas()
    game_framework.run(this_module)
    pico2d.close_canvas()


if __name__ == '__main__':
    test_self()




