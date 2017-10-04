#! /usr/bin/env python

import sys
from collections import defaultdict
from types_dic import types_dic
from scapy.all import *
from math import exp, log

def fill_dict(dic, key):
    if key in dic:
        dic[key] += 1
    else:
        dic[key] = 1


if __name__ == '__main__':
    
    # Levantar el pcap
    packets = rdpcap(sys.argv[1])
    logfile = open("data_S.log", "w")
    logfile.write("# Paquetes vistos: " + str(len(packets)) + "\n")
    logfile.write("\n")

    # dicc de tipos observados
    obs_types_dic = defaultdict(int)
    arp_dic = defaultdict(int)


    #Llenar los diccionarios
    pkt_arp_count = 0
    for pkt in packets:

        if 'type' in pkt.fields:

            # Cuento un paquete solo del type ARP para la fuente S_1
            type_str = str(hex(pkt.fields['type']))
            
            # Cuento un paquete mas del type correspondiente para la fuente S
            fill_dict(obs_types_dic, type_str)

            # Logueamos si encontramos un paquete de tipo desconocido para el dict
            if not type_str in types_dic:
                print type_str
            
            # Si el paquete es ARP de tipo who-has guardamos su ip destino
            if types_dic[type_str] == "ARP" and pkt.op == 1:
                fill_dict(arp_dic, pkt.pdst)
                pkt_arp_count += 1


        # Caso especial 802.3
        elif 'len' in pkt.fields:
            fill_dict(obs_types_dic, "0xff0f")

    # probabilidad de la fuente S
    entropia_s = 0
    prob_tmp = 0
    
    logfile.write("# Tipo \t Probabilidad \t Cantidad de paquetes\n")
    logfile.write("\n")

    for key, value in obs_types_dic.iteritems():
        
        prob_tmp = value/float(len(packets))
        
        if not key in types_dic:
            logfile.write("\"" + str(key) + "\"" + "\t" + str(prob_tmp) + "\t" + str(value) + "\n")
        else:
            logfile.write("\"" + types_dic[key] + "\"" + "\t" + str(prob_tmp) + "\t" + str(value) + "\n")
            
        entropia_s += prob_tmp * (-log(prob_tmp,2))
            
    # entropia de la fuente S
    logfile.write("\n")
    logfile.write("#Entropia de S: " + str(entropia_s) + "\n\n")
    logfile.close()

    entropia_s_1 = 0
    prob_tmp = 0
    
    logfile_s1 = open("data_S1.log", "w")
    logfile_s1.write("#Paquetes ARP vistos: " + str(pkt_arp_count) + "\n")
    logfile_s1.write("\n")

    logfile_s1.write("# Direccion \t Probabilidad \t Cantidad de paquetes \n")
    logfile_s1.write("\n")

    # probabilidad de la fuente S_1
    for key, value in arp_dic.iteritems():
        prob_tmp = value/float(pkt_arp_count)
        logfile_s1.write(str(key) + "\t" + str(prob_tmp) + "\t" + str(value) + "\n")
        entropia_s_1 += prob_tmp * (-log(prob_tmp,2))
    
    # entropia de la fuente S1
    logfile_s1.write("\n")
    logfile_s1.write("#Entropia de S_1: " + str(entropia_s_1) + "\n\n")
    logfile_s1.close()
    
    
