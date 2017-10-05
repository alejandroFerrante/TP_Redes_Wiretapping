#! /usr/bin/env python

import sys
# from collections import defaultdict
from types_dic import types_dic
from scapy.all import *
from math import exp, log

def dict_add(dic, key):
    if key in dic:
        dic[key] += 1
    else:
        dic[key] = 1

broadcast_address = 'ff:ff:ff:ff:ff:ff'
ARP_type = 2054


if __name__ == '__main__':
    
    # Levantar el pcap
    packets = rdpcap(sys.argv[1])
    logfile = open("data_S.log", "w")
    logfile.write("# Paquetes vistos: " + str(len(packets)) + "\n")
    logfile.write("\n")

    # dicc de tipos observados
    S1_dict = dict()
    S2_dict = dict()

    # obs_types_dic = defaultdict(int)
    # arp_dic = defaultdict(int)

    #Lleno los diccionarios
    paquetes_S1 = 0
    paquetes_S2 = 0

    # pkt_arp_count = 0

    for pkt in packets:

        # Clasifico paquetes para la fuente S1 como (broadcast/unicast, type)
        if 'type' in pkt.fields and 'dst' in pkt.fields:
            if pkt.dst == broadcast_address:
                dict_add(S1_dict, ('broadcast', pkt.type))
            else:
                dict_add(S1_dict, ('unicast', pkt.type))
            paquetes_S1 += 1

        # Clasifico paquetes ARP para la fuente S2 si son de tipo who-is de acuerdo a que IP buscan 
        if 'type' in pkt.fields:
            if pkt.type == ARP_type and pkt.op == 1:
                dict_add(S2_dict, pkt.pdst)
                paquetes_S2 += 1

        #     # Cuento un paquete solo del type ARP para la fuente S_1
        #     type_str = str(hex(pkt.fields['type']))
            
        #     # Cuento un paquete mas del type correspondiente para la fuente S
        #     dict_add(obs_types_dic, type_str)

        #     # Logueamos si encontramos un paquete de tipo desconocido para el dict
        #     if not type_str in types_dic:
        #         print type_str
            
        #     # Si el paquete es ARP de tipo who-has guardamos su ip destino
        #     if types_dic[type_str] == "ARP" and pkt.op == 1:
        #         dict_add(arp_dic, pkt.pdst)
        #         pkt_arp_count += 1


        # # Caso especial 802.3
        # elif 'len' in pkt.fields:
        #     dict_add(obs_types_dic, "0xff0f")

    # Fuente S1

    # probabilidad de la fuente S1
    # entropia_s = 0
    # prob_tmp = 0
    
    logfile.write("## Fuente S1 ##\n")
    logfile.write("Broadcast/Unicast | Protocolo | Probabilidad | Informacion\n")
    logfile.write("\n")

    for cast, protocol in S1_dict:
        logfile.write(cast + " | " + types_dic[str(hex(protocol))] + " | " + "{0:.3f}".format(S1_dict[(cast, protocol)]/float(paquetes_S1)) + "\n")

    # for key, value in obs_types_dic.iteritems():
        
    #     prob_tmp = value/float(len(packets))
        
    #     if not key in types_dic:
    #         logfile.write("\"" + str(key) + "\"" + "\t" + str(prob_tmp) + "\t" + str(value) + "\n")
    #     else:
    #         logfile.write("\"" + types_dic[key] + "\"" + "\t" + str(prob_tmp) + "\t" + str(value) + "\n")
            
    #     entropia_s += prob_tmp * (-log(prob_tmp,2))
            
    # # entropia de la fuente S
    # logfile.write("\n")
    # logfile.write("#Entropia de S: " + str(entropia_s) + "\n\n")
    # logfile.close()

    # entropia_s_1 = 0
    # prob_tmp = 0
    
    # logfile_s1 = open("data_S1.log", "w")
    # logfile_s1.write("#Paquetes ARP vistos: " + str(pkt_arp_count) + "\n")
    # logfile_s1.write("\n")

    # logfile_s1.write("# Direccion \t Probabilidad \t Cantidad de paquetes \n")
    # logfile_s1.write("\n")

    # # probabilidad de la fuente S_1
    # for key, value in arp_dic.iteritems():
    #     prob_tmp = value/float(pkt_arp_count)
    #     logfile_s1.write(str(key) + "\t" + str(prob_tmp) + "\t" + str(value) + "\n")
    #     entropia_s_1 += prob_tmp * (-log(prob_tmp,2))
    
    # # entropia de la fuente S1
    # logfile_s1.write("\n")
    # logfile_s1.write("#Entropia de S_1: " + str(entropia_s_1) + "\n\n")
    # logfile_s1.close()
    
    
