from pico2d import *
import game_framework
import Stage.stage1_state as stage1_state
import Stage.stage2_state as stage2_state
import Stage.stage3_state as stage3_state
import game_world


from isaac import Isaac
from life import Life

isaac = None
stage = None
life = None

class Stage:
    def __init__(self):
        self.image = load_image('Image/stage0.png')
        self.bgm = load_music('music/stage.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

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
    global isaac, stage, life
    isaac = Isaac(400, 250)
    stage = Stage()
    life = Life()
    game_world.add_object(isaac, 1)
    game_world.add_object(life, 1)


# 게임 종료 - 객체를 소멸
def exit():
    game_world.clear()

# 게임 월드 객체를 업데이트 - 게임 로직
def update():
    for game_object in game_world.all_objects():
        game_object.update()
    if isaac.x <= 70 and 245 <= isaac.y <= 285:
        isaac.dir_x = 0
        isaac.dir_y = 0
        isaac.x =120
        game_framework.push_state(stage1_state)
    elif isaac.y >= 420 and 380 <= isaac.x <= 420:
        isaac.dir_x = 0
        isaac.dir_y = 0
        isaac.y = 380
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
    game_world.remove_object(isaac)
    pass

def resume():
    game_world.add_object(isaac, 1)
    game_world.add_object(life, 1)
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
    import os
    this_module = sys.modules['__main__']
    pico2d.open_canvas()
    os.chdir('..')
    game_framework.run(this_module)
    pico2d.close_canvas()


if __name__ == '__main__':
    test_self()