import urllib.request
from time import sleep

branchURL = "www.geocities.com/Athens/"
sleepTime = 5

dest = 'jsons/'

def fetchURL(url):
	finished = False
	while not finished:
		try:
			fetch = urllib.request.urlopen(url)
			text = fetch.read().decode('utf-8')
			finished = True
		except:
			print("Error, trying again in " + str(sleepTime) + " seconds.")
			sleep(sleepTime)
			finished = False
	return text
	
def buildQuery(url):
	prefix = "http://web.archive.org/cdx/search/cdx?url="
	appendix = "&matchType=prefix&output=json"
	return prefix + url + appendix
	
#first, get total number of pages
queryBase = buildQuery(branchURL)
numPages = fetchURL(queryBase + "&showNumPages=true").strip('\n')

print("Found " + numPages + " pages of results")

for p in range(0,int(numPages)):
	print("Fetching " + str(p))
	json = fetchURL(queryBase + "&page=" + str(p))
	with open('jsons/' + str(p) + '.json',mode='w',encoding='utf-8') as file:
		file.write(json)
	print("Complete\n")