from abc import ABCMeta, abstractmethod
import random
from environment import Environment


class AbstractMap(object):

    def __init__(self, agent_pos_default, reward_pos_default):

        self.data = None
        self.field_size = -1

        self.agent_pos_default = agent_pos_default
        self.agent_pos = self.agent_pos_default
        self.reward_pos_default = reward_pos_default
        self.reward_pos = self.reward_pos_default

        # Action is the destination ID
        self.action_list = None # Desided by field_size
        self.effect_path_list = None
        
        self.is_reward = False
        self.map_type = 0

    def step(self, action):


        """ Wss it rewarding place? """
        if self.is_reward:
            self.reward_pos = self.reward_pos_update()
            
        is_success, self.is_reward = self.check(self.agent_pos,
                                                      self.action_list[action])

        #print (is_success, self.is_reward, self.agent_pos, self.action_list[action])
        
        observation = self.data
        reward = 1 if self.is_reward else 0
        done = None
        info = None

        """ Is it wall? """
        if not is_success:
            return (observation, reward, done, info)

        self.agent_pos = self.action_list[action]

        return (observation, reward, done, info)

    def set(self, map_data, effect_path_list,
            id2pos=None, reward_pos_update=None):

        self.data = map_data
        self.field_size = len(map_data)
        self.action_list = range(self.field_size)
        self.effect_path_list = effect_path_list
        if id2pos is not None:
            self.id2pos = id2pos
        if reward_pos_update is not None:
            self.reward_pos_update = reward_pos_update
        
    
    def check(self, cur_pos, tar_pos):
        """
        Note: Jadge dose the move is effective or not
        return is_success, is_reward
        """

        if self.effect_path_list[cur_pos][tar_pos] == 0:
            return False, False
        elif self.reward_pos == tar_pos:
            return True, True
        else:
            return True, False

    def id2pos(self, id):
        raise NotImplementedError()

    def reward_pos_update(self):
        return random.randint(0, self.field_size-1)

    
class AbstractEnv(Environment):

    __metaclass__ = ABCMeta

    class ActionSpace(object):

        def __init__(self, as_leng):
            print ("AbstractEnv class > ActionSpace")            
            self.as_list = range(as_leng)

        def sample(self):
            return random.choice(self.as_list)

    def __init__(self, as_leng, agent_pos_default,
                 reward_pos_default, renderer=None):

        super(AbstractEnv, self).__init__(renderer=renderer, as_leng=as_leng)
        
        self.action_space = self.ActionSpace(self.as_leng)
        self.map = AbstractMap(agent_pos_default, reward_pos_default)
            
    def step(self, action):
        """
        INPUT: action
        OUTPUT: (observation, reward, done, info)
        """
        
        res = self.map.step(action)
        return res

    def render(self):
        
        if self.renderer is not None:
            self.renderer(self.map)

    def reset(self):
        pass
