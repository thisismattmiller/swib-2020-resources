import requests
from pathlib import Path
import xml.etree.ElementTree as ET



reports_dir = f"{str(Path.home())}/data/swib_data/load_reports/"



r = requests.get('https://id.loc.gov/loads/extrardf/wikidata/latest.xml')


data = ET.fromstring(r.text)
errors = []
for el in data:
	if el.tag == '{info:lc/lds-id/log}stats':
		for stat in el:

			print(stat.attrib['date']) 
			url = f"https://id.loc.gov/loads/extrardf/wikidata/{stat.attrib['date']}.xml"
			print(url)
			try:
				r = requests.get(url)
			except requests.exceptions.ChunkedEncodingError:
				print('error with:', url)
				errors.append(f"wget \"{url}\"")
				continue

			if "<log" in r.text:
				with open(f"{reports_dir}{stat.attrib['date']}.xml",'w') as out:
					out.write(r.text)

			else:
				print('problems with', stat.attrib['date'])	

print("-----------")
print("Errors with these, download manually?")
for e in errors:
	print(e)
print("-----------")