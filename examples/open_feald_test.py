import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from environments import OpenFealdTest
from renderers import GridRenderer

if __name__ == "__main__":

    renderer = GridRenderer()

    env = OpenFealdTest(renderer)
    env.reset()

    for _ in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
