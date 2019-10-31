from glob import glob
from time import sleep
from os.path import exists
from os import mkdir
from urllib.request import Request,urlopen
import time

filelist = sorted(glob('bydate/*.tsv'))
delimit = '\t'
targetDir = 'storage/'
sleepTime = 0.5 
excludes = {'http://geocities.com:80/Athens/Aegean/4994/oleary.html'}

useragent = {'User-Agent':'Academic research crawler operated by Michael L. Black, 1 request per 0.5 seconds, michael_black@uml.edu for questions or concerns'}

def makeRequest(url,date):
	return Request('http://web.archive.org/web/' + date + '/' + url,headers=useragent)

def fetchURL(url):
	finished = False
	errorcount = 0
	while not finished:
		try:
			fetch = urlopen(url,timeout=30)
			text = fetch.read().decode('utf-8')
			finished = True
		except:
			errorcount += 1
			if errorcount < 10:
				print("Error, trying again in " + str(sleepTime) + " seconds.")
				sleep(sleepTime)
				finished = False
			else:
				return '##ERROR##'
	return text

def removeArchiveStamp(text):
	## DEPRECIATED, NOW HANDLED DURING PRE-PROCESSING
	#text = text[text.find('<!-- END WAYBACK TOOLBAR INSERT -->')+35:]
	#text = text[:text.find('<!--\n     FILE ARCHIVED ON')]
	return text	

bigCounter = 0	
for filename in filelist:
	print("Pulling from " + filename)
	datalist = list()
	with open(filename,encoding='utf-8') as file:
		for line in file:
			datalist.append(line.strip().split(delimit))
	for entry in datalist:
		bigCounter += 1
		stamp = time.strftime('%H:%M:%S')
		dateDir = entry[1][:6]
		saveName = entry[0][entry[0].lower().find('athens'):].replace('/','!')
		if exists(targetDir + dateDir + '/' + saveName):
			print(stamp + ' ' + str(bigCounter) + ": Already captured " + entry[0])
			continue
		elif '?' in saveName or ':' in saveName or '%' in saveName:
			print("- Invalid URL " + entry[0] + ". Skipping for now")
			with open('errors.tsv',mode='a',encoding='utf-8') as file:
				file.write(entry[0] + delimit + entry[1] + '\n')
			continue
		elif entry[0] in excludes:
			print(stamp + ' ' + str(bigCounter) + ': Excluded URL ' + entry[0])
			continue
		print(stamp + ' ' + str(bigCounter) + ": Capturing " + entry[0])
		webpage = fetchURL(makeRequest(entry[0],entry[1]))
		if webpage == '##ERROR##':
			print("- Error fetching page. Skipping for now.")
			with open('errors.tsv',mode='a',encoding='utf-8') as file:
				file.write(entry[0] + delimit + entry[1] + '\n')
			continue
		if not exists(targetDir + dateDir):
			mkdir(targetDir + dateDir)
		with open(targetDir + dateDir + '/' + saveName,mode='w',encoding='utf-8') as file:
			file.write(removeArchiveStamp(webpage))
		print("- Complete!")
		sleep(sleepTime)
print("Finished " + str(len(filelist)))
