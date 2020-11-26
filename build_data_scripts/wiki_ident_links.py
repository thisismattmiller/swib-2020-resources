import requests
import ujson
from pathlib import Path



wikidata_data_file = f"{str(Path.home())}/data/swib_data/wikidata_entities.ndjson"
viz_data_dir = f"{str(Path.home())}/data/swib_data/viz_data_source/"
wikidata_labels = ujson.load(open(f"{str(Path.home())}/data/swib_data/wikidata_labels.json"))


all_ident_links = {}

c=0
with open(wikidata_data_file) as infile:
	for line in infile:
		c+=1
		if c % 1000 == 0:
			print(c, len(all_ident_links))

		data = ujson.loads(line)
		qid = list(data['entities'].keys())[0]

		for claim in data['entities'][qid]['claims']:


			if data['entities'][qid]['claims'][claim][0]['mainsnak']['datatype'] == 'external-id':
				label = wikidata_labels[claim]
				if claim not in all_ident_links:
					all_ident_links[claim] = {'label':wikidata_labels[claim],'count':0,'p':claim}

				all_ident_links[claim]['count']+=1



print('all links',c)
all_data = []
for k in all_ident_links:
	all_data.append({'p':k,'count':all_ident_links[k]['count'], 'label': all_ident_links[k]['label'] ,'percent': all_ident_links[k]['count']/c *100})			

all_data = sorted(all_data, key = lambda i: i['count'], reverse=True)
ujson.dump(all_data,open(f"{viz_data_dir}wiki_identifier_links.json",'w'),indent=2)
