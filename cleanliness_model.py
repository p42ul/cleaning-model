from collections import namedtuple

from mesa import Agent, Model
from mesa.time import RandomActivation


RoommateConfig = namedtuple('RoommateConfig',
    ['cleanliness_tolerance',
    'dirtiness_added',
    'cleaning_added',
    'apartment',
    ]
)

class RoommateAgent(Agent):
    '''Agent with preferences about cleanliness.'''
    def __init__(self, unique_id, model, cfg):
        super().__init__(unique_id, model)
        self.cleanliness_tolerance = cfg.cleanliness_tolerance
        self.dirtiness_added = cfg.dirtiness_added
        self.cleaning_added = cfg.cleaning_added
        self.apartment = cfg.apartment

    def step(self):
        print(f'i am agent {self.unique_id}')
        if self.apartment.cleanliness < self.cleanliness_tolerance:
            print(f'the apartment is dirty ({self.apartment.cleanliness}) so i will clean it')
            self.apartment.cleanliness += self.cleaning_added
        self.apartment.cleanliness -= self.dirtiness_added
        print(f'the apartment is now at {self.apartment.cleanliness} cleanliness')


class RoommateModel(Model):
    '''A model with some number of agents.'''
    def __init__(self, num_agents, cfg):
        self.num_agents = num_agents
        self.schedule = RandomActivation(self)
        for i in range(self.num_agents):
            a = RoommateAgent(i, self, cfg)
            self.schedule.add(a)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

class Apartment:
    def __init__(self, cleanliness):
        self.cleanliness = cleanliness

def main():
    apartment = Apartment(1.0)
    cfg = RoommateConfig(0.75, 0.1, 0.1, apartment)
    num_steps = 10
    num_roommates = 3
    m = RoommateModel(num_roommates, cfg)
    for i in range(num_steps):
        m.step()
    print(f'apartment cleanliness with {num_roommates} roommates after {num_steps} steps: {apartment.cleanliness}')

if __name__ == '__main__':
    main()