import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math
# Create a population
population = np.random.normal(30, 20, 10000)  # These parameters will be used to check if how well our bayesian model performs
plt.hist(population)
plt.title('Population')
plt.show()

# Sample 1000 data
sample1 = np.random.choice(population, 1000, replace=True)
plt.hist(sample1)
plt.title('Sample 1, 1000ppl')
plt.show()

# Bayesian
'''
P(H|D) = P(D|H) * P(H) / P(D)
Where P(H|D) is our prosterior
P(D|H) is our likelihood
P(H) is our prior
But unfortunately, it's not that easy when we're calculating prior distributions.
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


