from bs4 import BeautifulSoup
import bs4
from glob import glob

dataDir = 'storage/'
outname = 'fullcount-162910-tagcount.csv'

print("Building filelist...")
filelist = glob(dataDir + '**/Athens*',recursive=True)

counter = 0
alltags = dict()
tagtypes = dict()	# This will be the dictionary that holds values for all docs. Insert a check below to reject already parsed pages

for filename in filelist:
	counter += 1
	## CHECK FOR PARSED GOES HERE
	## Crop full filename to Athens/.. and reject if already in dictionary
	pagename = filename
	tagtypes[pagename] = dict()
	print(str(counter) + ": " + filename)
	if filename.endswith('.map') or filename.endswith('.css'):
		continue
	with open(filename,encoding='utf-8') as file:
		webpage = BeautifulSoup(file.read(),"lxml")
	for htmltag in list(webpage.descendants):
		# Check to see if its a valid tag, bad formatting from author, or junk inserted by Geocities/Archive.org
		if type(htmltag.name) != type(str()):
			continue
		elif htmltag.name not in tagtypes[pagename]:
			tagtypes[pagename][htmltag.name] = 0
		if htmltag.name not in alltags:
			alltags[htmltag.name] = 0
		tagtypes[pagename][htmltag.name] += 1
		alltags[htmltag.name] += 1
		
print("Complete. Writing results to disk as " + outname)
empty = 0
with open(outname,mode='w',encoding='utf-8') as file:
	for webpage in sorted(tagtypes.keys()):
		if len(tagtypes[webpage].keys()) == 0:
			empty += 1
		file.write(webpage)
		for htmltag in sorted(tagtypes[webpage].keys()):
			file.write(',' + htmltag + '=' + str(tagtypes[webpage][htmltag]))
		file.write('\n')
	
with open('bigtaglist.csv',mode='w',encoding='utf-8') as file:
	for htmltag in sorted(alltags.keys()):
		file.write(htmltag + ',' + str(alltags[htmltag]) + '\n')
		
print(str(len(tagtypes)) + ' pages processed.')
print(str(empty) + ' pages with errors due to archive bar removal.')