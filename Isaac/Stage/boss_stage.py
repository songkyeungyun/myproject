from pico2d import *
import game_framework
import game_world

from red_isaac import RedIsaac
from life import Life
from boss import Boss

import server

class Stage:
    def __init__(self):
        self.image = load_image('Image/boss_stage.png')

    def draw(self):
        self.image.draw(400, 300)



def enter():
    global stage
    server.red_isaac = RedIsaac(120, 240)
    stage = Stage()
    server.life = Life()
    server.boss = Boss()
    game_world.add_object(server.red_isaac, 1)
    game_world.add_object(server.life, 1)
    game_world.add_object(server.boss, 1)



# 게임 종료 - 객체를 소멸
def exit():
    game_world.clear()

# 게임 월드 객체를 업데이트 - 게임 로직
def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            a.handle_collision(b, group)
            b.handle_collision(a, group)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            server.red_isaac.handle_event(event)

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
    pass

def resume():
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




