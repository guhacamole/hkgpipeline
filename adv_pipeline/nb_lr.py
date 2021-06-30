#Script to learn through Naive Bayes & Logistic Regression
import pandas
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

def NB(file = "emr-50k.csv", predicate = "symptoms", type="GaussianNB()"):

	diseases = ["diabetes", "covid19", "tuberculosis", "malaria", "dengue", "ischemic stroke", "alzheimers", "hepatitis-C", "typhoid"]
	symptoms = ["cough", "fever", "headache", "nausea", "fatigue", "diarrhoea", "shortness of breath", "muscle-ache", "loss of appetite", "pallor", "vomiting"]
	drugs = ["paracetamol", "insulin", "albuterol", "fluticasone", "levothyroxine", "rosuvastatin", "esomeprazole", "pregabalin"]

	rawdata = returnraw(file)

	ds_data = process(rawdata,predicate)
	X1,y1 = array(ds_data,diseases,symptoms)
	X,y = onevsall(ds_data,"diabetes",diseases,symptoms)

	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
	gnb = GaussianNB()
	gnb.fit(X_train,y_train)
	y_pred = gnb.predict(X_test)
	y_train_pred = gnb.predict(X_train)
	print("GNB Model Accuracy on test data (One vs all):", metrics.accuracy_score(y_test, y_pred)*100)
	print("GNB Model Accuracy on training data (One vs all):", metrics.accuracy_score(y_train, y_train_pred)*100)
	

	#for i in range(len(y)):
		#print(X[i],y[i],sep=":")

	dd_data = process(rawdata,predicate = "drugs")
	dd_dict = table(dd_data,diseases,drugs)

def LR(file = "emr-50k.csv", predicate = "symptoms", beverbose = False):

	diseases = ["diabetes", "covid19", "tuberculosis", "malaria", "dengue", "ischemic stroke", "alzheimers", "hepatitis-C", "typhoid"]
	symptoms = ["cough", "fever", "headache", "nausea", "fatigue", "diarrhoea", "shortness of breath", "muscle-ache", "loss of appetite", "pallor", "vomiting"]
	drugs = ["paracetamol", "insulin", "albuterol", "fluticasone", "levothyroxine", "rosuvastatin", "esomeprazole", "pregabalin"]

	rawdata = returnraw(file)

	weights = []

	ds_data = process(rawdata,predicate)

	for each_dis in diseases:

		X,y = onevsall(ds_data,each_dis,diseases,symptoms)

		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
		logreg = LogisticRegression()
		logreg.fit(X_train,y_train)
		y_pred = logreg.predict(X_test)
		y_train_pred = logreg.predict(X_train)

		if beverbose:
			print("LR Model Accuracy on test data (One vs all) for " + str(each_dis) + ":", metrics.accuracy_score(y_test, y_pred)*100)
			print("LR Model Accuracy on training data (One vs all) for " + str(each_dis) + ":", metrics.accuracy_score(y_train, y_train_pred)*100)

		wt = logreg.coef_[0]
		for i in range(len(wt)):
			if wt[i] < 0:
				wt[i] = 0
		weights.append(wt)

	dd_data = process(rawdata,predicate = "drugs")
	dd_dict = table(dd_data,diseases,drugs)

	return weights

def returnraw(file):

	with open(file,"r") as f:
		next(f)
		emrdata = f.readlines()
	for i in range(len(emrdata)):
		data = emrdata[i]
		data = data.strip()
		data = data.split(",")
		data[3] = int(data[3])
		for k in range(3):
			data[k] = data[k].split(";")
		emrdata[i] = data

	return emrdata

def process(emrdata,predicate, order = ["diseases","symptoms","drugs","age","gender"]):

	rawdata = [[data[0],data[order.index(predicate)]] for data in emrdata]
	l = 0
	for data in rawdata:
		l += len(data[0])
	processdata = [None] * l
	k = 0
	for data in rawdata:
		if len(data[0]) == 1:
			processdata[k] = data
		else:
			processdata[k] = [[data[0][0]],data[1]]
			processdata[k+1] = [[data[0][1]],data[1]]
		k += len(data[0])

	return processdata

def table(processdata,subject_list, object_list, demo = False):

	table_dict = {key: list() for key in subject_list}

	if not demo:
		for i in range(len(processdata)):
			line = processdata[i]
			i += 1
			arr = [0] * len(object_list)
			for elem in line[1]:
				arr[object_list.index(elem)] = 1
			table_dict[line[0][0]].append(arr)

	#for key, value in table_dict.items():
		#print(key)
		#[print(line) for line in value]
		#print("\n")

	return table_dict

def array(processdata, subject_list, object_list, demo = False):

	table_para = []
	table_classes = []

	if not demo:
		for i in range(len(processdata)):
			line = processdata[i]
			arr = [0] * len(object_list)
			table_classes.append(line[0][0])
			for elem in line[1]:
				arr[object_list.index(elem)] = 1
			table_para.append(arr)

	return table_para, table_classes

def onevsall(processdata, subject, subject_list, object_list, demo = False):

	table_para = []
	table_classes = []

	if not demo:
		for i in range(len(processdata)):
			line = processdata[i]
			arr = [0] * len(object_list)
			if line[0][0] == subject:
				table_classes.append(1)
			else:
				table_classes.append(0)
			for elem in line[1]:
				arr[object_list.index(elem)] = 1
			table_para.append(arr)

	return table_para, table_classes



diseases = ["diabetes", "covid19", "tuberculosis", "malaria", "dengue", "ischemic stroke", "alzheimers", "hepatitis-C", "typhoid"]
symptoms = ["cough", "fever", "headache", "nausea", "fatigue", "diarrhoea", "shortness of breath", "muscle-ache", "loss of appetite", "pallor", "vomiting"]

lrweights = LR(file = "emr-500.csv", beverbose = False)

with open("lrweights.csv", "w") as f:

	f.write("sb,wt,ob\n")
	for i in range(len(diseases)):
		for j in range(len(lrweights[i])):
			wt = lrweights[i][j]
			if wt > 0.2:
				sb = diseases[i]
				ob = symptoms[j]
				wt = str(wt)
				f.write(",".join([sb,wt,ob]) + "\n")
#NB(file = "emr-500.csv")