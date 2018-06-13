import random
from noh import Architecture, Component, Sensor, Actuator


class HippocampalFormation(Architecture):
    def __init__(self):
        super(HippocampalFormation, self).__init__(
            dict(
                ec=Sensor(),
                ca3=Component(),
                ca1=Component(),
            ), [
                (("ec"), 'ca3'),
                (("ec", 'ca3'), 'ca1'),
                ('ca1', 'ec'),
            ])


class SNr_GP(Actuator):
    def __init__(self):
        super(SNr_GP, self).__init__()
        
    def output(self):
        return random.choice(list(self.buffer.values()))        


class BasalGanglia(Architecture):
    def __init__(self):
        super(BasalGanglia, self).__init__(
            dict(
                dstr=Sensor(),
                mstr=Sensor(),                
                snr_gp=SNr_GP(),
            ), [
                (("dstr", 'mstr'), 'snr_gp'),
            ])

class MA(Actuator):
    def __init__(self):
        super(MA, self).__init__()

    def output(self):
        return random.choice(list(self.buffer.values()))

    
class SeedWBA(Architecture):
    def __init__(self):
        super(SeedWBA, self).__init__(
            dict(
                sa=Sensor(),
                hip=HippocampalFormation(),
                amg=Component(),
                rsc=Component(),
                ppc=Component(),
                bg=BasalGanglia(),
                thalamus=Component(),
                pfc=Component(),
                ma=MA(),
            ), [
                (('hip', 'sa', 'amg'), 'bg'),
                (('amg', 'sa'), 'hip'),
                ('hip', 'amg'),
                ('hip', 'rsc'),
                ('rsc', 'ppc'),
                ('bg', 'thalamus'),
                (('thalamus', 'ppc'), 'pfc'),
                ("pfc", "ma"),
            ])
