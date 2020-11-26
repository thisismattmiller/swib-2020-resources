import glob
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
import csv


reports_dir = f"{str(Path.home())}/data/swib_data/load_reports/"
viz_data_dir = f"{str(Path.home())}/data/swib_data/viz_data_source/"

all_reports = {}
for file in glob.glob(f"{reports_dir}*.xml"):

	with open(file) as infile:
		print(file)
		xml = ET.fromstring(infile.read())

		datestr = xml.attrib['start'].split(' ')[0]
		date = datetime(int(datestr.split('-')[0]), int(datestr.split('-')[1]), int(datestr.split('-')[2]))
		timestmp = int(date.timestamp())

		all_reports[timestmp] = {
			'newNAF' : 0,
			'unlinkNAF' : 0,
			'linkChangedNAF' : 0,
			'labelChangedNAF' : 0,
			'newLCSH' : 0,
			'unlinkLCSH' : 0,
			'linkChangedLCSH' : 0,
			'labelChangedLCSH' : 0,
			'date' : datestr,
			'dateStamp' : timestmp
		}

		details_el = xml.find('{info:lc/lds-id/log}logDetails')

		for el in details_el:

			if el.attrib['action'] == 'partialUnlink':
				if  el.attrib['lccn'][0] == 'n':
					all_reports[timestmp]['linkChangedNAF']+=1
				elif el.attrib['lccn'][0] == 's':
					all_reports[timestmp]['linkChangedLCSH']+=1

			if el.attrib['action'] == 'unlink':
				if  el.attrib['lccn'][0] == 'n':
					all_reports[timestmp]['unlinkNAF']+=1
				elif el.attrib['lccn'][0] == 's':
					all_reports[timestmp]['unlinkLCSH']+=1


			if el.attrib['action'] == 'new':
				if  el.attrib['lccn'][0] == 'n':
					all_reports[timestmp]['newNAF']+=1
				elif el.attrib['lccn'][0] == 's':
					all_reports[timestmp]['newLCSH']+=1


			if el.attrib['action'] == 'labelChange':
				if  el.attrib['lccn'][0] == 'n':
					all_reports[timestmp]['labelChangedNAF']+=1
				elif el.attrib['lccn'][0] == 's':
					all_reports[timestmp]['labelChangedLCSH']+=1




with open(f"{viz_data_dir}report_hisogram.csv",'w') as out:

	writer = csv.writer(out)

	writer.writerow(['Date','New NAF','Unlink NAF', 'Link Change NAF', 'Label Change NAF','New LCSH','Unlink LCSH', 'Link Change LCSH', 'Label Change LCSH'])


	for t in sorted(list(all_reports.keys())):
		writer.writerow([all_reports[t]['date'],all_reports[t]['newNAF'],all_reports[t]['unlinkNAF'], all_reports[t]['linkChangedNAF'], all_reports[t]['labelChangedNAF'],all_reports[t]['newLCSH'],all_reports[t]['unlinkLCSH'], all_reports[t]['linkChangedLCSH'], all_reports[t]['labelChangedLCSH']])


# json.dump(all_reports,open(f"{viz_data_dir}report_hisogram.json",'w'),indent=2)



