'''
This script takes the list of all dates found on pages and attempts to derive a 
"first published" or "last updated" date. It checks the list of all dates found on a
given page (found via datescan.py) and looks for the earliest one within an acceptable range.

Presumably, any page including a copyright or last updated statement would have been published
to the web on or after Geocities' founding in 1995. If no date is found on the page, then the 
script falls back on the Wayback Machine's earliest capture date.

It is possible that this method may result in some false positives (e.g., a page published in
1997 by referencing events that took place in 1995 or some piece of speculative fiction that
references a future date). However, relying on the Internet Archive's capture metadata also has
significant drawbacks. The Wayback Machine began capturing pages experimentally in 1996 but didn't
officially launch until 2001. Additionally, the Internet Archive didn't begin prioritizing Geocites captures until after the company announced its closure in 2009.
'''

datafile = 'uniqueurls.csv'
outfile = 'processlist.csv'

def sortDates(dateblob):
	dateStr = dateblob.split(';')
	dateInt = list()
	for date in dateStr:
		dateInt.append(int(date))
	return sorted(dateInt)

def derivePageDate(capstr,regstr):
	capdates = sortDates(capstr)
	firstCap = capdates[0]

	# If it there are regex'd dates to check...
	if regstr != '<blank>':
		regdates = sortDates(regstr)
		for date in sorted(regdates,reverse=True):
			if date <= firstCap and date >= 1995:
				return date
	
	# If there are no regex'd dates to check or none are acceptable, fall back to first capture
	return firstCap	

capOnly = list()
regFixed = list()
counter = 0
	
with open(datafile,encoding='utf-8') as file:
	for row in file.readlines():
		counter += 1
		stub,URL,capdates,regdates,toplevel,filelist = row.strip().split(',')
		print(str(counter) + ": " + stub + " " + URL)
		date = str(derivePageDate(capdates,regdates))
		firstFile = sorted(filelist.split(';'))[0]
		with open(outfile,mode='a',encoding='utf-8') as ofile:
			ofile.write(','.join([stub,URL,date,toplevel,firstFile]) + '\n')