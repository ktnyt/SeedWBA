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

        time.sleep(0.1)

if __name__ == "__main__":
    # Initializing threads
    exe = concurrent.futures.ThreadPoolExecutor(max_workers=10)
    
    # Making action instances for each files in modules/actions
    actions_obj = []
    actions = {}
    for f in glob.glob(os.path.join("fr/modules/actions", "*.py")):
        # Loading each files as module
        classname = os.path.splitext(os.path.basename(f))[0]
        m = importlib.import_module("fr.modules.actions.{}".format(classname))
        # Loading classes written in files
        actions_obj += [c for c in inspect.getmembers(m, inspect.isclass) if c[0] == my_capitalize(classname)]
    
    for o in actions_obj:
        if o[0] != 'Action': actions[o[0]] = o[1]

    print("Loaded actions: " + str(actions))

    # Making action instances for each files in modules/analyzers
    analyzers_obj = []
    analyzers = {}
    for f in glob.glob(os.path.join("fr/modules/analyzers", "*.py")):
        # Loading each files as module
        classname = os.path.splitext(os.path.basename(f))[0]
        m = importlib.import_module("fr.modules.analyzers.{}".format(classname))
        # Loading classes written in files
        analyzers_obj += [c for c in inspect.getmembers(m, inspect.isclass) if c[0] == my_capitalize(classname)]
    
    for o in analyzers_obj:
        if o[0] != 'Analyzer': analyzers[o[0]] = o[1]

    print("Loaded analyzers: " + str(actions))

    # Initializing environments
    env = minidora.MinidoraEnv('0.0.0.0', 'minidora-v0-yayoi.local')
    architecture = SeedWBA()
 
    nsteps = 500000
    act = BASE_ACTION
    act["armright"] = 0.5
    act["armright"] = 0.5
    for _ in range(nsteps):
        observation, reward, done, info = env.step(act)
        act = actions["SearchFaces"].update('')
        print("Detected faces: {}".format(analyzers["IsFaceExist"].analyze('', observation)))
        time.sleep(1.0)
    
    exe.submit(update, actions)
