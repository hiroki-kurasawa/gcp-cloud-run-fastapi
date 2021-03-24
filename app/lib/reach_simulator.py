import numpy as np

MEDIA_COEFFICIENT = {
    "Twitter": 6.000,
    "Youtube": 2.375,
    "Facebook": 5.755,
}


class ReachSimulator:
    def __init__(self, budget, media_name):
        self.budget = budget / 1_000_000
        self.media_name = media_name
        self.coefficient = MEDIA_COEFFICIENT[self.media_name]

    def unique_reach_function(self, x):
        return self.coefficient * np.log(x+1)

    def execute(self):
        simulated_reach = self.unique_reach_function(self.budget)
        return simulated_reach
