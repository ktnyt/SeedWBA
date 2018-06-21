import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import numpy as np
from policy_gradient import PG

from environments import MizutaMazeAbstract
from renderers import AbstractRenderer

if __name__ == "__main__":

  renderer = AbstractRenderer()
  env = MizutaMazeAbstract(renderer)
  observation = env.reset()
  reward_sum = 0
  episode_number = 0
  running_reward = None


  pg = PG(D=10, H=20, O=5, batch_size=10, learning_rate=1e-2,
          gamma=0.3, decay_rate=0.99, resume=False)
  
  while True:

    env.render()

    x = pg.preprop(observation)
    aprob, h = pg.policy_forward(x)
    action = pg.select_action(aprob)
    observation, reward, done, info = env.step(action)
    reward_sum += reward
    pg.record_reward(reward)

    if done: # an episode finished
      episode_number += 1

      if reward_sum != 0:
        pg.calc_grad()

      # perform rmsprop parameter update every batch_size episodes
      if episode_number % pg.batch_size == 0:
        pg.update_params()

      running_reward = reward_sum if running_reward is None \
                       else running_reward * 0.99 + reward_sum * 0.01
      print ('ep %d:  episode reward total was %f. running mean: %f'
             % (episode_number, reward_sum, running_reward))
      
      if episode_number % 100 == 0:
        pg.save_model(filename="save.p")

      f = open("res.txt", "a")
      f.write(str(reward_sum) + "\n")
      f.close()

      reward_sum = 0
      observation = env.reset() # reset env


