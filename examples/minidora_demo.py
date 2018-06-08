import sys
import os
import random
from time import sleep

path = os.path.dirname(os.path.join(os.path.abspath(__file__), '..'))
sys.path.append(path)

from environments import minidora
from architecture import SeedWBA

BASE_ACTION = {
    "armleft": 0.0,
    "armright": 0.0,
    "headroll": 0.0,
    "headpitch": 0.0,
    "headyaw": 0.0,
    "wheelleft": 0.0,
    "wheelright": 0.0
}

def passthrough(arg):
    return arg


def random_action_r(_):
    act = BASE_ACTION
    act["armright"] = random.uniform(-1.0, 1.0)
    return act


def random_action_l(_):
    act = BASE_ACTION
    act["armleft"] = random.uniform(-1.0, 1.0)
    return act


def random_action_d(_):
    act = BASE_ACTION
    act["armright"] = random.uniform(-1.0, 1.0)
    act["armright"] = random.uniform(-1.0, 1.0)
    return act


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
    action = BASE_ACTION
    action["armright"] = 0.5
    action["armright"] = 0.5
    for _ in range(nsteps):
        observation, _, _, _ = env.step(action)
        action = architecture(sa=observation)
        print("action ",  action)
        sleep(0.1)
        
        

if __name__ == '__main__':
    main()
