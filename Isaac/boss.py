import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import game_world

import server

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
        self.timer = 1.0  # change direction every 1 sec when wandering
        self.wait_timer = 1.0
        self.frame = 0
        self.build_behavior_tree()
        self.image = load_image('Image/boss stop.png')
        self.life = 2
        self.chase = True
        self.bgm = load_music('music/boss.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def wait(self):
        self.speed = 0
        self.wait_timer -= game_framework.frame_time
        if self.wait_timer <= 0:
            self.wait_timer = 1.0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def wander(self):
        self.speed = RUN_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
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
        # fill here
        pass
    def update(self):
        self.bt.run()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(100, self.x, 700)
        self.y = clamp(100, self.y, 400)

    def draw(self):
        if self.speed == 0:
            self.image.draw(self.x, self.y)
        else:
            self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 150, self.y - 100, self.x + 50, self.y + 40

    def handle_collision(self, other, group):
        pass