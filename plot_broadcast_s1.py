import sys
import matplotlib.pyplot as plt
from scapy.all import rdpcap

broadcast_address = 'ff:ff:ff:ff:ff:ff'

packets = rdpcap(sys.argv[1])
broadcast = 0
unicast = 0
otros = 0
for p in packets:
	if 'dst' in p.fields:
		if p.dst == broadcast_address:
			broadcast += 1
		else:
			unicast += 1
	else:
		otros += 1

colors = ['palevioletred', 'mediumturquoise', 'gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

if otros > 0: 
	plt.pie([broadcast, unicast, otros], labels=['broadcast', 'unicast', 'otro'],
		autopct='%1.1f%%', shadow=True, startangle=140, colors=colors)
else:
	plt.pie([broadcast, unicast], labels=['broadcast', 'unicast'],
		autopct='%1.1f%%', shadow=True, startangle=140, colors=colors)

plt.axis('equal')
plt.savefig('broadcastRed1.png', bbox_inches='tight', dpi=200)
# plt.show()