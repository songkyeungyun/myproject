from pico2d import *
import game_framework
import title_state

image = None
logo_time = 0.0

def enter():
    global image
    image = load_image('Image/load.png')

# 게임 종료 - 객체를 소멸
def exit():
    global image
    del image

# 게임 월드 객체를 업데이트 - 게임 로직
def update():
    global logo_time
    if logo_time > 1.0:
        logo_time = 0
        game_framework.change_state(title_state)
    delay(0.01)
    logo_time += 0.01

    # 게임 월드 렌더링
def draw():
    clear_canvas()
    image.draw(400, 300)
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


