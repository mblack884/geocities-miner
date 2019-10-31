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

def oneShot(html):
	return stripToolbar(stripAnalytics(stripArchiveStamp(html)))