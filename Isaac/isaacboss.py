from pico2d import *
import game_framework
import Stage.boss_stage as boss_stage

image = None
bgm = None
logo_time = 0.0


def enter():
    global image, bgm
    image = load_image('Image/isaac vs boss.png')
    bgm = load_music('music/boss stage.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()

# 게임 종료 - 객체를 소멸
def exit():
    global image
    bgm.stop()
    del image

# 게임 월드 객체를 업데이트 - 게임 로직
def update():
    global logo_time
    if logo_time > 2.0:
        logo_time = 0
        game_framework.change_state(boss_stage)
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


