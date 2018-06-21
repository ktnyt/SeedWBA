import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import numpy as np
import _pickle as pickle

from environments import MizutaMazeAbstract
from renderers import AbstractRenderer

class PG(object):
  def __init__(self, D, H, O, batch_size=10, learning_rate=1e-2,
               gamma=0.3, decay_rate=0.99, resume=False, filename="save.p"):

    self.D = D
    self.H = H
    self.O = O
    self.batch_size = batch_size
    self.learning_rate = learning_rate
    self.gamma = gamma
    self.decay_rate = decay_rate
    self.epsilon = 0.

    self.prev_x = 0
    self.xs,self.hs,self.dlogps,self.drs = [],[],[],[]

    if resume:
      self.model = pickle.load(open(filename, 'rb'))
    else:
      self.model = {}
      self.model['W1'] = np.random.randn(self.H,self.D) / np.sqrt(self.D) 
      self.model['W2'] = np.random.randn(self.O,self.H) / np.sqrt(self.H)
    
    self.grad_buffer = { k : np.zeros_like(v) for k,v in self.model.items() } 
    self.rmsprop_cache = { k : np.zeros_like(v) for k,v in self.model.items() } 

  def sigmoid(self, x):
    return 1.0 / (1.0 + np.exp(-x))

  def softmax(self, x):
    exp_x = np.exp(x)
    y = exp_x / np.sum(np.exp(x))
    return y

  def preprop(self, observation):

    self.cur_x = observation      
    x = [0] * self.D
    x[self.cur_x] = 1
    x[5+self.prev_x] = 1
    self.prev_x = self.cur_x

    self.xs.append(x) # observation
    return x

  def record_x(self, x):
    self.xs.append(x) # observation

  def discount_rewards(self, r):
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r)
    running_add = 0
    for t in reversed(range(0, r.size)):
      running_add = running_add * self.gamma + r[t]
      discounted_r[t] = running_add
    return discounted_r

  def policy_forward(self, x):
    h = np.dot(self.model['W1'], x)
    h[h<0] = 0 # ReLU nonlinearity
    logp = np.dot(self.model['W2'], h)
    p = self.softmax(logp)

    self.hs.append(h)
    
    return p, h 

  def select_action(self, aprob):

    if np.random.random() < self.epsilon:
      action = np.random.choice(range(len(aprob)))
    else:
      action = np.random.choice(range(len(aprob)), p=aprob)
    y = [0] * self.O
    y[action] = 1
    self.dlogps.append(y - aprob)
    return action

  def record_reward(self, reward):
      self.drs.append(reward) 

  def policy_backward(self, eph, epdlogp):
    """ backward pass. (eph is array of intermediate hidden states) """
    dW2 = np.dot(eph.T, epdlogp).T
    dh = np.dot(epdlogp, self.model['W2'])
    dh[eph <= 0] = 0 # backpro prelu
    dW1 = np.dot(dh.T, self.epx)
    return {'W1':dW1, 'W2':dW2}
    
  def calc_grad(self):

      self.epx = np.vstack(self.xs)
      self.eph = np.vstack(self.hs)
      self.epdlogp = np.vstack(self.dlogps)
      epr = np.vstack(self.drs)
      self.xs,self.hs,self.dlogps,self.drs = [],[],[],[]

      discounted_epr = self.discount_rewards(epr)
      discounted_epr -= np.mean(discounted_epr)
      discounted_epr /= np.std(discounted_epr)
      
      self.epdlogp *= discounted_epr
      grad = self.policy_backward(self.eph, self.epdlogp)

      for k in self.model:
          self.grad_buffer[k] += grad[k] # accumulate grad over batch
          
  def update_params(self):
      # self.epsilon *= 0.9
      print (" ====== epsilon :", self.epsilon)
      for k,v in self.model.items():
          g = self.grad_buffer[k] # gradient
          self.rmsprop_cache[k] = self.decay_rate * self.rmsprop_cache[k] + \
                             (1 - self.decay_rate) * g**2
          self.model[k] += self.learning_rate * g / \
                           (np.sqrt(self.rmsprop_cache[k]) + 1e-5)
          self.grad_buffer[k] = np.zeros_like(v) # reset batch gradient buffer

  def save_model(self, filename="save.p"):
      pickle.dump(self.model, open(filename, 'wb'))
