import sys
import matplotlib.pyplot as plt
from types_dic import types_dic
from scapy.all import rdpcap
from math import log
import numpy as np

broadcast_address = 'ff:ff:ff:ff:ff:ff'

def dict_add(dic, key):
    if key in dic:
        dic[key] += 1
    else:
        dic[key] = 1

packets = rdpcap(sys.argv[1])
S1_dict = dict()

paquetes_S1 = 0
for pkt in packets:
    if 'type' in pkt.fields and 'dst' in pkt.fields:
        if pkt.dst == broadcast_address:
            dict_add(S1_dict, '<broadcast, ' + types_dic[str(hex(pkt.type))] +'>')
        else:
            dict_add(S1_dict, '<unicast, ' + types_dic[str(hex(pkt.type))] +'>')
        paquetes_S1 += 1

x = list()
y = list()
for s in S1_dict:
	x.append(s)
	probabilidad = S1_dict[s]/float(paquetes_S1)
	informacion = -log(probabilidad, 2)
	y.append(informacion)

ind = np.arange(len(S1_dict))
fig, ax = plt.subplots()
plt.bar(ind, y)
plt.xticks(ind, x, rotation=30)
plt.show()