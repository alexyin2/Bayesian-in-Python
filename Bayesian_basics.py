import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

NUM_TRIALS = 2000
BANDIT_PROBABILITIES = [0.2, 0.5, 0.75]

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
        

def plot(bandits, trial):  # Plot the pdf of each bandit
    x = np.linspace(0, 1, 200)
    for b in bandits:  
        y = beta.pdf(x, b.a, b.b)  # Returns the pdf of x, given a and b
        plt.plot(x, y, label="real p: %.4f" % b.p)
    plt.title("Bandit distributions after %s trials" % trial)
    plt.legend()
    plt.show()


def experiment():
    bandits = [Bandit(p) for p in BANDIT_PROBABILITIES]
    sample_points = [5,10,20,50,100,200,500,1000,1500,1999]
    for i in range(NUM_TRIALS):
        # take a sample from each bandit
        bestb = None  # The bandit whose arm we eventually pull
        maxsample = -1  # Keep track of the max sample we've got
        allsamples = [] # let's collect these just to print for debugging
        for b in bandits:
            sample = b.sample()
            allsamples.append("%.4f" % sample)
            if sample > maxsample:
                maxsample = sample
                bestb = b
        if i in sample_points:
            print("current samples: %s" % allsamples)
            plot(bandits, i)

            # pull the arm for the bandit with the largest sample
        x = bestb.pull()

        # update the distribution for the bandit whose arm we just pulled
        bestb.update(x)


'''
I try my best to write down how it works in experiment()

We have three bandits with different probability which we don't know and would like to estimate it.
At the beginning, all three bandits seems same to us and our prior is they're all following uniform distribution.
So we will first randomly pick one to try.
Then we will update the information to the bandit we've pull.
As the number of trying increases, we will more likely to pull the bandit that has a higher probability to win.
So the bandit with highest probability to win will be pulled more and more times, making the estimation more precise.

This is the core of Bayesian, we don't need to spend our money to the bandits with lower probability to win.
'''


# Run the experiment
if __name__ == "__main__":
    experiment()

