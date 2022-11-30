import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import game_world

import server

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 15.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Monster_1():
    def __init__(self):
        self.x, self.y = 0, 0
        self.dir = random.random() * 2 * math.pi  # random moving direction
        self.speed = 0
        self.timer = 1.0  # change direction every 1 sec when wandering
        self.wait_timer = 2.0
        self.frame = 0
        self.build_behavior_tree()
        self.image = load_image('Image/monster2 animation.png')
        self.life = 1
        self.chase = True

    def wait(self):
        self.speed = 0
        self.wait_timer -= game_framework.frame_time
        if self.wait_timer <= 0:
            self.wait_timer = 2.0
            return BehaviorTree.SUCCESS

    def find_player(self):
        distance2 = (server.isaac.x - self.x)**2 + (server.isaac.y - self.y)**2
        if distance2 <= (PIXEL_PER_METER*10)**2:
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL


    def move_to_player(self):
        if self.chase == True:
            self.speed = RUN_SPEED_PPS
            self.dir = math.atan2(server.isaac.y - self.y, server.isaac.x - self.x)
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        wait_node = LeafNode('wait', self.wait)
        find_player_node = LeafNode('find player', self.find_player)
        move_to_player_node = LeafNode('move to player', self.move_to_player)
        chase_node = SequenceNode('chase')
        chase_node.add_children(find_player_node, move_to_player_node)

        chase_wait_node = SelectorNode('chase or wander')
        chase_wait_node.add_children(chase_node, wait_node)

        self.bt = BehaviorTree(chase_wait_node)
        # fill here
        pass
    def update(self):
        self.bt.run()
        # fill here

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(100, self.x, 700)
        self.y = clamp(100, self.y, 400)
        if server.isaac.invincibility == False:
            self.chase = True

    def draw(self):
        if math.cos(self.dir) >= 0:
            self.image.clip_draw(int(self.frame) * 33, 30, 25, 35, self.x, self.y, 35, 35)
        else:
            self.image.clip_composite_draw(int(self.frame) * 33, 30, 25, 35, 3.141592, 'v', self.x, self.y, 35, 35)
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, other, group):
        if group == 'isaac:monster1':
            self.chase = False
        if group == 'tear:monster1':
            if self.life == 3:
                self.life = 2
            elif self.life == 2:
                self.life = 1
            elif self.life == 1:
                game_world.remove_object(self)
        if group == 'monster1:block1':
            self.y -= self.speed * math.sin(self.dir) * game_framework.frame_time