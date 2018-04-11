import sys
import os
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

#from environments import MinidoraEnv
from environments import minidora
from architecture import SeedWBA
from noh import Circuit




def passthrough(arg):
    return arg


def random_action(_):
    larm = random.uniform(-1.0, 1.0)
    rarm = random.uniform(-1.0, 1.0)
    return [larm, rarm, 0.0, 0.0]


def main():
    print("minidora env set up...")
    env = minidora.MinidoraEnv('0.0.0.0', 'minidora-v0-mutsuki.local')
    print("ok")
    
    architecture = SeedWBA()
    main = Circuit(('sa', 'bg'), ('bg', 'pfc'))
    main.implement(
        sa=passthrough,
        bg=random_action,
        pfc=passthrough,
    )
    architecture.add_circuits(main=main)

    nsteps = 50
    action = [0.5, 0.5, 0.0, 0.0]
    for _ in range(nsteps):
        observation, reward, done, info = env.step(action)
        action = architecture.main(observation)
        print("acrion ",  action)


if __name__ == '__main__':
    main()
