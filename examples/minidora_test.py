import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import time
import random

from environments import minidora


def main():
    env = minidora.MinidoraEnv('0.0.0.0', 'minidora-v0-mutsuki.local')
    env.step([0.5, 0.5, 0.0, 0.0])
    env.close()


if __name__ == '__main__':
    main()
