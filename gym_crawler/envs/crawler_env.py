import configparser
import numpy as np

import gym
from gym import spaces, utils, logger
from gym.utils import seeding
from gym_crawler.server_comm.interact import Interact

class CrawlerEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):

        # Read in INI File
        logger.debug("Environment Setup...")
        config = configparser.ConfigParser()
        config.read('NetCrawler.ini')
        logger.debug("Read in INI file")

        # Start Server
        ssh_connection = Interact(config['Connect']['host'],
                                  config['Connect']['user'],
                                  config['Connect']['key_path'])
        logger.debug("Connected to Server")

        # Login
        auth = ssh_connection.auth(config['Logon']['user'], 
                                   config['Logon']['password'])
        if auth == False:
            logger.debug("Auth Failed")
            quit(1)
        logger.debug("Logged into NetHack")
        quit(0)

        # Set Options
        # ...

        # Start Game
        # ...       

        # OpenAI Specific
        self.action_space = spaces.Discrete(4)
        #self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        self.state = None
        self.steps_beyond_done = None
        
    def step(self, action):
        pass

        #self.state = output from the game
        #done = player is dead or timer

        #if not done:
        #    reward = game score
        #elif self.steps_beyond_done is None:
        #    self.steps_beyond_done = 0
        #    reward = game score
        #else:
        #    if self.steps_beyond_done == 0:
        #        logger.warn("Attempted to call step() after Done already happened")
        #    self.steps_beyond_done += 1
        #    reward = 0.0
        #return np.array(self.state), reward, done, {}       

    def reset(self):
        pass

        # Start a new Game
        #(1) exit_game -> EXIT_QUIT
        #(2) start a new game 

        #self.state = output from the game
        #self.steps_beyon_done = None
        #return np.array(self.state), reward, done, {} 
 
    def render(self, mode='human', close=False):
        pass
