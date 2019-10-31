import re
import os
import datetime

datadir = 'storage/'

'''
When working with a Wayback Machine copy, the following code is injected by Archive.org:
- The archive's navigation toolbar
- Analytics script
- Timestamp of capture + copyright disclaimer for injected code
- All URLs are revised to fit Wayback ecosystem (new URLs do include dating)

The navbar, analytics, and timestamps are easy to remove. The new URLs aren't necessarily a problem apart from doing the datescan. Presumably, this issue can be resolved with some smart regexing.

Current regex '(?<=\s)199\d(?!\d)'
Lookbehind checks to see that 1999 is preceeded by some kind of whitespace character.
Then checks to see if a 1990's year is present
Lookahead checks to make sure that the year is not part of a longer string of digits

Other things to keep in mind:
The variable in the toolbar "firstYear" is the display date, not the first capture

Probably the most successful capture strategy: latest date that is equal to or less than the capture date. Many pages have references to the future or past (pre-Internet years), so this will skip over both. There still might be some egregious outliers that I'll need to consider (i.e., what if they reference a historical date but have no copyright statement?)

Alternatively, create a new database to reshape based on the following scheme:

Site URL as base with the following fields
1) Capture dates
2) All regex dates
3) Any regex dates that are mentioned on index.html, main.html or stub URL

When correcting, privilege from toplevel to any page to capture

Assumptions behind this organization
- Sites are relatively stable (handcoding = static) because...
- Pre-css era of design meant that it was very timeconsuming to do full-scale redesigns
- In reviewing some examples, noted that copyright notices were not always on all pages...
- However, users seemed more likely to put a copyright date on the most top-level page

EX: http://web.archive.org/web/19990129010944/http://www.geocities.com/Athens/1059/books.html has no copyright date... (capture 1999, latest date referenced is 1995 in regards to a trip)

BUT top-level page does!
http://web.archive.org/web/19990129042654/http://www.geocities.com/Athens/1059/index.html lists 1996 as the copyright date!
'''

def stripToolbar(html):
	start = html.find('<!-- BEGIN WAYBACK TOOLBAR INSERT')
	end = html.find('END WAYBACK TOOLBAR INSERT -->')+30
	return html[:start] + html[end:]

def stripAnalytics(html):
	start = html.find('<script type="text/javascript" src="/static/js/analytics.js"')
	end = html.find('banner-styles.css"/>')+20
	return html[:start] + html[end:]
	
def stripArchiveStamp(html):
	start = html.find('<!--\n     FILE ARCHIVED ON')
	end = html.find('SECTION 108(a)(3)).\n-->')+23
	return html[:start] + html[end:]

def getStub(filename):
	address = re.findall('!\d\d\d\d!',filename)[0]
	return filename[filename.find('Athens!')+7:filename.find(address)+5]

def checkHomestead(filename):
	address = re.findall('!\d\d\d\d!',filename)
	if len(address) > 0:
		return True
	else:
		return False	
	
def getCaptureDate(filename):
	filename = filename.replace(datadir,'')
	return filename[:4]

def checkTopLevel(filename):
	if ('index.htm' in filename) or ('main.htm' in filename):
		return True
	elif len(re.findall('!\d\d\d\d!$',filename)) > 0: #check for homestead address at end of string
		return True
	else:
		return False
	
filelist = list()

start = datetime.datetime.now()
print("Starting at " + ':'.join([str(start.hour),str(start.minute),str(start.second)]))

for root,directories,filenames in os.walk(datadir):
	for filename in filenames:
		filelist.append(os.path.join(root,filename))

date90 = re.compile('(?<=\W)199\d(?!\d)')
date00 = re.compile('(?<=\W)200\d(?!\d)')

results = list()
bigDict = dict()

print("Preparing to scan for dates in " + str(len(filelist)) + " files.")

for filename in filelist:
	if not checkHomestead(filename):
		print("Skipping " + filename)
		continue
	elif "%" in filename or "#" in filename:
		continue
	print("Scanning " + filename)
	with open(filename,encoding='utf-8') as file:
		fulltext = file.read()
	
	# Derive homestead address & capture date from filename
	stub = getStub(filename)
	captureDate = getCaptureDate(filename)
	
	# Setup dictionary to store all dates for all pages + individual records
	if stub not in bigDict:
		bigDict[stub] = dict()
		bigDict[stub]['capture'] = set()
		bigDict[stub]['topdates'] = set()
		bigDict[stub]['pagedates'] = set()
		bigDict[stub]['files'] = dict()

	bigDict[stub]['capture'].add(captureDate)
		
	# Setup individual page record
	if filename not in bigDict[stub]['files']:
		bigDict[stub]['files'][filename] = dict()
		bigDict[stub]['files'][filename]['capture'] = captureDate
		bigDict[stub]['files'][filename]['pagedates'] = set()
	
	# Get all years that match 199X or 200X
	stripped = stripArchiveStamp(stripAnalytics(stripToolbar(fulltext)))	
	dates = re.findall(date90,stripped) + re.findall(date00,stripped)

	bigDict[stub]['pagedates'] = bigDict[stub]['pagedates'].union(set(dates))
	bigDict[stub]['files'][filename]['pagedates'] = set(dates)
	
	if checkTopLevel(filename):
		bigDict[stub]['topdates'] = bigDict[stub]['topdates'].union(set(dates))

end = datetime.datetime.now()
total = end - start
minutes,seconds = divmod(total.seconds,60)

print("Started at " + ':'.join([str(start.hour),str(start.minute),str(start.second)]))
print("Finished at " + ':'.join([str(end.hour),str(end.minute),str(end.second)]))
print("Scanning took " + str(minutes) + " minutes and " + str(seconds) + " seconds.")
		
print("Writing results for homesteads to disk.")	
with open('stubdates.csv',mode='w',encoding='utf-8') as file:
	for stub in sorted(bigDict.keys()):
		captures = ';'.join(sorted(bigDict[stub]['capture']))
		if len(bigDict[stub]['topdates']) > 0:
			topdates = ';'.join(sorted(bigDict[stub]['topdates']))
		else:
			topdates = '<blank>'
		if len(bigDict[stub]['pagedates']) > 0:
			pagedates = ';'.join(sorted(bigDict[stub]['pagedates']))
		else:
			pagedates = '<blank>'
		file.write(','.join([stub,captures,str(len(bigDict[stub]['capture'])),topdates,str(len(bigDict[stub]['topdates'])),pagedates,str(len(bigDict[stub]['pagedates']))]) + '\n')

print("Writing results for all pages to disk.")
with open('fulldates.csv',mode='w',encoding='utf-8') as file:
	for stub in sorted(bigDict.keys()):
		for filename in sorted(bigDict[stub]['files'].keys()):
			if len(bigDict[stub]['files'][filename]['pagedates']) > 0:
				pagedates = ';'.join(sorted(bigDict[stub]['files'][filename]['pagedates']))
			else:
				pagedates = '<blank>'
			if checkTopLevel(filename):
				top = 'Y'
			else:
				top = 'N'
			file.write(','.join([filename.replace('\\','/').replace(datadir,''),stub,bigDict[stub]['files'][filename]['capture'],pagedates,str(len(bigDict[stub]['files'][filename]['pagedates'])),top]) + '\n')