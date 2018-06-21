from abc import ABCMeta, abstractmethod
import random
from environment import Environment


class GridMap(object):

    def __init__(self, as_leng, agent_pos_default, reward_pos_default, episode_size=1000):

        self.data = None
        self.ylen = -1
        self.xlen = -1

        self.agent_pos_default = agent_pos_default
        self.agent_pos = self.agent_pos_default
        self.reward_pos_default = reward_pos_default
        self.reward_pos = self.reward_pos_default


        self.episode_size = episode_size
        self.episode_counter = 0
        
        # Action is the destination to move
        if as_leng == 4:
            self.action_list = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        else:
            raise ValueError("as_leng should be set 4")

        self.is_reward = False
        self.map_type = 0
        
    def step(self, action):

        self.episode_counter += 1
        
        """ Wss it rewarding place? """
        if self.is_reward:
            self.reward_pos = self.reward_pos_update()
            
        agent_pos_tmp = [x + y for (x, y)
                         in zip(self.agent_pos, self.action_list[action])]

        self.map_type, self.is_reward = self.check(agent_pos_tmp)

        # observation = self.data
        observation = self.agent_pos
        
        reward = 1. if self.is_reward else 0.
        if self.episode_counter % self.episode_size == 0:
            done = True
        else:
            done = False
        info = None

        """ Is it wall? """
        if self.map_type == 1:
            return (observation, reward, done, info)

        self.agent_pos = agent_pos_tmp
        observation = self.agent_pos
        
        return (observation, reward, done, info)
    
    def set(self, map_data, ylen, xlen, reward_pos_update):

        if len(map_data) != (ylen * xlen):
            print ("ERROR: len(map) != (ylen * xlen)")
            return
            
        self.data = map_data
        self.ylen = ylen
        self.xlen = xlen
        self.reward_pos_update = reward_pos_update

    def check(self, agent_pos):
        agent_i = agent_pos[1] * self.xlen + agent_pos[0]
        map_type = self.data[agent_i]
        reward_i = self.reward_pos[1] * self.xlen + self.reward_pos[0]
        is_reward = (reward_i == agent_i)
        return map_type, is_reward

    
class GridWorldEnv(Environment):

    __metaclass__ = ABCMeta

    class ActionSpace(object):

        def __init__(self, as_leng):
            print ("GridWorldEnv class > ActionSpace")            
            self.as_list = range(as_leng)

        def sample(self):
            return random.choice(self.as_list)

    def __init__(self, as_leng, agent_pos_default, reward_pos_default,
                 renderer=None):

        super(GridWorldEnv, self).__init__(renderer=renderer, as_leng=4)
        
        self.action_space = self.ActionSpace(self.as_leng)
        self.map = GridMap(as_leng, agent_pos_default, reward_pos_default)
            
    def step(self, action):
        """
        INPUT: action
        OUTPUT: (observation, reward, done, info)
        """
        
        res = self.map.step(action)
        self.reward_pos = self.map.reward_pos
        self.agent_pos = self.map.agent_pos
        return res

    def render(self):
        
        if self.renderer is not None:
            self.renderer(self.map)

    def reset(self):
        self.agent_pos = self.map.agent_pos_default
        self.reward_pos = self.map.reward_pos_default
        return self.map.agent_pos_default
