from glob import glob
import json

filelist = glob('jsons/*.json')

data = list()
counter = 0
linenum = 0
for filename in filelist:
	counter += 1
	print("Processing " + filename + ": " + str(counter) + " of " + str(len(filelist)))
	with open(filename,encoding='utf-8') as file:
		lines = file.readlines()
	for line in lines[1:]:
		entry = json.loads(line.strip('\n,').replace(']]',']'))
		## Need to figure out what to do with these no message lines
		if entry[4] == '-':
			continue
		elif int(entry[4]) >= 200 and int(entry[4]) < 300 and entry[3] == 'text/html':
			data.append(entry)
	
with open('htmlonly-index.tsv',mode='w',encoding='utf-8') as file:
	for entry in data:
		file.write(entry[0])
		for item in entry[1:]:
			file.write('\t'+item)
		file.write('\n')