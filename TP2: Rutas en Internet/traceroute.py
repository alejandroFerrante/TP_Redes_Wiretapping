from scapy.all import *
# from collections import Counter
import sys
import json
import math
from scipy import stats

def main():
	#Initialize Variables
	target_url = sys.argv[1]
	dump_file = open(sys.argv[2], 'w')
	burst_size = int(sys.argv[3]) #50
	max_ttl = int(sys.argv[4]) #30
	echoReplyNotFound = True
	current_ttl = 1
	
	rtt_counter = 0
	rtt_acum    = 0
	rtt_average = 0
	
	
	global_rtt_counter = 0
	global_rtt_acum    = 0
	global_rtt_average = 0
	global_standard_deviation = 0
	global_rtt_samples = []
	global_null_packets_amount = 0.0
	global_total_packets_amount = 0.0
	
	standard_values = []
	
	# adresses = Counter() #used to check on every iteration the most common Ip adress
	addresses = dict()
	final_data = list()
	
	result_per_ttl = []

	while echoReplyNotFound and max_ttl > current_ttl:
		#Send packet	
		response, unans = sr( IP(dst=target_url,ttl=current_ttl)/ICMP()*burst_size, timeout = 1, verbose = 0)
	
		count = 0
		#Get RTT Average
		for (sent, received) in response:
			
			#Increase recieved adresses counter for this Ip
			# adresses[received.src] += 1
			if received.src in addresses:
				addresses[received.src][0] += received.time - sent.sent_time
				addresses[received.src][1] += 1
			else:
				addresses[received.src][0] = received.time - sent.sent_time
				addresses[received.src][1] = 1

			if addresses[received.src][1] > count:
				count = addresses[received.src]
				most_common_ip = received.src
			
			#Increment RTT counter
			# rtt_acum += (received.time - sent.sent_time)
			# rtt_counter += 1
			
			#Set flacg if echo-reply
			if(received.type == 0):
				echoReplyNotFound = False
	
	
		# if rtt_counter > 0 :
		#   rtt_average = rtt_acum / rtt_counter

		if count > 0:
			rtt_average = addresses[most_common_ip][0]/addresses[most_common_ip][1]
			final_data.append([most_common_ip, rtt_average, current_ttl])
		
			# data_object = {
			# 	"rtt" : round(rtt_average , 6),
			# 	# "ip_address" : ' '+str(adresses.most_common(1)[0][0])+' ',
			# 	"ip_address" : ' '+str(most_common_ip[0][0])+' ',
			# 	"salto_intercontinental" : False,
			# 	"hop_num" : current_ttl

				
			# }
		
			global_rtt_acum    += rtt_average
			global_rtt_counter += 1
			# global_rtt_samples.append(rtt_average) 
		
		else:
			final_data.append([None, None, current_ttl])
			# data_object = {
			# 	"rtt" : None,
			# 	"ip_address" : None,
			# 	"salto_intercontinental" : None,
			# 	"hop_num" : current_ttl
			# }  
			global_null_packets_amount += 1
		
		
		global_total_packets_amount = global_total_packets_amount +1  
		# result_per_ttl.append(data_object)

		current_ttl += 1
		rtt_acum = 0
		rtt_counter = 0
		adresses.clear()

	#Calculate rtt diffs
	for i in range(len(final_data)-1, 0, -1):
		if final_data[i][1] is None:
			final_data[i].append(None)
		else:
			j = i-1
			while final_data[j][1] is None and j > 0:
				j -= 1
			final_data[i].append(final_data[i][1] - final_data[j][1])	# 3

	final_data.sort(lambda x, y: cmp(x[3], y[3]))

	#Calculate mean
	sum_ = 0
	count = 0
	for data in final_data:
		if data[2] is not None:
			sum_ += data[2]
			count += 1
	mean = sum_ / count

	#Calculate std dev
	sum_ = 0
	for data in final_data:
		if data[2] is not None:
			sum_ = (data[2] - mean) ** 2
	Sdev = math.sqrt(sum_ / (count - 1))
	
	#Calculate absolute value of deviation for each rtt
	for i in len(final_data):
		if final_data[i][2] is not None:
			final_data[i].append(math.abs(final_data[i][2] - mean))		# 4

		# z_value = ( rtt_sample - global_rtt_average ) / global_standard_deviation
		# standard_values.append(z_value)

	#Calculate tau
	ppf = stats.t.ppf(0.05, count-2)
	tau = ppf * (count - 1) / (math.sqrt(count) * math.sqrt(count - 2 + ppf ** 2))
	tauS = tau * Sdev

	
	
	#Write result in File
	#dump_file.write( json.dumps(result_per_ttl) )	
	dump_file.write( '[\n' )
	for json_value in result_per_ttl:
	  dump_file.write("%s\n" % json_value)
	dump_file.write( '\n]' )
	  
	dump_file.write(' \n \n Global Average: ')
	dump_file.write(str(repr(global_rtt_average)))
	dump_file.write(' \n Global Standard Deviation: ')
	dump_file.write(str(repr(global_standard_deviation)))
	dump_file.write(' \n Global Standard Values:\n')
	for z_value in standard_values:
	  dump_file.write("%s\n" % z_value)
	
	dump_file.write(' \n % null Packets:\n')
	dump_file.write(str( round(global_null_packets_amount / global_total_packets_amount , 2)))
	
	dump_file.close()

if __name__ == "__main__":
	main()
