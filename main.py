from agent import Agent
from monitor import interact
import gym
import envs

if __name__ == '__main__':
    env = gym.make('CustomEnv-v0')
    agent = Agent()
    avg_rewards, best_avg_reward = interact(env, agent)
