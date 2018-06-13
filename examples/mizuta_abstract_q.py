import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from environments import MizutaMazeAbstract
from renderers import AbstractRenderer


import numpy as np
import random
import sys

# sample ref
# http://mnemstudio.org/path-finding-q-learning-tutorial.htm

# Initial Q-value
Q = np.zeros((5,5,5))

GAMMA = 0.8

class QLearning(object):
    def __init__(self):
        return
        
    def dumpQvalue(self):
        print (Q.astype(int)) # convert float to int for redability

    def runGreedy(self, start_state = 0, pstate=0):
        print ("===== START =====")
        state = start_state
        while state != GOAL_STATE:
            print ("p stat: %d current state: %d" % (pstate, state))
            possible_actions = self._getPossibleActionsFromState(state)
            
            # get best action which maximaizes Q-value(s, a)
            max_Q = 0
            best_action_candidates = []
            for a in possible_actions:            
                if Q[state][a] > max_Q:
                    best_action_candidates = [a,]
                    max_Q = Q[state][a]
                elif Q[state][a] == max_Q:
                    best_action_candidates.append(a)
            
            # get a best action from candidates randomly
            best_action = random.choice(best_action_candidates)
            print ("-> choose action: %d" % best_action)
            state = best_action # in this example, action value is same as next state
        print ("state is %d, GOAL!!" % state)



if __name__ == "__main__":

    renderer = AbstractRenderer()

    env = MizutaMazeAbstract(renderer)
    env.reset()

    QL = QLearning()
    
    # Q learning
    action = env.action_space.sample()
    observation = 0
    state = 0
    pstate = 0
    sum_reward = 0
    for _ in range(10000):
        print ("--- print ---")
        print ("state: ", state, )
        if random.random() < 0.5:
            action = env.action_space.sample()
            print ("action ", action)
        else:
            possible_actions = env.action_space.as_list
            action = np.argmax([Q[pstate][state][i] for i in (possible_actions)])
            print ("action* ", action)
            print ([Q[pstate][state][i] for i in (possible_actions)])
        
        # Update Q-value
        # Q(s,a) = r(s,a) + Gamma * max[Q(next_s, possible_actions)]
        observation, reward, done, info = env.step(action)
        next_state = observation

        sum_reward += reward
        print ("reward: ", reward)
        
        possible_actions = env.action_space.as_list

        print ([Q[state][next_state][i] for i in possible_actions])
        max_Q_next_s_a = max([Q[state][next_state][i] for i in (possible_actions)])

        Q[pstate, state, action] = reward + GAMMA * max_Q_next_s_a
        #print ("Q : ", Q)
        print (pstate, state, next_state)

        pstate = state
        state = next_state

        #env.render()

    #QL.dumpQvalue()
    for i in range(5):
        print (Q[i])

    print ("score : ", sum_reward)
