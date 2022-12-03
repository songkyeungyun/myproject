import random
import math
import time
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
from laser import Laser
from boss_tear import BossTear
import game_world
import finish_state

import server

boss_tear = []
laser = None

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5


class Boss():
    def __init__(self):
        self.x, self.y = 400, 250
        self.dir = random.random() * 2 * math.pi  # random moving direction
        self.speed = 0
        self.time = 0
        self.timer1 = 0
        self.cur_time = 0
        self.timer = 1.0  # change direction every 1 sec when wandering
        self.wait_timer = 4.0
        self.frame = 0
        self.build_behavior_tree()
        self.image = load_image('Image/boss stop.png')
        self.life = 5
        self.k = 0
        self.do = True
        self.invincibility = False

        Boss.breath_sound = load_wav('music/boss breath.wav')
        Boss.breath_sound.set_volume(10)

        Boss.shoot_sound = load_wav('music/boss shoot.wav')
        Boss.shoot_sound.set_volume(10)




    def wait(self):
        self.speed = 0
        self.wait_timer -= game_framework.frame_time
        if self.wait_timer >= 2.0:
            self.image = load_image('Image/boss stand by.png')
            Boss.breath_sound.play()
        else:
            self.image = load_image('Image/boss attack.png')
            if self.do == True:
                self.k += 1
                if self.k % 3 == 0:
                    self.laser()
                else:
                    self.tear()
                self.do = False
            Boss.shoot_sound.play()
        if self.wait_timer <= 0:
            self.wait_timer = 4.0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def wander(self):
        self.do = True
        self.image = load_image('Image/boss stop.png')
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 2.0
            self.dir = random.random() * 2 * math.pi
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def build_behavior_tree(self):
        wander_node = LeafNode('wander', self.wander)
        wait_node = LeafNode('wait', self.wait)

        wander_wait_node = SequenceNode('wander and wait')
        wander_wait_node.add_children(wander_node, wait_node)

        self.bt = BehaviorTree(wander_wait_node)
        pass

    def laser(self):
        laser = Laser(400, self.y)
        laser.time = time.time()
        game_world.add_object(laser, 0)
        game_world.add_collision_group(laser, None, 'laser:red_isaac')

    def tear(self):
        if server.red_isaac.x > self.x:
            boss_tear = [BossTear(self.x, self.y, random.randrange(1, 5), random.randrange(-5, 5)) for i in range(10)]
        else:
            boss_tear = [BossTear(self.x, self.y,random.randrange(-5, -1), random.randrange(-5, 5)) for i in range(10)]
        game_world.add_objects(boss_tear, 1)

        game_world.add_collision_group(boss_tear, None, 'boss_tear:red_isaac')


    def update(self):
        self.bt.run()


        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(150, self.x, 650)
        self.y = clamp(150, self.y, 350)
        self.cur_time = time.time()
        self.timer1 = self.cur_time - self.time
        if self.life == 0:
            Boss.shoot_sound.stop()
            Boss.breath_sound.stop()




    def draw(self):
        if self.timer1 >= 0.1:
            self.image.draw(self.x, self.y)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 70, self.y - 70, self.x + 70, self.y + 50

    def handle_collision(self, other, group):
        self.time = time.time()
        if group == 'red_tear:boss':
            game_world.remove_object(server.blood[self.life -1])
            self.life -= 1
            if self.life == 0:
                game_world.remove_object(self)
                game_framework.change_state(finish_state)




