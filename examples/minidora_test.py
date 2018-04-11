import sys
import os
import random
from time import sleep

sys.path.append(os.getcwd())

from environments import minidora
from architecture import SeedWBA


def passthrough(arg):
    return arg


def random_action_r(_):
    rarm = random.uniform(-1.0, 1.0)
    return [0.0, rarm, 0.0, 0.0]


def random_action_l(_):
    larm = random.uniform(-1.0, 1.0)
    return [larm, 0.0, 0.0, 0.0]


def random_action_d(_):
    arm = random.uniform(-1.0, 1.0)
    return [arm, arm, 0.0, 0.0]


class PFC(object):
    
    def __init__(self, call_circuits):
        self.call_circuits = call_circuits
        self.past_act = 0
        self.act_size = len(self.call_circuits)
        
    def __call__(self, arg):
        if random.random() < 0.05:
            self.past_act = (self.past_act + 1) % self.act_size
        return self.call_circuits[self.past_act](arg)

def main():
    env = minidora.MinidoraEnv('0.0.0.0', 'minidora-v0-mutsuki.local')
    
    architecture = SeedWBA()

    right_hand = architecture.create_circuit('right_hand', ('sa', 'bg', 'pfc'))
    left_hand = architecture.create_circuit('left_hand', ('sa', 'bg', 'pfc'))
    double_hand = architecture.create_circuit('double_hand', ('sa', 'bg', 'pfc'))

    right_hand.implement(passthrough, random_action_r)
    left_hand.implement(passthrough, random_action_l)
    double_hand.implement(passthrough, random_action_d)

    nsteps = 500000
    action = [0.5, 0.5, 0.0, 0.0]
    for _ in range(nsteps):
        observation, reward, done, info = env.step(action)
        action = architecture(sa=observation)['pfc']
        print("action:",  action)
        sleep(0.5)
        
        

if __name__ == '__main__':
    main()
