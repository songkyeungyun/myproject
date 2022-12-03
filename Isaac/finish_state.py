from pico2d import *
import game_framework

image = None
bgm = None

def enter():
    global image, bgm
    image = load_image('Image/finish.png')
    die_sound = load_wav('music/boss_die.wav')
    die_sound.set_volume(32)
    die_sound.play()

def exit():
    global image
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()

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




