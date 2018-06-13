import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

from environments import MizutaMazeAbstract
from renderers import AbstractRenderer
#from architecture import SeedWBA
from kyoto_architecture import SeedWBA

INPUT = {
    "abstract_cue": [0, 0, 0, 0, 0]
    }

def passthrough(arg):
    return arg

def get_id2act(action_space):
    def id2act(arg):
        return action_space.sample()
    return id2act


if __name__ == "__main__":

    renderer = AbstractRenderer()

    env = MizutaMazeAbstract(renderer)
    env.reset()

    id2act = get_id2act(env.action_space)
    
    architecture = SeedWBA()
    
    rl_act = architecture.create_circuit("rl_act", ("sa", "bg", "thalamus", "pfc", "ma"))
    rl_act.implement(passthrough, id2act, passthrough, passthrough)

    # wm = architecture.create_circuit("wm", ("sa", "hip", "bg"))
    # hip_wm = architecture.hip.create_circuit("hip_wm", ("ec", "ca3", "ca1"))
    # wm.implement(passthrough, hip_wm)
    
    action = env.action_space.sample()
    observation = None
    for _ in range(1000):
        observation, reward, done, info = env.step(action)
        action = architecture(sa=observation)["ma"]
        env.render()
        # action = env.action_space.sample()

