#! /usr/bin/env python

import sys
from scapy.all import rdpcap
from math import log
import pickle

def dict_add(dic, key):
    if key in dic:
        dic[key] += 1
    else:
        dic[key] = 1

def tipo(n):
    if str(n) in types:
        return types[str(n)]
    else:
        return str(hex(n))

types = pickle.load(open('tipos.p', 'rb'))

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

    #Lleno los diccionarios
    paquetes_S1 = 0
    paquetes_S2 = 0

    for pkt in packets:

        # Clasifico paquetes para la fuente S1 como (broadcast/unicast, type)
        if 'type' in pkt.fields and 'dst' in pkt.fields:
            if pkt.dst == broadcast_address:
                dict_add(S1_dict, ('broadcast', pkt.type))
            else:
                dict_add(S1_dict, ('unicast', pkt.type))
            paquetes_S1 += 1

        # Clasifico paquetes ARP para la fuente S2 si son de tipo who-is
        # de acuerdo al emisor
        if 'type' in pkt.fields:
            if pkt.type == ARP_type and pkt.op == 1:
                dict_add(S2_dict, pkt.psrc)
                paquetes_S2 += 1

    # Fuente S1
    logfile.write('#' * 45 + " FUENTE S1 " + '#' * 45 + '\n')
    logfile.write("{:^18} {:^55} {:^14} {:^12}".format("Broadcast/Unicast",
        "Protocolo", "Probabilidad", "Información") + '\n')
    logfile.write('-' * 101 + '\n')

    entropia_muestral = 0
    for cast, protocol in S1_dict:
        probabilidad = S1_dict[(cast, protocol)]/float(paquetes_S1)
        informacion = -log(probabilidad, 2)
        entropia_muestral += probabilidad*informacion
        logfile.write("{:^18} {:^55} {:^14} {:^12}".format(cast, tipo(protocol),
            "{0:.3f}".format(probabilidad), "{0:.3f}".format(informacion)) + '\n')

    entropia_maxima = log(len(S1_dict), 2)

    logfile.write("\n# Entropía muestral = " +
        "{0:.3f}".format(entropia_muestral) + '\n')
    logfile.write("# Entropía máxima = " + "{0:.3f}".format(entropia_maxima) + '\n\n')

    # Fuente S2
    logfile.write('#' * 16 + " FUENTE S2 " + '#' * 16 + '\n')
    logfile.write("{:^16} {:^14} {:^12}".format("IP emisora", "Probabilidad", "Información") + '\n')
    logfile.write('-' * 43 + '\n')

    entropia_muestral = 0
    for ip in S2_dict:
        probabilidad = S2_dict[ip]/float(paquetes_S2)
        informacion = -log(probabilidad, 2)
        entropia_muestral += probabilidad*informacion
        logfile.write("{:^16} {:^14} {:^12}".format(ip, "{0:.3f}".format(probabilidad),
            "{0:.3f}".format(informacion)) + "\n")

    entropia_maxima = log(len(S2_dict), 2)

    logfile.write("\n# Entropía muestral = " +
        "{0:.3f}".format(entropia_muestral) + '\n')
    logfile.write("# Entropía máxima = " + "{0:.3f}".format(entropia_maxima) + '\n\n')

    logfile.close()
