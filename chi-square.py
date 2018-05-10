import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, chi2_contingency
"""
We're doing chi square Goodness of Fit.

Our goal in this code is to see the difference of p-values when we have 
different sample sizes.

So remember that we need to have the basics of knowing how chi-squared test works.
"""
# contingency table
#        click       no click
#------------------------------
# ad A |   a            b
# ad B |   c            d
#
# chi^2 = (ad - bc)^2 (a + b + c + d) / [ (a + b)(c + d)(a + c)(b + d)]
# degrees of freedom = (#cols - 1) x (#rows - 1) = (2 - 1)(2 - 1) = 1

# Short example

# T = np.array([[36, 14], [30, 25]])
# c2 = np.linalg.det(T)**2 * T.sum() / ( T[0].sum()*T[1].sum()*T[:,0].sum()*T[:,1].sum() )
# p_value = 1 - chi2.cdf(x=c2, df=1)

# equivalent:
# (36-31.429)**2/31.429+(14-18.571)**2/18.571 + (30-34.571)**2/34.571 + (25-20.429)**2/20.429


class DataGenerator:
    """
    p1 and p2 means two different click rates.
    Each time DataGenerator(p1, p2).next() will generate an outcome of if 
    the customers clicks."""
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def next(self):
        click1 = 1 if (np.random.random() < self.p1) else 0
        click2 = 1 if (np.random.random() < self.p2) else 0
        return click1, click2


def get_p_value(T):  # T must be a contingency table
    # same as scipy.stats.chi2_contingency(T, correction=False)
    det = T[0,0]*T[1,1] - T[0,1]*T[1,0]
    c2 = float(det) / T[0].sum() * det / T[1].sum() * T.sum() / T[:,0].sum() / T[:,1].sum()
    p = 1 - chi2.cdf(x=c2, df=1)
    return p


def run_experiment(p1, p2, N):
    data = DataGenerator(p1, p2)
    p_values = np.empty(N)
    T = np.zeros((2, 2)).astype(np.float32)
    for i in range(N):
        c1, c2 = data.next()
        T[0,c1] += 1
        T[1,c2] += 1
    # ignore the first 10 values, because chi-square requires that there should be at least 5 samples in each column
        if i < 10:
            p_values[i] = None
        else:
            p_values[i] = get_p_value(T)
    plt.plot(p_values)
    plt.plot(np.ones(N)*0.05)  # set alpha = 0.05
    plt.show()

run_experiment(0.1, 0.11, 20000)  # We can run it several times

"""
Summary:
    We can see that if want to show there's a difference between ad A and ad B
    when one equals 0.1 and the other equals 0.11, we need to have a really 
    large sample size.
    
    In real world examples, it's a question for the company that is it worth to 
    collect so many data and is the difference of 0.11 and 0.1 really meaningful
    for the company?
"""
