import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rcParams['text.latex.unicode']=True

rtt = dict()
saltos = dict()
outliers = dict()

outliers["tokyo"] = [7, 9, 11]
outliers["ghana"] = [6, 8, 13]
outliers["ljubljana"] = [2, 6, 8]

saltos["tokyo"] = list(range(1, 16)) + [19, 20]
saltos["ghana"] = list(range(1, 20))
saltos["ljubljana"] = list(range(1, 13))

rtt["tokyo"] = [0.0017325083414713542,
0.005170042514801025,
0.025891196727752686,
0.018583366870880125,
0.017830891609191893,
0.018952195644378663,
0.04350351333618164,
0.145841326713562,
0.15910194396972657,
0.2012411069869995,
0.20321641206741334,
0.3121191906929016,
0.30716083288192747,
0.3099595808982849,
0.3081473233748455,
0.32519585371017456,
0.32267810583114626]

rtt["ghana"] = [0.002174854278564453,
0.006007180213928222,
0.016784078196475382,
0.014113867282867431,
0.013317852020263672,
0.014758341312408448,
0.15843845129013062,
0.17140392780303956,
0.23086218118667604,
0.22283175468444824,
0.22247609853744507,
0.22513556718826294,
0.22188199758529664,
0.5116087940503966,
0.321972278227289,
0.33367799628864636,
0.32982293764750165,
0.3453131516774495,
0.33933292735706677]

rtt["ljubljana"] = [0.005760351816813151,
0.004727878570556641,
0.02693478684676321,
0.016697497367858888,
0.015507066249847412,
0.02479156494140625,
0.25313496828079224,
0.26100012063980105,
0.38406392900567304,
0.398231104016304,
0.37075865983963013,
0.2604352784156799]


for u in rtt:
	data = rtt[u]
	for i in range(len(data)-1, 0, -1):
		data[i] -= data[i-1]

	hops = saltos[u]

	# for i in range(len(hops)):
	# 	hops[i] -= 0.5

	hops_out = list()
	hops_in = list()
	for i, v in enumerate(hops):
		if i in outliers[u]:
			hops_out.append(v)
		else:
			hops_in.append(v)

	data_out = list()
	data_in = list()
	for i, v in enumerate(data):
		if i in outliers[u]:
			data_out.append(v)
		else:
			data_in.append(v)

	plt.scatter(hops_in, data_in, marker='.', s=150, color='cornflowerblue', label='No outliers')
	plt.scatter(hops_out, data_out, marker='.', s=150, color='darkorange', label='Outliers')
	plt.xlabel("Salto")
	plt.ylabel("Diferencia de RTT con el salto anterior")
	plt.grid(True)
	plt.xticks(np.arange(min(hops), max(hops)+1, 1.0))
	plt.legend()
	plt.savefig(u+'1.png', bbox_inches='tight', dpi=200)
	# plt.show()
	plt.clf()

	mean = sum(data)/len(data)
	sum_ = 0
	for d in data:
		sum_ += (d - mean) ** 2
	Sdev = sqrt(sum_ / (len(data)-1))

	data2 = list()

	for d in data:
		data2.append((d - mean) / Sdev)

	data2_out = list()
	data2_in = list()
	for i, v in enumerate(data2):
		if i in outliers[u]:
			data2_out.append(v)
		else:
			data2_in.append(v)

	plt.scatter(data_in, data2_in, marker='.', s=150, color='cornflowerblue', label='No outliers')
	plt.scatter(data_out, data2_out, marker='.', s=150, color='darkorange', label='Outliers')
	plt.xlabel("Diferencia de RTT con el salto anterior")
	plt.ylabel("$(X_i - \overline{X})/S$")
	plt.grid(True)
	plt.legend()
	plt.savefig(u+'2.png', bbox_inches='tight', dpi=200)
	# plt.show()
	plt.clf()