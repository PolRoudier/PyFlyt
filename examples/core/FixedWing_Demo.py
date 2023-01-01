"""Spawn a single fixed wing UAV on x=0, y=0, z=50, with 0 rpy."""
import numpy as np
import gymnasium
from PyFlyt.core import Aviary, loadOBJ, obj_collision, obj_visual

from pyPS4Controller.controller import Controller
from threading import Thread, Event

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)


    def on_R3_down(self, value):
        global cmds

        value = value / 32767

        cmds[0] = value
        return value

    def on_R3_up(self, value):
        global cmds

        value = value / 32767

        cmds[0] = value
        return value

    def on_R3_left(self, value):
        global cmds

        value = value / 32767

        cmds[1] = value
        return value

    def on_R3_right(self, value):
        global cmds

        value = value / 32767

        cmds[1] = value
        return value

    def on_L3_left(self, value):
        global cmds

        value = value / 32767

        cmds[2] = value
        return value

    def on_L3_right(self, value):
        global cmds

        value = value / 32767

        cmds[2] = value
        return value

    def on_R2_press(self, value):
        global cmds

        value = value / 32767

        cmds[3] = value
        return value

def readDS4():
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()
    
t = Thread(target=readDS4, args=())
t.start()

cmds = [0, 0, 0, 0]

# the starting position and orientations
start_pos = np.array([[0.0, 0.0, 10]])
start_orn = np.array([[0.0, 0.0, 0.0]])
start_vel = np.array([[0.0, 20.0, 0.0]])

# environment setup
env = Aviary(start_pos=start_pos, start_orn=start_orn, start_vel=start_vel, use_camera=True, use_gimbal=False, render=True)

# set to position control
env.set_mode(1)

# call this to register all new bodies for collision
env.register_all_new_bodies()

# load the visual and collision entities and load the duck
visualId = obj_visual(env, "duck.obj")
collisionId = obj_collision(env, "duck.obj")
loadOBJ(
    env,
    visualId=visualId,
    collisionId=collisionId,
    baseMass=1.0,
    basePosition=[0.0, 0.0, 2.0],
)


# simulate for 1000 steps (1000/120 ~= 8 seconds)
for i in range(10000):
    env.step()
    
