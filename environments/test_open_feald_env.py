from environments import GridWorldEnv


class OpenFealdTest(GridWorldEnv):

    def __init__(self, renderer=None):
        super(OpenFealdTest, self).__init__(agent_pos_default=[6, 6],
                                            reward_pos_default=[3, 3],
                                            renderer=renderer)

        self.map.set([
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                1, 0, 0, 0, 2, 2, 0, 0, 0, 1,
                1, 0, 0, 0, 2, 2, 0, 0, 0, 1,
                1, 0, 0, 0, 2, 0, 0, 0, 3, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 3, 1,
                1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        ], ylen=8, xlen=10)

        self.agent_pos_default = [6, 6]
        self.agent_pos = self.agent_pos_default
        self.reward_pos_default = [3, 3]
        self.reward_pos = self.reward_pos_default

