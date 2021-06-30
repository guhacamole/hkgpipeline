import random

total_size = 5000000
size = int(total_size/5)

diseases = ["diabetes", "covid19", "tuberculosis", "malaria", "dengue", "ischemic stroke", "alzheimers", "hepatitis-C", "typhoid"]
disease_probab = [0.15,0.25,0.15,0.1,0.05,0.05,0.15,0.1,0.05]

genders =["male", "female", "third"]
gender_probab = [0.495, 0.495, 0.01]

ageranges = ["18-34","35-49","50-64","65+"]
agerange_probab = [0.35,0.30,0.25,0.1]

symptoms = ["cough", "fever", "headache", "nausea", "fatigue", "diarrhoea", "shortness of breath", "muscle-ache", "loss of appetite", "pallor", "vomiting"]
symptom_probab = [0.2,0.245,0.05,0.105,0.05,0.095,0.05,0.055,0.05,0.05,0.05]

drugs = ["paracetamol", "insulin", "albuterol", "fluticasone", "levothyroxine", "rosuvastatin", "esomeprazole", "pregabalin"]
drug_probab = [0.4,0.15,0.05,0.15,0.05,0.05,0.1,0.05]

datapoints = [genders,ageranges,symptoms,drugs,diseases]
probabs = [gender_probab,agerange_probab,symptom_probab,drug_probab,disease_probab]
reln = ["genders","ageranges","symptoms","drugs","diseases"]
final_data = list()
for i in range(4):
	df1 = random.choices(diseases,disease_probab, k = size)
	df2 = random.choices(datapoints[i],probabs[i],k = size)
	df3 = [reln[i]] * size
	df = list(map(list,zip(df1,df3,df2)))
	final_data.extend(df)
n = 0
df = [None]* size
while n < size:
	d = [None] * 3
	d0 = random.choices(diseases,disease_probab,k=1)[0]
	d1 = random.choices(diseases,disease_probab,k=1)[0]
	if d0 != d1:
	 	if d0 > d1:
			temp = d1
			d1 = d0
			d0 = temp
		d = [d0, reln[i+1],d1]
		df[n] = d
		n += 1

final_data.extend(df)
print(len(final_data))

freq_dict = {}
for item in final_data:
	string = ",".join(item)
	if string in freq_dict:
		freq_dict[string] += 1
	else:
		freq_dict[string] = 1

print(len(freq_dict))

f = open('data.csv', "w")
f.write("Subject,Predicate,Object,Frequency\n")

for spo, freq in freq_dict.items():
	f.write(spo + "," + str(freq) + "\n")

f.close()