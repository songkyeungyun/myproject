from pico2d import *
import game_framework
import Stage.stage1_state as stage1_state
import Stage.stage2_state as stage2_state
import Stage.stage3_state as stage3_state
import item_state


from isaac import Isaac
from tear import Tear
from monster1 import Monster_1
from monster2 import Monster_2
isaac = None
stage = None
monster1 = None
monster2 = None
tear = None
running = True
class Stage:
    def __init__(self):
        self.image = load_image('Image/stage0.png')

    def draw(self):
        self.image.draw(400, 300)


def handle_events():
    global running, isaac, tear
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_i:
                game_framework.push_state(item_state)
            if tear.item == None:
                if event.key == SDLK_w:
                    tear.x = isaac.x
                    tear.y = isaac.y
                    tear.speed[0] = 0
                    tear.speed[1] = 0
                    tear.item = 'tear'
                    tear.speed[1] = 10
                if event.key == SDLK_a:
                    tear.x = isaac.x
                    tear.y = isaac.y
                    tear.speed[0] = 0
                    tear.speed[1] = 0
                    tear.item = 'tear'
                    tear.speed[0] = -10
                if event.key == SDLK_s:
                    tear.x = isaac.x
                    tear.y = isaac.y
                    tear.speed[0] = 0
                    tear.speed[1] = 0
                    tear.item = 'tear'
                    tear.speed[1] = -10
                if event.key == SDLK_d:
                    tear.x = isaac.x
                    tear.y = isaac.y
                    tear.speed[0] = 0
                    tear.speed[1] = 0
                    tear.item = 'tear'
                    tear.speed[0] = 10
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                isaac.dir_x = 1
                isaac.x += isaac.dir_x
            if event.key == SDLK_LEFT:
                isaac.dir_x = -1
                isaac.x += isaac.dir_x
            if event.key == SDLK_UP:
                isaac.dir_y += 1
                isaac.y += isaac.dir_y
            if event.key == SDLK_DOWN:
                isaac.dir_y -= 1
                isaac.y += isaac.dir_y
            if event.key == SDLK_ESCAPE:
                running = False
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                isaac.dir_x = 0
            if event.key == SDLK_LEFT:
                isaac.dir_x = 0
            if event.key == SDLK_UP:
                isaac.dir_y = 0
            if event.key == SDLK_DOWN:
                isaac.dir_y = 0

def enter():
    global isaac, stage, running, monster1, monster2, tear
    isaac = Isaac()
    stage = Stage()
    monster1 = Monster_1()
    monster2 = Monster_2()
    tear = Tear()
    running = True
    pass

# 게임 종료 - 객체를 소멸
def exit():
    global isaac, stage, monster1, monster2, tear
    del isaac, stage, monster1, monster2, tear

# 게임 월드 객체를 업데이트 - 게임 로직
def update():
    global isaac, monster1, monster2, tear
    isaac.update()
    monster1.update()
    monster2.update()
    tear.update()
    if isaac.x <= 70 and 245 <= isaac.y <= 285:
        isaac.dir_x = 0
        isaac.dir_y = 0
        isaac.x = 120
        game_framework.push_state(stage1_state)
    elif isaac.y >= 430 and 380 <= isaac.x <= 420:
        isaac.dir_x = 0
        isaac.dir_y = 0
        isaac.y = 410
        game_framework.push_state(stage2_state)
    elif isaac.y <= 80 and 380 <= isaac.x <= 420:
        isaac.dir_x = 0
        isaac.dir_y = 0
        isaac.y = 120
        game_framework.push_state(stage3_state)
    delay(0.02)


def draw_world():
    stage.draw()
    isaac.draw()
    monster1.draw()
    monster2.draw()
    tear.draw()

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