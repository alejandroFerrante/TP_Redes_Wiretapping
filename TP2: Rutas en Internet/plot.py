import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rcParams['text.latex.unicode']=True

data = [0.020071242984972502,
0.07424725488174794,
0.03699378086173016,
0.04346095479053,
0.02192910263935725,
0.06048880993051732,
0.1129073625082498,
0.17000439292506167,
0.2852083534322759,
0.49432093153397244,
0.42420270366053425,
0.9055390207391036,
0.6164713529023257,
0.37772628435721767,
0.35222768276295763,
0.4735599548920341]

for i in range(len(data)-1, 0, -1):
	data[i] -= data[i-1]

hops = [1] + list(range(6, 19)) + [22, 23]
for i in range(len(hops)):
	hops[i] -= 0.5

plt.scatter(hops, data, marker='.', s=150)
plt.xlabel("Salto")
plt.ylabel("RTT entre saltos")
plt.grid(True)
plt.xticks(np.arange(min(hops)-0.5, max(hops)+1.5, 1.0))
plt.savefig('tokyo1.png', bbox_inches='tight', dpi=200)
# plt.show()

plt.clf()

mean = sum(data)/len(data)
sum_ = 0
for d in data:
	sum_ += (d - mean) ** 2
Sdev = sqrt(sum_ / (len(data)-1))

data2 = list()

for d in data:
	data2.append((d - mean) / Sdev)

plt.scatter(data, data2, marker='.', s=150, color='darkorange')
plt.xlabel("RTT entre saltos")
plt.ylabel("$(X_i - \overline{X})/S$")
plt.grid(True)
plt.savefig('tokyo2.png', bbox_inches='tight', dpi=200)
# plt.show()