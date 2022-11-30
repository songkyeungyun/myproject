from pico2d import *
import game_framework
import game_world
import pick_item
import Stage.boss_stage as boss_state

from isaac import Isaac
from life import Life
from item import Item

import server

class Stage:
    def __init__(self):
        self.image = load_image('Image/stage4.png')

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
            server.isaac.handle_event(event)

def enter():
    global stage
    server.isaac = Isaac(120, 255)
    stage = Stage()
    server.isaac.change = 3
    server.item = Item()
    server.life = Life()
    game_world.add_object(server.life, 1)
    game_world.add_object(server.isaac, 1)
    game_world.add_object(server.item, 1)
    if server.isaac.life ==3:
        Life.image = load_image('Image/life3.png')
    elif server.isaac.life ==2:
        Life.image = load_image('Image/life2.png')
    else:
        Life.image = load_image('Image/life1.png')
    game_world.add_collision_group(server.isaac, server.item, 'isaac:item')

def exit():
    game_world.clear()

def update():
    for game_object in game_world.all_objects():
        game_object.update()
    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            a.handle_collision(b, group)
            b.handle_collision(a, group)
    if server.isaac.x <= 70 and 245 <= server.isaac.y <= 285:
        server.isaac.dir_x = 0
        server.isaac.dir_y = 0
        game_framework.pop_state()
    elif server.isaac.x >= 730 and 245 <= server.isaac.y <= 285:
        server.isaac.dir_x = 0
        server.isaac.dir_y = 0
        server.isaac.x = 720
        game_framework.push_state(boss_state)
    if server.isaac.change == 2:
        server.isaac.change = 3
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
    game_world.remove_object(server.isaac)
    pass

def resume():
    game_world.add_object(server.isaac, 1)
    pass

def test_self():
    import sys
    this_module = sys.modules['__main__']
    pico2d.open_canvas()
    game_framework.run(this_module)
    pico2d.close_canvas()

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True



if __name__ == '__main__':
    test_self()




