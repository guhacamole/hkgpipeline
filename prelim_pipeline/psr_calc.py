from math import log10
import csv

def file2list(file):
	f = open(file,"r")
	data = list()
	next(f)
	for line in f:
		line = line.strip("\n")
		l = line.split(",")
		data.append(l)
	return data


def psrcalc(file, nmin = 0, R = 0):
	data = file2list(file)

	l = 0
	for iter0 in data:
		if iter0[1] != "diseases":
			l += 1

	psrdata = [[None] * 4] * l
	para = [[None] * 6] * l
	
	k = 0
	for iter1 in data:
		probability = 0
		specificity = 0
		if iter1[1] != "diseases":

			nco0 = int(iter1[3]) #Co occurence number
			nco1 = 0 #Total co occurence number
			ctr0 = 0 #Occurence Number
			ctr1 = 0 #Total occurence Number

			for iter2 in data:
				if iter1[1] == iter2[1]:
					if iter1[0] == iter2[0]:
						ctr0 += int(iter2[3])
					ctr1 += int(iter2[3])
					if iter1[2] == iter2[2]:
						nco1 += int(iter2[3])
			probability = nco0/ctr0
			specificity = probability/(nco1/ctr1)
			reliability = log10(max(1,1+nco0-nmin)) + R
			psr = probability * specificity * reliability

			#Insert code for if it's diseases
			para[k] = iter1
			para[k].extend([psr, probability,specificity,reliability])

			psrdata[k] = iter1[0:3] + iter1[4:5]
			k += 1
	return psrdata, para

def postprocess(predata,psrcutoff = 0.22):

	postdata = list()

	for i in range(len(predata)):
		if predata[i][3] > psrcutoff:
			postdata.append(predata[i])
			#predata[i].pop()

	print(len(postdata),len(predata),sep = ",")
	return postdata

def data2file(data,file):
	headers = ["sb","pr","ob","wt"] #Subject,Predicate,Object,Weight

	with open(file,"w") as file:
		W = csv.writer(file)
		W.writerow(headers)
		W.writerows(data)

psr, para = psrcalc("data-5m.csv", nmin = 5, R = 1)
finalpsr = postprocess(psr)

data2file(finalpsr,"psrdata.csv")