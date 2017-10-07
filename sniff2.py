import sys
from scapy.all import conf, sniff
from scapy.utils import PcapWriter
from datetime import datetime

if len(sys.argv) == 3:
	conf.sniff_promisc = 1
	nombre = 'sniff_{}_{}.pcap'.format(sys.argv[1], datetime.now().strftime("%Y%m%d-%H%M%S"))
	dump = PcapWriter(nombre, append=True, sync=True)
	count = int(sys.argv[2])
	while count >= 100:
		paquetes = sniff(count=100, store=1)
		dump.write(paquetes)
		count -= 100
		print(str(int(sys.argv[2]) - count) + ' tramas...')
	if count > 0:
		paquetes = sniff(count=count, store=1)
		dump.write(paquetes)
		print(sys.argv[2] + ' tramas...')
else:
	print("uso: sudo python3 sniff2.py <nombre de red> <# tramas>")