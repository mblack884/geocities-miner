Geocities Tag Miner Utilities
=======
I developed these utilities to avoid the need to download the entire 1TB archive of Geocities captured by ArchiveTeam. These scripts allow you specify a "branch" address in Geocities' directory structure and download only HTML files appearing within that branch. In practice, this means that you can selectively pull files from your "neighborhoods" of choice.

The general process is described below. Many of these steps could likely be combined in the future stages of the project.

## Data pulling

* **query.py:** This script queries the Wayback Machine's API for all captures that include the branch address in their complete URL. Working around limitations in the amount of results the API will return at a time, the script first checks to see how many "pages" of results there are and then crawls through each page, storing the results as JSONs.

* **indexer.py:** This script parses the downloaded JSONs for all URLs that the Wayback Machine has categorized as HTML files.

* **sortbydate.py:** This script reviews the index, dividing it up into smaller files by capture date (truncated to YYYYMM). Smaller indexed entries are sorted by their full capture date so from earliest to latest.

* **bigpuller.py:** This script downloads all of the files listed in the smaller indices, storing them in directories named after their truncated capture dates. If there was more than one capture performed in a month, it pulls only the earliest.

## Analysis

* **tagcounter.py:** This script parses all HTML files in a working directory and produces a vector-space model of tag counts per page.

* **wayback.py:** A small library containing tools to strip out the HTML code that the Wayback Machine injects into all of the HTML files it captures.

* **datescan.py:** This script parses the text of a page looking for dates in order to derive metadata that may better reflect the file's date of publication than Wayback's capture date.

* **datechooser.py:** The script compares all dates found on a page, identifying the earliest that falls within an acceptable range (when GeoCities was online). Ideally, this would locate things like "last updated on" or "copyright" dates. If none are found, it assigns the capture date as the file's publication date.

* **reducer.py:** An alternative date assignment tool that shares dates derived from page text among all pages within a "homestead." While not all pages to a user's homepage may have been published at the same time, the assumption here is that the date found in the text of their "index.html" file is still likely more closer to the actual date of publication than Wayback's capture date.