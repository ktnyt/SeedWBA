import sys, pygame


class AbstractRenderer(object):

    def __init__(self, width=320, height=320, grid_size=64):

        pygame.init()

        window_size = (width, height)
        bg_color = (0, 0, 255)
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(window_size)

        self.id2pos = None
        
        self.grid_size = grid_size
        self.end_game = False        
        
        agent_img_path='../renderers/agent.png'
        reward_path='../renderers/cheese.png'
        bg_img_path='../renderers/mizuta_maze_v0.png'

        self.img_agent = pygame.image.load(agent_img_path)
        self.img_agent = pygame.transform.smoothscale(self.img_agent,
                                                      (grid_size, grid_size))
        self.img_reward = pygame.image.load(reward_path)
        self.img_reward = pygame.transform.smoothscale(self.img_reward,
                                                       (grid_size, grid_size))
        self.img_bg = pygame.image.load(bg_img_path)
        self.rect_bg = self.img_bg.get_rect()
        
    def __call__(self, map):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end_game = True

        """ render map """
        self.screen.blit(self.img_bg, self.rect_bg)

        try:
            """ render reward """
            reward_pos = map.id2pos(map.reward_pos)
            self.render_item(reward_pos[0], reward_pos[1], self.img_reward)

            """ render agent """
            agent_pos = map.id2pos(map.agent_pos) 
            self.render_item(agent_pos[0], agent_pos[1], self.img_agent)
        except NotImplementedError:
            print("id2pos is not set")

        
        pygame.display.flip()

        if self.end_game:
            sys.exit(0)
        
    def render_item(self, x, y, item):
        self.screen.blit(item,(x-self.grid_size/2, y-self.grid_size/2),
                         (0, 0, self.grid_size, self.grid_size))
            


