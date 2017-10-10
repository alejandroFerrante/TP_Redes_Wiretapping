import sys
import matplotlib.pyplot as plt
import pickle
from scapy.all import rdpcap
from math import log
import numpy as np

broadcast_address = 'ff:ff:ff:ff:ff:ff'

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
S1_dict = dict()

paquetes_S1 = 0
for pkt in packets:
    if 'type' in pkt.fields and 'dst' in pkt.fields:
        if pkt.dst == broadcast_address:
            dict_add(S1_dict, 'broadcast\n' + tipo(pkt.type))
        else:
            dict_add(S1_dict, 'unicast\n' + tipo(pkt.type))
        paquetes_S1 += 1

x = list()
y = list()
entropia = 0
for s in S1_dict:
	x.append(s)
	probabilidad = S1_dict[s]/float(paquetes_S1)
	informacion = -log(probabilidad, 2)
	entropia += probabilidad*informacion
	y.append(informacion)
entropia_max = log(len(S1_dict), 2)
# print(entropia)

ind = np.arange(len(S1_dict))
fig, ax = plt.subplots()
plt.bar(ind, y)
# plt.xticks(ind, x, rotation=30)
plt.xticks(ind, x, rotation='vertical')
plt.axhline(y=entropia, color='g', linestyle='-', label='Entropía muestral')
plt.axhline(y=entropia_max, color='r', linestyle='-', label='Entropía máxima')
plt.ylabel('Información')
plt.xlabel('Símbolo')
plt.legend()
plt.savefig('entropiaS1Red4.png', bbox_inches='tight', dpi=200)
# plt.show()