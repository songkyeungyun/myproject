from pico2d import *
import game_framework
from Stage import stage0_state

image = None

def enter():
    global image
    image = load_image('a.png')

# 게임 종료 - 객체를 소멸
def exit():
    global image
    del image

# 게임 월드 객체를 업데이트 - 게임 로직
def update():
    pass

    # 게임 월드 렌더링
def draw():
    clear_canvas()
    #play_state.draw_world()
    image.draw(400, 300)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_ESCAPE:
                    stage0_state.isaac.item = None
                    game_framework.pop_state()
                case pico2d.SDLK_1:
                    stage0_state.isaac.item = 'tear'
                    game_framework.pop_state()

def test_self():
    import sys
    this_module = sys.modules['__main__']
    pico2d.open_canvas()
    game_framework.run(this_module)
    pico2d.close_canvas()


if __name__ == '__main__':
    test_self()

