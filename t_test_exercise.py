import numpy as np
import pandas as pd
from scipy import stats

# We'll use the dataset 'advertisement_clicks.csv'
df = pd.read_csv('advertisement_clicks.csv')
A = df[df.iloc[:, 0] == 'A']
B = df[df.iloc[:, 0] == 'B']
mean_a = A.iloc[:, 1].mean()
mean_b = B.iloc[:, 1].mean()
var_a = A.iloc[:, 1].var(ddof=1)  # Normalized by N-1 by default. Here we just type it out to make it clearer.
var_b = B.iloc[:, 1].var(ddof=1)

# Calculate t statistic
N = 1000
t = (mean_a - mean_b) / np.sqrt(var_a / N + var_b / N)
df = 2 * N - 2

# Calculate p
p = stats.t.cdf(t, df=df)  # one-sided t test p-value, H1: mean_a < mean_b

t2, p2 = stats.ttest_ind(A.iloc[:, 1], B.iloc[:, 1], equal_var=False)  # two-sided t test 
