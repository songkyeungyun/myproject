from pico2d import *
import game_framework
import Stage.stage4_state as stage4_state

import server
image = None
logo_time = 0.0

def enter():
    global image
    image = load_image('Image/pick_item.png')

# 게임 종료 - 객체를 소멸
def exit():
    global image
    del image

# 게임 월드 객체를 업데이트 - 게임 로직
def update():
    global logo_time
    if logo_time > 2.0:
        logo_time = 0
        game_framework.pop_state()
    logo_time += 0.01

    # 게임 월드 렌더링
def draw():
    clear_canvas()
    stage4_state.draw_world()
    image.draw(server.isaac.x, server.isaac.y-10)
    update_canvas()

def handle_events():
    events = get_events()


def test_self():
    import sys
    this_module = sys.modules['__main__']
    pico2d.open_canvas()
    game_framework.run(this_module)
    pico2d.close_canvas()


if __name__ == '__main__':
    test_self()


