import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import time
import random

from environments import minidora

def main():
    env = minidora.MinidoraEnv('0.0.0.0', 'minidora-v0-mutsuki.local')
    env.step(0)

    for _ in range(10):
        l = random.random
        r = random.random

    env.close()

if __name__ == '__main__':
    main()
