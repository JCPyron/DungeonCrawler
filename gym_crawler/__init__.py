from gym.envs.registration import register

register(
    id='Crawler-v0',
    entry_point='gym_crawler.envs:CrawlerEnv',
)
