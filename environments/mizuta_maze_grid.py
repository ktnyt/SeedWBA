from environments import GridWorldEnv


class MizutaMazeGrid(GridWorldEnv):

    ylen = 15
    xlen = 15
    
    def __init__(self, renderer=None, as_leng=4, agent_pos_default=[7,7],
                 reward_pos_default=[2,2]):
        super(MizutaMazeGrid, self).__init__(as_leng=as_leng,
                                            agent_pos_default=agent_pos_default,
                                            reward_pos_default=reward_pos_default,
                                            renderer=renderer)
        class RewardPosUpdate():
            def __init__(self):
                self.cycle = 4
                self.counter = -1
                self.table = [[12, 2], [2, 2], [12, 12], [2, 12]]
            def __call__(self):
                self.counter = (self.counter + 1) % self.cycle
                
                return self.table[self.counter]
        reward_pos_update = RewardPosUpdate()
        
        self.map.set([
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
                1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1,
                1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1,
                1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
                1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1,
                1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1,
                1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
                1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1            
        ], ylen=15, xlen=15, reward_pos_update=reward_pos_update)

        

        
        self.agent_pos_default = agent_pos_default
        self.agent_pos = self.agent_pos_default
        self.reward_pos_default = reward_pos_default
        self.reward_pos = self.reward_pos_default



