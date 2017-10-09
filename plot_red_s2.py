import sys
from scapy.all import rdpcap
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot

ARP_type = 2054

def dict_add(dic, key):
    if key in dic:
        dic[key] += 1
    else:
        dic[key] = 1

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
			dict_add(mensajes, (p.psrc, p.pdst))
			nodes.add(p.psrc)
			nodes.add(p.pdst)

# for ip in broadcast_src:
# 	for n in nodes:
# 		if ip != n:
# 			dict_add(mensajes, (ip, n))

G = nx.DiGraph()
G.add_nodes_from(nodes)
for ip1, ip2 in mensajes:
	G.add_edge(ip1, ip2, weight=mensajes[(ip1, ip2)])

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

write_dot(G,'graph.dot')