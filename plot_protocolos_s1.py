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

x = list()
y = list()
for prot in d:
	x.append(prot)
	y.append(d[prot])

colors = ['palevioletred', 'mediumturquoise', 'gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
 
# Plot
# plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140, colors=colors)
 
# plt.legend()
# print(d)
# plt.savefig('protocolosRed1.png', bbox_inches='tight', dpi=200)
# plt.show()

porcent = [100.0*i/sum(y) for i in y]

patches, texts = plt.pie(y, colors=colors, shadow=True, startangle=140)
labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, porcent)]
plt.axis('equal')

sort_legend = True
if sort_legend:
    patches, labels, dummy =  zip(*sorted(zip(patches, labels, y),
                                          key=lambda x: x[2],
                                          reverse=True))

plt.legend(patches, labels, loc='center left', bbox_to_anchor=(-0.1, 1.),
           fontsize=8)
# plt.show()
plt.savefig('protocolosRed4.png', bbox_inches='tight', dpi=200)