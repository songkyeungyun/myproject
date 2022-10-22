from pico2d import *
import game_framework
import Stage.stage1_state as stage1_state
import Stage.stage2_state as stage2_state
import Stage.stage3_state as stage3_state
import item_state

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

class Isaac:
    def __init__(self):
        self.x = 400
        self.y = 255
        self.frame = 0
        self.dir_x = 0
        self.dir_y = 0
        self.image = load_image('Image/animation.png')
        self.isaac_image = load_image('Image/isaac.png')
        self.head_image = load_image('Image/1png.png')
        self.head_1_image = load_image('Image/2.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir_x*5
        self.y += self.dir_y*5
        if self.x > 700:
            self.x = 700
        if 245 <= self.y <= 285:
            if self.x < 70:
                self.x = 70
        elif self.x < 100:
            self.x = 100
        if 380 <= self.x <= 420:
            if self.y < 80:
                self.y = 80
            elif self.y > 430:
                self.y = 430
        elif self.y < 100:
            self.y = 100
        elif self.y > 400:
            self.y = 400

    def draw(self):
        if self.dir_x == 1:
            self.image.clip_draw(self.frame * 49, 0, 45, 80, self.x, self.y)
            if tear.item == 'tear':
                self.head_1_image.draw(self.x-5, self.y-6)
        elif self.dir_x == -1:
            self.image.clip_composite_draw(self.frame * 50, 0, 45, 80, 3.141592, 'v', self.x, self.y, 45, 80)
            if tear.item == 'tear':
                self.head_image.draw(self.x, self.y - 23)
        elif self.dir_y == -1 or self.dir_y == 1:
            self.image.clip_draw(self.frame * 49, 90, 50, 80, self.x, self.y)
        elif self.dir_x == 0:
            self.isaac_image.draw(self.x, self.y-10)
            if tear.item == 'tear':
                self.head_image.draw(self.x+2, self.y - 25)

class Tear:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.tear_image = load_image('Image/tear.png')
        self.item = None
        self.speed = [0, 0]

    def update(self):
        if self.x > 700 or self.x < 100 or self.y > 400 or self.y < 100:
            self.item = None
            self.speed[0] = 0
            self.speed[1] = 0
        pass
    def draw(self):
        if self.item == 'tear':
            self.tear_image.draw(self.x, self.y)
        self.x += self.speed[0]
        self.y += self.speed[1]


class Monster_1():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.frame = 0
        self.dir = 1
        self.image = load_image('Image/monster2 animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 4
        self.x += self.dir*2
        if self.x > 400:
            self.dir = -1
            self.x = 400
        elif self.x < 100:
            self.dir = 1
            self.x = 100

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(self.frame * 33, 30, 25, 35, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 33, 30, 25, 35, self.x, self.y)

class Monster_2():
    def __init__(self):
        self.x = 700
        self.y = 350
        self.frame = 0
        self.dir = -1
        self.image = load_image('Image/monster1 animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 6
        self.x += self.dir*2
        if self.x > 700:
            self.dir = -1
            self.x = 700
        elif self.x < 400:
            self.dir = 1
            self.x = 400

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(self.frame * 30, 30, 25, 60, self.x, self.y)
        else:
            self.image.clip_draw(self.frame * 30, 30, 25, 60, self.x, self.y)


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