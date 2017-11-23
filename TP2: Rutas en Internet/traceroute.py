from scapy.all import sr, IP, ICMP
import sys
from json import dumps
from math import sqrt
from scipy import stats

class Hop:
	ip = None
	avg_rtt = None
	ttl = None
	rtt_diff = None
	abs_dev = None
	salto = None

	def __init__(self, ttl, ip=None, avg_rtt=None):
		self.ttl = ttl
		self.ip = ip
		self.avg_rtt = avg_rtt
		self.salto = False if ip else None

def main():
	if len(sys.argv) != 4:
		print('Modo de uso: sudo python3 traceroute.py <direccion> <tamaño de rafaga> <maximo ttl>')
		return

	#Initialize Variables
	target_url = sys.argv[1]
	burst_size = int(sys.argv[2]) #50
	max_ttl = int(sys.argv[3]) #30
	echoReplyNotFound = True
	current_ttl = 1
		
	addresses = dict()	# used to check on every iteration the most common Ip adress
	final_data = list()	# used for data analysis

	while echoReplyNotFound and max_ttl > current_ttl:
		#Send packet	
		response, unans = sr(IP(dst=target_url, ttl=current_ttl)/ICMP()*burst_size, timeout=1, verbose=0)
	
		count = 0
		#Get RTT Average
		for sent, received in response:
			
			#Increase received addresses counter for this Ip
			if received.src in addresses:
				addresses[received.src][0] += received.time - sent.sent_time
				addresses[received.src][1] += 1
			else:
				addresses[received.src] = [received.time - sent.sent_time, 1]

			if addresses[received.src][1] > count:
				count = addresses[received.src][1]
				most_common_ip = received.src
			
			#Set flacg if echo-reply
			if(received.type == 0):
				echoReplyNotFound = False

		if count > 0:
			rtt_average = addresses[most_common_ip][0]/addresses[most_common_ip][1]
			final_data.append(Hop(current_ttl, most_common_ip, rtt_average))
		
		else:
			final_data.append(Hop(current_ttl))
		
		current_ttl += 1
		addresses.clear()

	#Calculate rtt diffs
	for i in range(len(final_data)-1, 0, -1):
		if final_data[i].avg_rtt is not None:
			j = i-1
			while final_data[j].avg_rtt is None and j > 0:
				j -= 1
			final_data[i].rtt_diff = final_data[i].avg_rtt - final_data[j].avg_rtt
	i = 0
	while final_data[i].ip is None and i < len(final_data):
		i += 1
	final_data[i].rtt_diff = final_data[i].avg_rtt

	common_hops = [d for d in final_data if (d.ip is not None and d.rtt_diff >= 0)]
	# 		datos a analizar con Cimbala
	other_hops = [d for d in final_data if d not in common_hops]	
	# 		(nulos, saltos intercontinentales y con diferencia nula)

	while len(common_hops) > 0:
		#Calculate mean
		sum_ = 0
		for hop in common_hops:
			sum_ += hop.rtt_diff
		mean = sum_ / len(common_hops)

		#Calculate std dev
		sum_ = 0
		for hop in common_hops:
			sum_ += (hop.rtt_diff - mean) ** 2
		Sdev = sqrt(sum_ / (len(common_hops) - 1))
		
		#Calculate absolute value of deviation for each rtt
		for hop in common_hops:
			hop.abs_dev = abs(hop.rtt_diff - mean)

		#Calculate tau
		ppf = stats.t.ppf(1-0.025, len(common_hops)-2)
		tau = ppf * (len(common_hops) - 1) / (sqrt(len(common_hops)) * sqrt(len(common_hops) - 2 + ppf ** 2))
		tauS = tau * Sdev

		common_hops.sort(key=lambda x: x.abs_dev)

		if common_hops[-1].abs_dev > tauS:
			common_hops[-1].salto = True
			other_hops.append(common_hops[-1])
			common_hops.pop()
		else:
			break

	hops = common_hops + other_hops

	hops.sort(key=lambda x: x.ttl)

	results = list()
	for h in hops:
		data_object = {
				"rtt": h.avg_rtt,
				"ip_address": h.ip,
				"salto_intercontinental": h.salto,
				"hop_num": h.ttl
			}
		results.append(data_object)

	print(dumps(results, indent=2, separators=(',', ': ')))

if __name__ == "__main__":
	main()
