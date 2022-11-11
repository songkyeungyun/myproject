from pico2d import *
import game_framework
import Stage.stage4_state as stage4_state
import Stage.stage0_state as stage0_state
import game_world

from isaac import Isaac
from monster1 import Monster_1
from monster2 import Monster_2
from life import Life

isaac = None
stage = None
monster1 = None
monster2 = None
life = []

class Stage:
    def __init__(self):
        self.image = load_image('Image/stage3.png')

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
    global isaac, stage, monster1, monster2, life
    isaac = Isaac()
    stage = Stage()
    life = [Life() for i in range(3)]
    monster1 = Monster_1()
    monster2 = Monster_2()
    game_world.add_object(isaac, 1)
    game_world.add_object(monster1, 1)
    game_world.add_object(monster2, 1)
    game_world.add_objects(life, 1)

    game_world.add_collision_group(isaac, monster1, 'isaac:monster1')
    game_world.add_collision_group(isaac, monster2, 'isaac:monster2')

    pass

# 게임 종료 - 객체를 소멸
def exit():
    game_world.clear()

# 게임 월드 객체를 업데이트 - 게임 로직
def update():
    for game_object in game_world.all_objects():
        game_object.update()

    for a, b, group in game_world.all_collision_pairs():
        if collide(a, b):
            print('collision by', group)
            a.handle_collision(b, group)
            b.handle_collision(a, group)
    if isaac.y >= 430 and 380 <= isaac.x <= 420:
        isaac.dir_x = 0
        isaac.dir_y = 0
        game_framework.pop_state()
    elif isaac.x >= 730 and 245 <= isaac.y <= 285:
        isaac.dir_x = 0
        isaac.dir_y = 0
        isaac.x = 720
        game_framework.push_state(stage4_state)
    delay(0.02)


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




