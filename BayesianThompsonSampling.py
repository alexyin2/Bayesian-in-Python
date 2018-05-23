import matplotlib.pyplot as plt
import numpy as np


class Bandit(object):
    def __init__(self, p):
        self.p = p
        self.a = 1
        self.b = 1

    def pull(self):
        return np.random.random() < self.p

    def sample(self):  # Sampling from current beta distribution
        return np.random.beta(self.a, self.b)

    def update(self, x):
        self.a += x
        self.b += 1 - x


def run_experiment(p1, p2, p3, N):
    bandits = [Bandit(p1), Bandit(p2), Bandit(p3)]
    data = np.empty(N)  # Return a new array of given shape and type, without initializing entries. This is a liitle bit faster than create a new array of zeros

    for i in range(N):
        # thompson sampling
        j = np.argmax([b.sample() for b in bandits])  # Find the largest sample
        x = bandits[j].pull()
        bandits[j].update(x)
        # for the plot
        data[i] = x
    cumulative_average_ctr = np.cumsum(data) / (np.arange(N) + 1)  # Detailed explanations of np.cumsum will be in PS.
    # cumulative_average_ctr shows the click through rate in every time after we've added a new sample
    # plot moving average ctr
    plt.plot(cumulative_average_ctr)
    plt.plot(np.ones(N)*p1)
    plt.plot(np.ones(N)*p2)
    plt.plot(np.ones(N)*p3)
    plt.ylim((0,1))
    plt.xscale('log')
    plt.show()


run_experiment(0.2, 0.25, 0.3, 100000)

#PS.
#1. np.cumsum()
test = np.array([1, 1, 3, 4, 5])
np.cumsum(test) 
'''
Explanation:
    Notice that the first element is 1.
    than the second is the first element + second element in test
    Keep going on...
'''






