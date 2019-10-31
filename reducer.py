datafile = 'fulldates.csv'
outfile = 'uniqueurls.csv'

'''
Date file structure:
0 = filename (with yyyydd path prepend)
1 = homestead stub (everything after Athens, including subhomesteads)
2 = capture date
3 = number of dates scraped via regex
4 = top level (Y/N)

Reduction structure:
Top level key = stub 
- Leads into nested dictionary with keys as URL relative to geocities.com/...
-- capdates: set of all capture dates
-- regdates: set of all regex'd dates
-- toplevel: bool translation of Y/N
-- filelist: set all captured filenames based on relative URL
'''

print("Beginning scan of " + datafile)
fileDict = dict()
counter = 0
skip = 0

with open(datafile,encoding='utf-8') as file:
	for row in file.readlines():
		counter += 1
		if 'Ithaca!1313' in row:
			print(str(counter) + ": Skipping homestead with bad URLS")
			skip += 1
			continue
		filename,stub,capture,regex,numdates,toplevel = row.strip().split(',')
		URL = filename[14:].lower() #Set URL identifier as lowercase for reduction but leave filename unchanged for reference later
		print(str(counter) + ": Processing listing for " + filename)
		
		# Initialized homestead dictionary
		if stub not in fileDict:
			fileDict[stub] = dict()
		
		# Initialize dictionary for relative URL
		if URL not in fileDict[stub]:
			fileDict[stub][URL] = dict()
			fileDict[stub][URL]['capdates'] = set()
			fileDict[stub][URL]['regdates'] = set()
			fileDict[stub][URL]['filelist'] = list()
			# toplevel should be same for all listings of same URL, so just set once 
			if toplevel == 'Y':
				fileDict[stub][URL]['toplevel'] = True
			else:
				fileDict[stub][URL]['toplevel'] = False
		
		if regex != '<blank>':
			fileDict[stub][URL]['regdates'] = fileDict[stub][URL]['regdates'].union(regex.split(';'))
		fileDict[stub][URL]['capdates'] = fileDict[stub][URL]['capdates'].union(capture.split(';'))
		fileDict[stub][URL]['filelist'].append(filename)

print("Skipped: " + str(skip))
print("Writing to disk as " + outfile)
with open(outfile,mode='w',encoding='utf-8') as file:
	for stub in sorted(fileDict.keys()):
		for URL in sorted(fileDict[stub].keys()):
			if len(fileDict[stub][URL]['regdates']) > 0:
				regdates = ';'.join(sorted(fileDict[stub][URL]['regdates']))
			else:
				regdates = "<blank>"
			capdates = ';'.join(sorted(fileDict[stub][URL]['capdates']))
			filelist = ';'.join(sorted(fileDict[stub][URL]['filelist']))
			if fileDict[stub][URL]['toplevel']:
				toplevel = 'Y'
			else:
				toplevel = 'N'
			file.write(','.join([stub,URL,capdates,regdates,toplevel,filelist]) + '\n')