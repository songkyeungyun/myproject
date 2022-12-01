from pico2d import *
import game_framework
import Stage.stage0_state as stage0_state
import game_world


from monster2 import Monster_2
from life import Life
from isaac import Isaac
from block1 import Block

import server

class Stage:
    def __init__(self):
        self.image = load_image('Image/stage1.png')

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
    server.isaac = Isaac(680, 255)
    stage = Stage()
    server.life = Life()
    game_world.add_object(server.life, 1)
    server.monster2 = [Monster_2() for i in range(4)]
    server.block1 = [Block() for i in range(4)]
    game_world.add_object(server.isaac, 1)
    server.monster2[0].y, server.monster2[0].x = 400, 100
    server.monster2[1].y, server.monster2[1].x = 100, 100
    server.monster2[2].y, server.monster2[2].x = 400, 700
    server.monster2[3].y, server.monster2[3].x = 100, 700
    server.block1[0].y, server.block1[0].x = 350, 100
    server.block1[1].y, server.block1[1].x = 350, 150
    server.block1[2].y, server.block1[2].x = 150, 700
    server.block1[3].y, server.block1[3].x = 150, 650
    game_world.add_objects(server.monster2, 1)
    game_world.add_objects(server.block1, 1)
    game_world.add_collision_group(server.isaac, server.monster2, 'isaac:monster2')
    game_world.add_collision_group(server.isaac, server.block1, 'isaac:block1')
    game_world.add_collision_group(server.monster2, server.block1, 'monster2:block1')
    game_world.add_collision_group(None, server.monster2, 'tear:monster2')


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
    if server.isaac.x >= 700 and 245 <= server.isaac.y <= 285:
        server.isaac.dir_x = 0
        server.isaac.dir_y = 0
        game_framework.pop_state()


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
    game_world.remove_object(server.monster2)
    pass

def resume():
    game_world.add_object(server.isaac, 1)
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




