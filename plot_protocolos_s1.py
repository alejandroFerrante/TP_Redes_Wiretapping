import sys
import matplotlib.pyplot as plt
from scapy.all import rdpcap
import pickle

def dict_add(dic, key):
    if key in dic:
        dic[key] += 1
    else:
        dic[key] = 1

def tipo(n):
    if str(n) in types:
        return types[str(n)]
    else:
        return str(hex(n))

types = pickle.load(open('tipos.p', 'rb'))

packets = rdpcap(sys.argv[1])
d = dict()

for pkt in packets:
	if 'type' in pkt.fields:
	        dict_add(d, tipo(pkt.type))

labels = list()
sizes = list()
for prot in d:
	labels.append(prot)
	sizes.append(d[prot])

colors = ['palevioletred', 'mediumturquoise', 'gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
 
# Plot
plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140, colors=colors)
 
plt.axis('equal')
plt.savefig('protocolos_s1.png', bbox_inches='tight', dpi=200)
# plt.show()