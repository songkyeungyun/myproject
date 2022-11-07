from pico2d import *
import game_framework
import Stage.stage1_state as stage1_state
import Stage.stage2_state as stage2_state
import Stage.stage3_state as stage3_state
import game_world


from isaac import Isaac
from monster1 import Monster_1
from monster2 import Monster_2

isaac = None
stage = None
monster1 = None
monster2 = None

class Stage:
    def __init__(self):
        self.image = load_image('Image/stage0.png')

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
    global isaac, stage, running, monster1, monster2
    isaac = Isaac()
    stage = Stage()
    monster1 = Monster_1()
    monster2 = Monster_2()
    game_world.add_object(isaac, 1)
    game_world.add_object(monster1, 1)
    game_world.add_object(monster2, 1)
    pass

# 게임 종료 - 객체를 소멸
def exit():
    global isaac, stage, monster1, monster2
    del isaac, stage, monster1, monster2

# 게임 월드 객체를 업데이트 - 게임 로직
def update():
    for game_object in game_world.all_objects():
        game_object.update()
    if isaac.x <= 70 and 245 <= isaac.y <= 285:
        isaac.dir_x = 0
        isaac.dir_y = 0
        isaac.x = 120
        game_framework.push_state(stage1_state)
    elif isaac.y >= 420 and 380 <= isaac.x <= 420:
        isaac.dir_x = 0
        isaac.dir_y = 0
        isaac.y = 400
        game_framework.push_state(stage2_state)
    elif isaac.y <= 80 and 380 <= isaac.x <= 420:
        isaac.dir_x = 0
        isaac.dir_y = 0
        isaac.y = 120
        game_framework.push_state(stage3_state)


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

def test_self():
    import sys
    import os
    this_module = sys.modules['__main__']
    pico2d.open_canvas()
    os.chdir('..')
    game_framework.run(this_module)
    pico2d.close_canvas()


if __name__ == '__main__':
    test_self()