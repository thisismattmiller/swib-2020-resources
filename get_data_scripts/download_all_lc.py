import requests
import ujson
from pathlib import Path
import os

"""
This script uses the bulk download file to pull out any NAF/LCSH records that are
on wikidata. It then usese id.loc.gov to download any missing from the bulk file (created after the file was cut)
"""


lc_data_dir = f"{str(Path.home())}/data/swib_data/lc_entities/"
lc_data_dump_naf = f"{str(Path.home())}/Downloads/lcnaf.both.ndjson"
lc_data_dump_lcsh = f"{str(Path.home())}/Downloads/lcsh.both.ndjson"


url = "https://query.wikidata.org/sparql"


sparql = """
	SELECT ?item ?o 
	WHERE 
	{
	  ?item wdt:P244 ?o.
	}
"""

params = {
	'query' : sparql
}

headers = {
	'Accept' : 'application/json',
	'User-Agent': 'USER thisismattmiller - Data Analysis '
}

r = requests.get(url, params=params, headers=headers)

data = ujson.loads(r.text)

all_p244 = []
lccns={}

for result in data['results']['bindings']:
	all_p244.append({'q':result['item']['value'].split("/")[-1], 'lccn':result['o']['value']})
	lccns[result['o']['value']] = True

wrote_out = 0

print("LCNAF")
with open(lc_data_dump_naf) as infile:
	for line in infile:
		d = ujson.loads(line)
		lccn = d['@context']['about'].split('/')[-1]
		if lccn in lccns:
			wrote_out+=1
			print(wrote_out)
			ujson.dump(d,open(f"{lc_data_dir}{lccn}.json",'w'))

print("LCSH")
with open(lc_data_dump_lcsh) as infile:
	for line in infile:
		d = ujson.loads(line)
		lccn = d['@context']['about'].split('/')[-1]
		if lccn in lccns:
			wrote_out+=1
			print(wrote_out)
			ujson.dump(d,open(f"{lc_data_dir}{lccn}.json",'w'))



headers = {
	'Accept' : 'application/json',
	'User-Agent': 'It\'s Matt - Doing data gathering for SWIB2020 presentation'
}

for entitiy in all_p244:

	file = f"{lc_data_dir}{entitiy['lccn'].split('/')[-1]}.json"


	if not os.path.exists(file):

		url = f"https://id.loc.gov/authorities/{entitiy['lccn']}.json"

		r = requests.get(url, headers=headers)
		try:
			with open(file,'w') as out:
				out.write(r.text)
		except:
			print('error:',file)

	else:
		print(f'skip {file}')

