import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from environments import MizutaMazeGrid
from renderers import GridRenderer
# from architecture import SeedWBA

def passthrough(arg):
    return arg

def get_id2act(action_space):
    def id2act(arg):
        return action_space.sample()


if __name__ == "__main__":

    grid_size = 32
    ylen = MizutaMazeGrid.ylen
    xlen = MizutaMazeGrid.xlen    
    renderer = GridRenderer(width=xlen*grid_size, height=ylen*grid_size,
                            grid_size=grid_size)

    env = MizutaMazeGrid(renderer)
    env.reset()

    id2act = get_id2act(env.action_space)

    
    # architecture = SeedWBA()
    # rl_act = architecture.create_circuit("rl_act", ("sa", "bg", "pfc"))
    # rl_act.implement(passthrough, id2act)
    
    for _ in range(10000):
        env.render()
        # action = architecture(sa=observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
