from scipy import stats
from math import sqrt

def tau(n):
	ppf = stats.t.ppf(1-0.025, n-2)
	return ppf * (n - 1) / (sqrt(n) * sqrt(n - 2 + ppf ** 2))

for i in range(3, 39):
	print(i, tau(i))