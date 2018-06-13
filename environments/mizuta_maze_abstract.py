from environments import AbstractEnv


class MizutaMazeAbstract(AbstractEnv):

    def __init__(self, renderer=None):
        super(MizutaMazeAbstract, self).__init__(as_leng=5,
                                            agent_pos_default=0,
                                            reward_pos_default=0,
                                            renderer=renderer)

        self.map_state = [0, 0, 0, 0, 0]
        # effect_path_list[CURRENT_POSITION][TARGET_POS]
        self.effect_path_list = [[1, 1, 1, 1, 1],
                                 [1, 1, 0, 0, 0],
                                 [1, 0, 1, 0, 0],
                                 [1, 0, 0, 1, 0],
                                 [1, 0, 0, 0, 1]]


        class ID2Pos():
            def __init__(self):
                self.table = [[160, 160],
                              [80, 80],
                              [200, 80],
                              [80, 200],
                              [200, 200]]
            def __call__(self, id):
                return self.table[id]
        id2pos = ID2Pos()
            
        class RewardPosUpdate():
            def __init__(self):
                self.cycle = 4
                self.counter = -1
                self.table = [2, 3, 4, 1]
            def __call__(self):
                self.counter = (self.counter + 1) % self.cycle
                
                return self.table[self.counter]
        reward_pos_update = RewardPosUpdate()
            
        self.map.set(self.map_state, self.effect_path_list,
                     id2pos, reward_pos_update)



