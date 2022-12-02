from pico2d import *
import game_framework
from Stage import stage0_state

image = None
bgm = None

def enter():
    global image, bgm
    image = load_image('Image/title.png')
    bgm = load_music('music/start.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()



def exit():
    global image
    bgm.stop()
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(stage0_state)

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()

def update():
    handle_events()


def pause():
    pass

def resume():
    pass




