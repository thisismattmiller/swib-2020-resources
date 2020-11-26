import requests
import ujson
from pathlib import Path



wikidata_data_file = f"{str(Path.home())}/data/swib_data/wikidata_entities.ndjson"
wikidata_labels = ujson.load(open(f"{str(Path.home())}/data/swib_data/wikidata_labels.json"))
viz_data_dir = f"{str(Path.home())}/data/swib_data/viz_data_source/"


all_P31 = {}

c=0
with open(wikidata_data_file) as infile:
	for line in infile:
		c+=1
		if c % 1000 == 0:
			print(c, len(all_P31))

		data = ujson.loads(line)
		qid = list(data['entities'].keys())[0]

		# get the instance of
		if 'P31' in data['entities'][qid]['claims']:
			for p31 in data['entities'][qid]['claims']['P31']:
				if 'datavalue' in p31['mainsnak']:
					if p31['mainsnak']['datavalue']['value']['id'] not in all_P31:
						all_P31[p31['mainsnak']['datavalue']['value']['id']]=0
					all_P31[p31['mainsnak']['datavalue']['value']['id']]+=1

		if c % 100000 == 0:

			all_data = []
			for k in all_P31:
				all_data.append({'q':k,'label':wikidata_labels[k],'count':all_P31[k]})			

			all_data = sorted(all_data, key = lambda i: i['count'], reverse=True)
			ujson.dump(all_data,open(f"{viz_data_dir}wiki_instance_of.json",'w'),indent=2)
			


all_data = []
for k in all_P31:
	all_data.append({'q':k,'label':wikidata_labels[k],'count':all_P31[k]})			

all_data = sorted(all_data, key = lambda i: i['count'], reverse=True)
ujson.dump(all_data,open(f"{viz_data_dir}wiki_instance_of.json",'w'),indent=2)
