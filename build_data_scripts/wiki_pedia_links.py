import requests
import ujson
from pathlib import Path



wikidata_data_file = f"{str(Path.home())}/data/swib_data/wikidata_entities.ndjson"
viz_data_dir = f"{str(Path.home())}/data/swib_data/viz_data_source/"


all_pedia = {'nolink':0}

c=0
with open(wikidata_data_file) as infile:
	for line in infile:
		c+=1
		if c % 1000 == 0:
			print(c, len(all_pedia))

		data = ujson.loads(line)
		qid = list(data['entities'].keys())[0]


		for k in data['entities'][qid]['sitelinks'].keys():
			if k not in all_pedia:
				all_pedia[k] = 0

			all_pedia[k]+=1


		if len(list(data['entities'][qid]['sitelinks'].keys())) == 0:
			all_pedia['nolink']+=1
			

print('all links',c)
all_data = []
for k in all_pedia:
	all_data.append({'wiki':k,'count':all_pedia[k], 'percent': all_pedia[k]/c *100})			

all_data = sorted(all_data, key = lambda i: i['count'], reverse=True)
ujson.dump(all_data,open(f"{viz_data_dir}wiki_site_links.json",'w'),indent=2)
