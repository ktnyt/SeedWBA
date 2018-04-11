import random
from noh import Architecture, Component, Sensor, Actuator


class PFC(Actuator):
    def __init__(self):
        super(PFC, self).__init__()

    def output(self):
        return random.choice(list(self.buffer.values()))

    
class SeedWBA(Architecture):
    def __init__(self):
        super(SeedWBA, self).__init__(
            dict(
                sa=Sensor(),
                hip=Component(),
                amg=Component(),
                bg=Component(),
                pfc=PFC(),
            ), [
                (('hip', 'sa'), 'bg'),
                (('amg', 'sa'), 'hip'),
                ('hip', 'amg'),
                (('hip', 'bg'), 'pfc'),
            ])
