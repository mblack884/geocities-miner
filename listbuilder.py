datafile = 'uniqueurls.csv'
outfile = 'processlist.csv'

'''

'''

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