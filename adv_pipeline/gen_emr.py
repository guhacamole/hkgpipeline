import random

def generate_emr(size = 5000000):

	diseases = ["diabetes", "covid19", "tuberculosis", "malaria", "dengue", "ischemic stroke", "alzheimers", "hepatitis-C", "typhoid"]
	symptoms = ["cough", "fever", "headache", "nausea", "fatigue", "diarrhoea", "shortness of breath", "muscle-ache", "loss of appetite", "pallor", "vomiting"]
	drugs = ["paracetamol", "insulin", "albuterol", "fluticasone", "levothyroxine", "rosuvastatin", "esomeprazole", "pregabalin"]


	disease_df, diseases_probab = generate_disease(diseases,size)
	symptom_df = generate_symptoms(symptoms,diseases,diseases_probab,disease_df)
	drug_df = generate_symptoms(drugs,diseases,diseases_probab,disease_df) #Similar functions and distributions for symptoms and drugs
	age_df, gen_df = generate_demo(diseases,diseases_probab,disease_df)

	finaldf = list(map(list,zip(disease_df,symptom_df,drug_df,age_df,gen_df)))

	return finaldf

def data2file(data):

	f = open('emr.csv',"w")
	f.write("Disease(s),Symptom(s),Drug(s),Age,Gender\n")
	for i in range(len(data)):
		line = ""
		record = data[i]
		s = [None] * len(record)
		for j in range(len(record)):
			if isinstance(record[j],list):
				s[j] = ";".join(record[j])
			else:
				s[j] = record[j]
		line = ",".join(s) + "\n"
		f.write(line)
	f.close()

def generate_symptoms(symptoms,diseases,diseases_probab,dis_df): #can also be used for drugs, same logic

	symptoms_probab = [None] * len(symptoms)
	symptom_probab_array = [[None]*len(symptoms) for i in range(len(diseases))]
	random.shuffle(symptoms)

	for i in range(len(symptoms)):
		if random.random() < 0.5:
			symptoms_probab[i] = random.randint(1,10)
		else:
			symptoms_probab[i] = 10*random.randint(1,10)

	for i in range(len(diseases)):
		for j in range(len(symptoms)):
			if diseases_probab[i] <= 10 and symptoms_probab[j] <=10:
				if random.random() < 1/3:
					symptom_probab_array[i][j] = random.randint(0,5)
				else:
					symptom_probab_array[i][j] = random.randint(1,10)
			else:
				if random.random() < 2/3:
					symptom_probab_array[i][j] = random.randint(1,10)
				else:
					symptom_probab_array[i][j] = 10*random.randint(1,10)

	sym_df = [None] * len(dis_df)
	for t in range(len(dis_df)):
		if len(dis_df[t]) == 1:
			if random.random() < 0.2:
				sym = random.choices(symptoms,symptom_probab_array[diseases.index(dis_df[t][0])],k=1)
			else:
				sym1 = random.choices(symptoms,symptom_probab_array[diseases.index(dis_df[t][0])],k=1)[0]
				sym2 = random.choices(symptoms,symptom_probab_array[diseases.index(dis_df[t][0])],k=1)[0]
				if sym1 != sym2:
					sym = [sym1,sym2]
				else:
					sym = [sym1]
		elif len(dis_df[t]) == 2:
			sym1 = random.choices(symptoms,symptom_probab_array[diseases.index(dis_df[t][0])],k=1)[0]
			sym2 = random.choices(symptoms,symptom_probab_array[diseases.index(dis_df[t][1])],k=1)[0]
			sym3 = random.choices(symptoms,symptom_probab_array[diseases.index(dis_df[t][random.randint(0,1)])],k=1)[0]

			sym = list(set([sym1,sym2,sym3]))

		sym_df[t] = sym

	return sym_df

def generate_demo(diseases,diseases_probab,dis_df):

	median_age = [random.randint(33,60)] * (len(diseases))
	age_df = [None] * len(dis_df)

	for k in range(len(dis_df)):
		if len(dis_df[k]) == 1:
			age = median_age[diseases.index(dis_df[k][0])] + random.randint(-15,15)
		elif len(dis_df[k]) == 2:
			age1 = median_age[diseases.index(dis_df[k][0])] + random.randint(-15,15)
			age2 = median_age[diseases.index(dis_df[k][1])] + random.randint(-15,15)
			age3 = int((age1 + age2)/2)
			age = random.choice([age1,age2,age3,age3])
		
		age_df[k] = str(age)

	genders = ["M","F"]
	gen_dis = [random.randint(-2,2)] * len(dis_df)
	gen_df = [None] * len(dis_df)

	for k in range(len(dis_df)):
		if len(dis_df[k]) == 1:
			gn = gen_dis[diseases.index(dis_df[k][0])] + random.randint(-1,1)
		else:
			gn1 = gen_dis[diseases.index(dis_df[k][0])] + random.randint(-1,1)
			gn2 = gen_dis[diseases.index(dis_df[k][1])] + random.randint(-1,1)
			gn3 = (gn1 + gn2)/2
			gn = random.choice([gn1,gn2,gn3,gn3])
		if gn == 0:
			gen = random.choice(genders)
		elif gn > 0:
			gen = genders[0]
		else:
			gen = genders[1]

		gen_df[k] = gen

	return age_df, gen_df

def generate_disease(diseases,size):

	diseases_probab = [None] * len(diseases)
	diseases_probab_array = [[None]*len(diseases) for i in range(len(diseases))]
	random.shuffle(diseases)

	for i in range(len(diseases)):
		if random.random() < 0.5:
			diseases_probab[i] = random.randint(1,10)
		else:
			diseases_probab[i] = 10*random.randint(1,10)

	dis_df = random.choices(diseases,diseases_probab, k = size)

	for i in range(len(diseases)):
		for j in range(len(diseases)):
			if i == j:
				diseases_probab_array[i][j] = 0
			elif i != j:
				if diseases_probab[i] <= 10 and diseases_probab[j] <= 10:
					if random.random() < 2/3:
						diseases_probab_array[i][j] = 0
					else:
						diseases_probab_array[i][j] = random.randint(1,10)
				else:
					if random.random() < 2/3:
						diseases_probab_array[i][j] = random.randint(1,10)
					else:
						diseases_probab_array[i][j] = 10*random.randint(1,10)

	for t in range(len(dis_df)):
		if random.random() < 0.1:
			d1 = random.choices(diseases,diseases_probab_array[diseases.index(dis_df[t])],k=1)[0]
			dis_df[t] = [dis_df[t],d1]
		else:
			dis_df[t] = [dis_df[t]]

	return dis_df, diseases_probab



if __name__ == "__main__":
	emr = generate_emr(size = 500)
	data2file(emr)



'''
length = [0] * 2
for elem in dis_df:
	length[len(elem)-1]+=1
print(length)
'''