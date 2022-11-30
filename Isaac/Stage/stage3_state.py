from pico2d import *
import game_framework
import Stage.stage4_state as stage4_state
import game_world

from isaac import Isaac
from monster1 import Monster_1
from life import Life
from block1 import Block

import server

class Stage:
    def __init__(self):
        self.image = load_image('Image/stage3.png')

    def draw(self):
        self.image.draw(400, 300)



def enter():
    global stage
    server.isaac = Isaac(400, 380)
    stage = Stage()
    server.life = Life()
    server.monster1 = [Monster_1() for i in range(4)]
    server.block1 = [Block() for i in range(16)]
    game_world.add_object(server.isaac, 1)
    game_world.add_object(server.life, 1)
    server.monster1[0].y, server.monster1[0].x = 400, 700
    server.monster1[1].y, server.monster1[1].x = 100, 100
    server.monster1[2].y, server.monster1[2].x = 400, 100
    server.monster1[3].y, server.monster1[3].x = 100, 700
    server.block1[0].y, server.block1[0].x = 350, 100
    server.block1[1].y, server.block1[1].x = 350, 150
    server.block1[2].y, server.block1[2].x = 350, 200
    server.block1[3].y, server.block1[3].x = 350, 250
    server.block1[4].y, server.block1[4].x = 150, 100
    server.block1[5].y, server.block1[5].x = 150, 150
    server.block1[6].y, server.block1[6].x = 150, 200
    server.block1[7].y, server.block1[7].x = 150, 250
    server.block1[8].y, server.block1[8].x = 350, 700
    server.block1[9].y, server.block1[9].x = 350, 650
    server.block1[10].y, server.block1[10].x = 350, 600
    server.block1[11].y, server.block1[11].x = 350, 550
    server.block1[12].y, server.block1[12].x = 150, 700
    server.block1[13].y, server.block1[13].x = 150, 650
    server.block1[14].y, server.block1[14].x = 150, 600
    server.block1[15].y, server.block1[15].x = 150, 550
    game_world.add_objects(server.monster1, 1)
    game_world.add_objects(server.block1, 1)
    game_world.add_collision_group(server.isaac, server.monster1, 'isaac:monster1')
    game_world.add_collision_group(server.isaac, server.block1, 'isaac:block1')
    game_world.add_collision_group(server.monster1, server.block1, 'monster1:block1')




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
    if server.isaac.y >= 420 and 380 <= server.isaac.x <= 420:
        server.isaac.dir_x = 0
        server.isaac.dir_y = 0
        game_framework.pop_state()
    elif server.isaac.x >= 730 and 245 <= server.isaac.y <= 285:
        server.isaac.dir_x = 0
        server.isaac.dir_y = 0
        server.isaac.x = 720
        game_framework.push_state(stage4_state)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            server.isaac.handle_event(event)

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
    game_world.remove_object(server.monster1)
    game_world.remove_object(server.block1)

def resume():
    game_world.add_object(server.isaac, 1)
    game_world.add_object(server.life, 1)
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




