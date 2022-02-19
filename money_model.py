import matplotlib.pyplot as plt

from mesa import Agent, Model
from mesa.time import RandomActivation

class MoneyAgent(Agent):
    '''Agent with fixed initial wealth.'''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        if self.wealth == 0:
            return
        other_agent = self.random.choice(self.model.schedule.agents)
        other_agent.wealth += 1
        self.wealth -= 1


class MoneyModel(Model):
    '''A model with some number of agents.'''

    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()


def main():
    m = MoneyModel(10)
    for i in range(10):
        m.step()
    agent_wealth = [a.wealth for a in m.schedule.agents]
    plt.hist(agent_wealth)

if __name__ == '__main__':
    main()