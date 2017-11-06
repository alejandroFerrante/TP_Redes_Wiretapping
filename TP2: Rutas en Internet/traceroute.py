from scapy.all import *
from collections import Counter
import sys
import json
import math

def main():
	#Initialize Variables
	target_url = sys.argv[1]
	burst_size = int(sys.argv[3]) #50
	max_ttl = int(sys.argv[4]) #30
	dump_file = open(sys.argv[2], 'w')
	echoReplyNotFound = True
	current_ttl = 1
	
	rtt_counter = 0
	rtt_acum    = 0
	rtt_average = 0
	
	
	global_rtt_counter = 0
	global_rtt_acum    = 0
	global_rtt_average = 0
	global_standard_deviation = 0
	global_standard_deviation_acum = 0
	global_rtt_samples = []
	global_null_packets_amount = 0.0
	global_total_packets_amount = 0.0
	
	standard_values = []
	
	adresses = Counter() #used to check on every iteration the most common Ip adress
	
	result_per_ttl = []
  #

	while echoReplyNotFound and max_ttl > current_ttl:
    
    #Send packet	
		response, unans = sr( IP(dst=target_url,ttl=current_ttl)/ICMP()*burst_size, timeout = 1, verbose = 0)
    
    #Get RTT Average
		for (sent, received) in response:
			
			#Increase recieved adresses counter for this Ip
			adresses[received.src] += 1
			
			#Increment RTT counter
			rtt_acum += (received.time - sent.sent_time)
			rtt_counter += 1
			
			#Set flacg if echo-reply
			if(received.type == 0):
				echoReplyNotFound = False
    
    
		if rtt_counter > 0 :
		  rtt_average = rtt_acum / rtt_counter
		
		  data_object = {
		    "rtt" : round(rtt_average , 6),
		    "ip_adress" : ' '+str(adresses.most_common(1)[0][0])+' ',
            "salto_intercontinental" : False,
		    "hop_num" : current_ttl,

		    
		  }
		  
		  
		  global_rtt_acum    += rtt_average
		  global_rtt_counter += 1
		  global_rtt_samples.append(rtt_average) 
	    
		  
		else:
		  data_object = {
		    "rtt" : None,
		    "ip_adress" : None,
		    "salto_intercontinental" : False,
		    "hop_num" : current_ttl
		    
		  }  
		  global_null_packets_amount = global_null_packets_amount +1
		
		
		global_total_packets_amount = global_total_packets_amount +1  
		result_per_ttl.append(data_object)

		current_ttl += 1
		rtt_acum = 0
		rtt_counter = 0
		adresses.clear()
	
	#Calculate Overall Average
	global_rtt_average = global_rtt_acum / global_rtt_counter
	
	#Calculate Standard Deviation
	for rtt_sample in global_rtt_samples :
	  global_standard_deviation_acum +=  ( (rtt_sample - global_rtt_average )**2 )
	
	global_standard_deviation = math.sqrt(global_standard_deviation_acum / global_rtt_counter)
	
	#Calculate Z-Value for each rtt
	for rtt_sample in global_rtt_samples :
	  z_value = ( rtt_sample - global_rtt_average ) / global_standard_deviation
	  standard_values.append(z_value)
	
	
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
