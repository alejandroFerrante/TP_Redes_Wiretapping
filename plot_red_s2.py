import sys
from scapy.all import rdpcap
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot

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

def dict_add_req(dic, key):
    if key in dic:
        dic[key][1] += 1
    else:
        dic[key] = [1, 0]
def dict_add_rep(dic, key):
	if key in dic:
		dic[key][0] += 1
	else:
		dic[key] = [0, 1]

# broadcast_src = dict()
mensajes = dict()
nodes = set()
packets = rdpcap(sys.argv[1])
for p in packets:
	if 'type' in p.fields:
		if p.type == ARP_type:
			# if p.op == 1:
			# 	# request ARP
			# 	dict_add(broadcast_src, p.psrc)
			# 	nodes.add(p.psrc)
			# elif p.op == 2:
			# 	# reply
			# 	dict_add(mensajes, (p.psrc, p.pdst))
			# 	nodes.add(p.psrc)
			# 	nodes.add(p.pdst)
			if p.op == 1:
				dict_add_req(mensajes, (p.psrc, p.pdst))
			elif p.op == 2:
				dict_add_rep(mensajes, (p.psrc, p.pdst))
			# dict_add(mensajes, (p.psrc, p.pdst))
			nodes.add(p.psrc)
			nodes.add(p.pdst)

# for ip in broadcast_src:
# 	for n in nodes:
# 		if ip != n:
# 			dict_add(mensajes, (ip, n))

G = nx.DiGraph()
# G.add_nodes_from(nodes)
for n in nodes:
	if n in destacados:
		G.add_node(n, color='red')
	else:
		G.add_node(n)
for ip1, ip2 in mensajes:
	if ip1 in destacados:
		if mensajes[(ip1, ip2)][0] > 0 or mensajes[(ip1, ip2)][1] > 0: 
			G.add_edge(ip1, ip2, label=str(mensajes[(ip1, ip2)][0]) + ' / ' + str(mensajes[(ip1, ip2)][1]) , color='red')
	else:
		if mensajes[(ip1, ip2)][0] > 0 or mensajes[(ip1, ip2)][1] > 0:
			G.add_edge(ip1, ip2, label=str(mensajes[(ip1, ip2)][0]) + ' / ' + str(mensajes[(ip1, ip2)][1]))

# A = nx.to_agraph(G)
# A.draw('test.png')
# nx.draw_networkx(G,pos=nx.shell_layout(G))
# print(mensajes)
# nx.draw_networkx_edge_labels(G,pos=nx.shell_layout(G))
# plt.show()



# nx.draw(G, pos=graphviz_layout(G), node_size=1600, cmap=plt.cm.Blues,
#         node_color=range(len(G)),
#         prog='dot')
# plt.show()

nx.draw_networkx_edge_labels(G,pos=nx.shell_layout(G))
write_dot(G,'graph.dot')
#### dot -Tpng -Kfdp graph.dot > graph.png