import numpy as np
from scipy import stats

N = 10
a = np.random.randn(N) + 2
b = np.random.randn(N)

# Calculate variance of a
# In default a.var() uses n as the denominator, but here we want to use n-1 
var_a = a.var(ddof=1)
var_b = b.var(ddof=1)

# Calculate pooled standard deviation
s = np.sqrt((var_a + var_b) / 2)

# Calculate t statistic
t = (a.mean() - b.mean()) / (s * np.sqrt(2 / N))
df = 2 * N - 2

# Calculate p
p = 1 - stats.t.cdf(t, df=df)  # one-sided test p-value
print('t: \t', t, 'p: \t', 2 * p)  # two-sided test p-value

# Use package in scipy to calculate t
t2, p2 = stats.ttest_ind(a, b)
print('t2: \t', t2, 'p2: \t', p2)
