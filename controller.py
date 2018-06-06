import sys
import time
import readchar
import concurrent.futures
import os
import inspect
import importlib
import glob

BASE_ACTION = {
    "armleft": 0.0,
    "armright": 0.0,
    "headroll": 0.0,
    "headpitch": 0.0,
    "headyaw": 0.0,
    "wheelleft": 0.0,
    "wheelright": 0.0
}

from environments import minidora
from architecture import SeedWBA

def my_capitalize(str):
    return (str[0]).upper() + str[1:]

def passthrough(arg):
    return arg

def update(actions):
    while(True):
        for action in actions:
            if(action.active):
                action.update()

        time.sleep(1.0 / 60.0)

if __name__ == "__main__":
    # Initializing threads
    exe = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    
    # Making action instances for each files in modules/actions
    actions_obj = []
    for f in glob.glob(os.path.join("modules/actions", "*.py")):
        # Loading each files as module
        classname = os.path.splitext(os.path.basename(f))[0]
        m = importlib.import_module("modules.actions.{}".format(classname))
        # Loading classes written in files
        actions_obj += [c for c in inspect.getmembers(m, inspect.isclass) if c[0] == my_capitalize(classname)]
    
    actions = [o for o in actions_obj if o[0] != 'Action']

    print("Loaded actions: " + actions)

    # Initializing environments
    env = minidora.MinidoraEnv('0.0.0.0', 'minidora-v0-yayoi.local')
    architecture = SeedWBA()

    for action in actions:
        newcircuit = architecture.create_circuit(action[0], ('sa', 'bg', 'pfc'))
        newcircuit.implement(passthrough, action[1].update())

    nsteps = 500000
    action = BASE_ACTION
    action["armright"] = 0.5
    action["armright"] = 0.5
    for _ in range(nsteps):
        observation, reward, done, info = env.step(action)
        action = architecture(sa=observation)
        print("action ",  action)
        time.sleep(1.0 / 60.0)
    
    exe.submit(update, actions)
