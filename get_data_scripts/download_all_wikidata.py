import requests
import json
from pathlib import Path
import os


wikidata_data_dir = f"{str(Path.home())}/data/swib_data/wikidata_entities/"

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

data = json.loads(r.text)

all_p244 = []

for result in data['results']['bindings']:
	all_p244.append({'q':result['item']['value'].split("/")[-1], 'lccn':result['o']['value']})


for entitiy in all_p244:

	file = f"{wikidata_data_dir}{entitiy['q']}.json"

	try:

		if not os.path.exists(file):

			url = f"https://www.wikidata.org/wiki/Special:EntityData/{entitiy['q']}.json"

			r = requests.get(url, headers=headers)

			with open(file,'w') as out:
				out.write(r.text)

		else:
			print(f'skip {file}')
			
	except:
		
		continue


