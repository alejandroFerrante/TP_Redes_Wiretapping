import sys
import matplotlib.pyplot as plt
from scapy.all import rdpcap
from math import log
import numpy as np

ARP_type = 2054

def dict_add(dic, key):
    if key in dic:
        dic[key] += 1
    else:
        dic[key] = 1

packets = rdpcap(sys.argv[1])
S2_dict = dict()
paquetes_S2 = 0
for pkt in packets:
    if 'type' in pkt.fields:
        if pkt.type == ARP_type and pkt.op == 1:
            dict_add(S2_dict, pkt.psrc)
            paquetes_S2 += 1

x = list()
y = list()
entropia = 0
for s in S2_dict:
	x.append(s)
	probabilidad = S2_dict[s]/float(paquetes_S2)
	informacion = -log(probabilidad, 2)
	entropia += probabilidad*informacion
	y.append(informacion)
entropia_max = log(len(S2_dict), 2)

ind = np.arange(len(S2_dict))
fig, ax = plt.subplots()
plt.bar(ind, y)
plt.xticks(ind, x, rotation='vertical')
plt.axhline(y=entropia, color='g', linestyle='-', label='Entropía muestral')
plt.axhline(y=entropia_max, color='r', linestyle='-', label='Entropía máxima')
plt.ylabel('Información')
plt.xlabel('Símbolo')
plt.legend()
plt.savefig('entropiaS2Red4.png', bbox_inches='tight', dpi=200)
# plt.show()