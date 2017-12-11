import sys
import matplotlib.pyplot as plt
from scapy.all import rdpcap
from math import log
import numpy as np

colors = ['deeppink', 'red', 'darkorange', 'gold', 'yellowgreen', 'cornflowerblue', 'darkorchid']

# red 1
# destacados = ['10.251.21.236',
# '10.251.21.216',
# '0.0.0.0',
# '10.251.21.1',
# '10.251.21.213',
# '10.251.21.240',
# '10.251.21.209']

# red 2
# destacados = ['192.168.0.2',
# '192.168.0.1']

# red 3
destacados = ['192.168.250.1']

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

print(S2_dict)

x = list()
y_normal = list()
y_destacados = list()
entropia = 0
for s in S2_dict:
	x.append(s)
	probabilidad = S2_dict[s]/float(paquetes_S2)
	informacion = -log(probabilidad, 2)
	entropia += probabilidad*informacion
	if s in destacados:
		y_destacados.append([informacion, s])
	else:
		y_normal.append([informacion, s])
entropia_max = log(len(S2_dict), 2)

ind = np.arange(len(S2_dict))
fig, ax = plt.subplots()
# plt.bar(np.arange(len(y_destacados)), y_destacados)

for i in range(len(y_destacados)):
	plt.bar([x.index(y_destacados[i][1])], [y_destacados[i][0]], color=colors[destacados.index(y_destacados[i][1])])

for i in range(len(y_normal)):
	plt.bar([x.index(y_normal[i][1])], [y_normal[i][0]], color='black')

# plt.bar(np.arange(len(y_normal)) + len(y_destacados), y_normal)
plt.xticks(ind, x, rotation='vertical')
plt.axhline(y=entropia, color='g', linestyle='-', label='Entropía muestral')
plt.axhline(y=entropia_max, color='r', linestyle='-', label='Entropía máxima')
plt.ylabel('Información')
plt.xlabel('Símbolo')
plt.legend()
# plt.savefig('entropiaS2Red4.png', bbox_inches='tight', dpi=200)
plt.show()