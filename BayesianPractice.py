import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
# 1. Task 1 
# Just for warm up
# Create a Guassian distributed population
population = np.random.normal(30, 20, 10000)  # These parameters will be used to check if how well our bayesian model performs
plt.hist(population)
plt.title('Population')
plt.show()

# Bayesian
'''
P(H|D) = P(D|H) * P(H) / P(D)
Where P(H|D) is our prosterior
P(D|H) is our likelihood
P(H) is our prior
But unfortunately, it's not that easy when we're calculating prior distributions times likelihood.
So I'll just use the outcome found on wiki.
Notice that if prior is Gaussian distribution, then posterior is also Gaussian distribution.
Our prior has two parameters: mu and sigma_0
'''
class Bayesian:
    def prior(self, prior_mu, prior_sigma_0):
        self.mu = prior_mu
        self.sigma_0 = prior_sigma_0
    
    
    def predict(self, sample_size):
        n = sample_size
        sample = np.random.choice(population, n, replace=True)
        mean = sample.mean()
        sigma = sample.std()
        posterior_mean = (1 / ((1 / self.sigma_0 ** 2) + (n / sigma ** 2))) * ((self.mu / self.sigma_0 ** 2) + (n * mean / sigma ** 2))
        posterior_variance = 1 / ((1 / self.sigma_0 ** 2) + (n / sigma ** 2))
        posterior_std = math.sqrt(posterior_variance)
        x = np.linspace(0, 100, 1000)
        plt.plot(x, mlab.normpdf(x, posterior_mean, posterior_std))
        plt.title(f'{n} people')
        plt.xticks(np.linspace(0, 100, 11))
        plt.show()


if __name__ == '__main__':
    for i in [10, 100, 500, 1000]:
        test = Bayesian()
        test.prior(50, 10)
        test.predict(i)

# 2. Task 2 
# What if our population is a bimodel distribution but our prior is still gaussian?
# Create a bimodel Population
population = np.hstack((np.random.normal(20, 10, 10000), np.random.normal(50, 5, 5000)))
plt.hist(population)
plt.title('Population')
plt.show()
population.mean()

# Run Bayesian
if __name__ == '__main__':
    for i in [10, 100, 500, 1000]:
        test = Bayesian()
        test.prior(50, 10)
        test.predict(i)
'''
After doing this task, I've realized that if we're using Gaussian as a prior, 
then we're just focusing on estimating the mean of the population, 
so I guess the prior doesn't have such big effect on our prosterior, which is a good thing.

Because when the results are sensitive to the choice of prior, then it may be a 
message that the data are not that informative, which implies that we should get
more data or be careful about deciding our prior distribution.

But notice that there's a huge problem in the data.
In Gaussian distribution, there's no difference between mean and mode.
But in bimodel distribution, we have to make sure what is the target that we want?
Are we just concerning about the mean or do we like to estimate the two modes
of the population?
'''


# Task 3
# Estimating the modes from bimodel estimation
'''
This part is not finished yet, since I've search about some recent data and 
find out we may probably need to use MCMC, which I haven't totally understand it.

So I'll come back and finish this part later.
References: https://stats.stackexchange.com/questions/59237/applying-bayes-estimating-a-bimodal-distribution
'''










