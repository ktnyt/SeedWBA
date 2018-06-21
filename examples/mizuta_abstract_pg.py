import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import numpy as np
import _pickle as pickle

from environments import MizutaMazeAbstract
from renderers import AbstractRenderer

class PG(object):
  def __init__(self, resume=False):

    # hyperparameters
    self.H = 20 # number of hidden layer neurons
    self.batch_size = 10 # every how many episodes to do a param update?
    self.learning_rate = 1e-2
    self.gamma = 0.3 # discount factor for reward
    self.decay_rate = 0.99 # decay factor for RMSProp leaky sum of grad^2

    # model initialization
    self.D = 10
    self.O = 5

    if resume:
      self.model = pickle.load(open('save.p', 'rb'))
    else:
      self.model = {}
      # "Xavier" initialization
      self.model['W1'] = np.random.randn(self.H,self.D) / np.sqrt(self.D) 
      self.model['W2'] = np.random.randn(self.O,self.H) / np.sqrt(self.H)
    
    # update buffers that add up gradients over a batch
    self.grad_buffer = { k : np.zeros_like(v) for k,v in self.model.items() } 
    # rmsprop memory
    self.rmsprop_cache = { k : np.zeros_like(v) for k,v in self.model.items() } 

  def sigmoid(self, x):
    # sigmoid "squashing" function to interval [0,1]
    return 1.0 / (1.0 + np.exp(-x))

  def softmax(self, x):
    exp_x = np.exp(x)
    y = exp_x / np.sum(np.exp(x))
    return y
    
  def discount_rewards(self, r):
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r)
    running_add = 0
    for t in reversed(range(0, r.size)):
      running_add = running_add * self.gamma + r[t]
      discounted_r[t] = running_add
    return discounted_r

  def policy_forward(self, x):
    #print ("var : ", self.model['W1'], x)
    h = np.dot(self.model['W1'], x)
    h[h<0] = 0 # ReLU nonlinearity
    logp = np.dot(self.model['W2'], h)
    #p = self.sigmoid(logp)
    p = self.softmax(logp)
    return p, h # return probability of taking action 2, and hidden state

  def policy_backward(self, eph, epdlogp):
    """ backward pass. (eph is array of intermediate hidden states) """
    #dW2 = np.dot(eph.T, epdlogp).ravel()
    dW2 = np.dot(eph.T, epdlogp).T # ***** IS IT OK ??? ****
    #dh = np.outer(epdlogp, self.model['W2'])
    dh = np.dot(epdlogp, self.model['W2']) # ***** IS IT OK ??? ****
    dh[eph <= 0] = 0 # backpro prelu
    dW1 = np.dot(dh.T, epx)
    return {'W1':dW1, 'W2':dW2}
    
if __name__ == "__main__":

  renderer = AbstractRenderer()
  env = MizutaMazeAbstract(renderer)
  observation = env.reset()

  prev_x = 0
  xs,hs,dlogps,drs = [],[],[],[]
  running_reward = None
  reward_sum = 0
  episode_number = 0

  pg = PG()
  
  while True:

    #env.render()
      
    # preprocess the observation, set input to network to be difference image
    cur_x = observation
    x = [0] * 10
    x[cur_x] = 1
    x[5+prev_x] = 1
    prev_x = cur_x

    # forward the policy network and sample an action
    # from the returned probability
    aprob, h = pg.policy_forward(x)
    action = np.random.choice(range(len(aprob)), p=aprob)

    # record various intermediates (needed later for backprop)
    xs.append(x) # observation
    hs.append(h) # hidden state
    y = [0] * 5
    y[action] = 1
    # grad that encourages the action that was taken to be taken
    # (see http://cs231n.github.io/neural-networks-2/#losses if confused)
    dlogps.append(y - aprob) 

    # step the environment and get new measurements
    observation, reward, done, info = env.step(action)
    reward_sum += reward

    drs.append(reward) # record reward (has to be done after we call step() to get reward for previous action)

    if done: # an episode finished
    #if reward != 0: # an reward get
      episode_number += 1

      if reward_sum != 0:

          # stack together all inputs, hidden states, action gradients,
          # and rewards for this episode
          epx = np.vstack(xs)
          eph = np.vstack(hs)
          epdlogp = np.vstack(dlogps)
          epr = np.vstack(drs)
          xs,hs,dlogps,drs = [],[],[],[] # reset array memory

          # compute the discounted reward backwards through time
          discounted_epr = pg.discount_rewards(epr)
          # standardize the rewards to be unit normal
          # (helps control the gradient estimator variance)
          discounted_epr -= np.mean(discounted_epr)
          #print (epr)
          #print (discounted_epr)
          #print (reward_sum)
          discounted_epr /= np.std(discounted_epr)

          # modulate the gradient with advantage (PG magic happens right here.)
          epdlogp *= discounted_epr
          grad = pg.policy_backward(eph, epdlogp)

          k = "W1"
          pg.grad_buffer[k] += grad[k] # accumulate grad over batch
          k = "W2"

          pg.grad_buffer[k] += grad[k] # accumulate grad over batch

      
          for k in pg.model:
              pg.grad_buffer[k] += grad[k] # accumulate grad over batch

      # perform rmsprop parameter update every batch_size episodes
      if episode_number % pg.batch_size == 0:
        for k,v in pg.model.items():
          g = pg.grad_buffer[k] # gradient
          pg.rmsprop_cache[k] = pg.decay_rate * pg.rmsprop_cache[k] + \
                             (1 - pg.decay_rate) * g**2
          pg.model[k] += pg.learning_rate * g / (np.sqrt(pg.rmsprop_cache[k]) + 1e-5)
          pg.grad_buffer[k] = np.zeros_like(v) # reset batch gradient buffer

      # boring book-keeping
      running_reward = reward_sum if running_reward is None \
                       else running_reward * 0.99 + reward_sum * 0.01
      print ('resetting env. episode reward total was %f. running mean: %f'
             % (reward_sum, running_reward))
      if episode_number % 100 == 0: pickle.dump(pg.model, open('save.p', 'wb'))

      f = open("res.txt", "a")
      f.write(str(reward_sum) + "\n")
      f.close()

      reward_sum = 0
      observation = env.reset() # reset env

    if reward != 0: # Pong has either +1 or -1 reward exactly when game ends.
      print (('ep %d: game finished, reward: %f'
              % (episode_number, reward)) + \
             ('' if reward == -1 else ' !!!!!!!!'))


