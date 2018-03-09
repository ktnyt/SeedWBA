from noh import Architecture

class SeedWBA(Architecture):
    def __init__(self):
        super(SeedWBA, self).__init__(['sa', 'amg', 'bg', 'hip', 'pfc'], [
            (('hip', 'sa'), 'bg'),
            (('amg', 'sa'), 'hip'),
            (('hip', 'bg'), 'pfc'),
            ('hip', 'amg'),
        ])
