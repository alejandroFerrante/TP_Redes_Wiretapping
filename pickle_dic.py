import pickle
import csv

dic = dict()

with open('ieee-802-numbers-1.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		dic[row['Ethertype (decimal)']] = row['Description']
	pickle.dump(dic, open('tipos.p', 'wb'))

