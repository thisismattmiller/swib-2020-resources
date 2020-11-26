import glob
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
import csv
import json
from fuzzywuzzy import fuzz


reports_dir = f"{str(Path.home())}/data/swib_data/load_reports/"
viz_data_dir = f"{str(Path.home())}/data/swib_data/viz_data_source/"

label_changes = {}
for file in glob.glob(f"{reports_dir}*.xml"):

	with open(file) as infile:
		print(file)
		xml = ET.fromstring(infile.read())

		datestr = xml.attrib['start'].split(' ')[0]
		date = datetime(int(datestr.split('-')[0]), int(datestr.split('-')[1]), int(datestr.split('-')[2]))
		timestmp = int(date.timestamp())


		details_el = xml.find('{info:lc/lds-id/log}logDetails')

		for el in details_el:

			if el.attrib['action'] == 'labelChange':

				if el.attrib['oldQ'] not in label_changes:
					label_changes[el.attrib['oldQ']] = {'q': el.attrib['oldQ'], 'lccn': el.attrib['lccn'], 'changes': []}
				

				try:
					label_old = el.text.split('changed from')[1].split('" to "')[0].replace('"','').strip().encode().decode('unicode-escape')
				except UnicodeDecodeError:
					label_old = el.text.split('changed from')[1].split('" to "')[0].replace('"','').strip()

				try:
					label_new = el.text.split('changed from')[1].split('" to "')[1].replace('"','').strip().encode().decode('unicode-escape')
				except UnicodeDecodeError:
					label_new = el.text.split('changed from')[1].split('" to "')[1].replace('"','').strip()


				
				label_changes[el.attrib['oldQ']]['changes'].append({'from':label_old,'to':label_new,'stamp':timestmp})




json.dump(label_changes,open(f"{viz_data_dir}label_changes_raw.json",'w'),indent=2)


possible_vandalism_label_changes = {}
for l in label_changes:
	
	changes_sorted = sorted(label_changes[l]['changes'], key = lambda i: i['stamp'])


	previous_from = []
	possible_vandalism = False
	for c in changes_sorted:

		c['distance'] = fuzz.token_sort_ratio(c['from'], c['to'])

		if fuzz.token_sort_ratio(c['from'], c['to']) > 90:
			# try:
			# 	print('skipping',c['from'], "->",c['to'], fuzz.token_sort_ratio(c['from'], c['to']))
			# except UnicodeEncodeError:
			# 	print('UnicodeEncodeError')
			# continue

			continue

		if c['to'] in previous_from:
			possible_vandalism = True

		previous_from.append(c['from'])


	if possible_vandalism:

	# if len(changes_sorted) > 4:

		possible_vandalism_label_changes[l] =label_changes[l]
		for c in changes_sorted:
			try:
				print(label_changes[l]['q'], datetime.utcfromtimestamp(c['stamp']).strftime('%Y-%m-%d') , c['from'], '->', c['to'])
			except UnicodeEncodeError:
				print('UnicodeEncodeError')
		print('-----')


json.dump(possible_vandalism_label_changes,open(f"{viz_data_dir}label_changes_possible_vandalism.json",'w'),indent=2)

print(len(possible_vandalism_label_changes))



# with open(f"{viz_data_dir}report_hisogram.csv",'w') as out:

# 	writer = csv.writer(out)

# 	writer.writerow(['Date','New NAF','Unlink NAF', 'Link Change NAF', 'Label Change NAF','New LCSH','Unlink LCSH', 'Link Change LCSH', 'Label Change LCSH'])


# 	for t in sorted(list(all_reports.keys())):
# 		writer.writerow([all_reports[t]['date'],all_reports[t]['newNAF'],all_reports[t]['unlinkNAF'], all_reports[t]['linkChangedNAF'], all_reports[t]['labelChangedNAF'],all_reports[t]['newLCSH'],all_reports[t]['unlinkLCSH'], all_reports[t]['linkChangedLCSH'], all_reports[t]['labelChangedLCSH']])


# # json.dump(all_reports,open(f"{viz_data_dir}report_hisogram.json",'w'),indent=2)



