import sys, pygame


class GridRenderer(object):

    def __init__(self, width=320, height=256, grid_size=32):

        pygame.init()

        window_size = (width, height)
        bg_color = (0, 0, 255)
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(window_size)

        self.grid_size = grid_size
        self.end_game = False        
        
        agent_img_path='../renderers/agent.png'
        reward_path='../renderers/cheese.png'
        chip_path='../renderers/chip.png'
        self.img_agent = pygame.image.load(agent_img_path)
        self.img_agent = pygame.transform.smoothscale(self.img_agent,
                                                    (grid_size, grid_size))
        self.img_reward = pygame.image.load(reward_path)
        self.img_reward = pygame.transform.smoothscale(self.img_reward,
                                                    (grid_size, grid_size))
        self.img_bg = pygame.image.load(chip_path)
        self.num_chips_per_line = int(self.img_bg.get_width() / self.grid_size)
        
    def __call__(self, map):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end_game = True

        """ render map """
        for y in range(0, map.ylen):
            for x in range(0, map.xlen):
                i = y * map.xlen + x
                c = map.data[i]
                dx = c % self.num_chips_per_line
                dy = int(c / self.num_chips_per_line)
                self.screen.blit(self.img_bg,
                         (x * self.grid_size, y * self.grid_size),
                         (self.grid_size * dx, self.grid_size * dy,
                          self.grid_size, self.grid_size))                
                
        """ render reward """
        self.render_item(map.reward_pos[0], map.reward_pos[1], self.img_reward)

        """ render agent """
        self.render_item(map.agent_pos[0], map.agent_pos[1], self.img_agent)

        pygame.display.flip()

        if self.end_game:
            sys.exit(0)
        
    def render_item(self, x, y, item):
        self.screen.blit(item,(x * self.grid_size, y * self.grid_size),
                         (0, 0, self.grid_size, self.grid_size))
            

