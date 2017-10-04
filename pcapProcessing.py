#!/usr/bin/python

#bokeh

import re
from math import log

print ("Lets Processs this Shit!")
print ("Reading File...")


#Initialize Dictionary of appearences
appearanceDictionary = {}

#Initialize Dictionary of packet sizes
packetSizesDictionary = {}

#Initialize counter
totalPackets = 0


#Open File
file = open('C:/Users/Falcon/Desktop/TPRedes/NetworkDump01.txt','r') 


#Process Each Line
for line in file:

    #Get values
    values = line.split(',')
    
    #Process only TCP packets
    if values[4].find('TCP') != -1:

        #print('READING: SRC: '+values[2]+' DST: '+values[3]+' PROTOCOL: '+values[4]+' CONTENT SIZE: '+values[5]+' CONTENT: '+values[6])
        
        #Increment counter
        totalPackets = totalPackets + 1

        #Get packet content
        packetContent = values[6]

        #Get packet type
        indexFrom  = packetContent.find('[') + 1
        indexTo = packetContent.find(']')
    
        packetType = packetContent[indexFrom:indexTo]
        #

        #Adjust to group by different types of ACKs
        if 'ACK' in packetType:
            packetType = 'ACK'

        #Update appearance dictionary
        if packetType in appearanceDictionary:
            appearanceDictionary[packetType] = appearanceDictionary[packetType] + 1
        else:
            appearanceDictionary[packetType] = 1

        #Update packet sizes dictionary
        packetSize = int(values[5].replace('"' , ''))
        if packetType in packetSizesDictionary:
            packetSizesDictionary[packetType] = packetSizesDictionary[packetType] + packetSize
        else:
            packetSizesDictionary[packetType] = packetSize
            
        
print('TOTAL PACKETS PROCESSED:')
print(totalPackets)
print('*****************************************************************')
print('APPEARANCE OF EACH SYMBOL:')
print(appearanceDictionary)
print('*****************************************************************')


#Construct probability, information and average code length Dictionaries
probabilityDictionary = {}
informationDicionary = {}
averageCodeLengthDictionary = {}

entropy = 0
averageCodeLength = 0
typesAmount = 0
for key in appearanceDictionary :
    probabilityDictionary[key] = appearanceDictionary[key] / totalPackets
    informationDicionary[key] =  (- log( probabilityDictionary[key] , 2 ) )    
    averageCodeLengthDictionary[key] = packetSizesDictionary[key] / appearanceDictionary[key]
    averageCodeLength = averageCodeLength + (packetSizesDictionary[key] / appearanceDictionary[key])
    entropy = entropy + ( probabilityDictionary[key] * ( -log( probabilityDictionary[key] , 2 ) ) )
    typesAmount = typesAmount + 1
    
averageCodeLength = averageCodeLength / typesAmount

print('AVERAGE CODE SIZES')
print(averageCodeLengthDictionary)
print('*****************************************************************')
print('PROBABILITY OF EACH SYMBOL:')
print(probabilityDictionary)
print('*****************************************************************')
print('INFORMATION OF EACH SYMBOL:')
print(informationDicionary)
print('*****************************************************************')
print('ENTROPY:')
print(str(entropy))
print('*****************************************************************')
print('AVERAGE CODE LENGTH:')
print(str(averageCodeLength))
print('*****************************************************************')

for key in appearanceDictionary :
    print('CODE: "'+key+'" | PROBABILITY: '+str(probabilityDictionary[key])+' | INFORMATION: '+str(informationDicionary[key])+' ')
    
    
