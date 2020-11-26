import requests
import ujson
from pathlib import Path



wikidata_data_file = f"{str(Path.home())}/data/swib_data/wikidata_entities.ndjson"
viz_data_dir = f"{str(Path.home())}/data/swib_data/viz_data_source/"
wikidata_labels = ujson.load(open(f"{str(Path.home())}/data/swib_data/wikidata_labels.json"))


all_claims = {}

c=0
with open(wikidata_data_file) as infile:
	for line in infile:
		c+=1
		if c % 1000 == 0:
			print(c, len(all_claims))

		data = ujson.loads(line)
		qid = list(data['entities'].keys())[0]

		for claim in data['entities'][qid]['claims']:

			if data['entities'][qid]['claims'][claim][0]['mainsnak']['datatype'] != 'external-id':
				if claim not in all_claims:
					all_claims[claim] = {'label':wikidata_labels[claim],'count':0,'p':claim}

				all_claims[claim]['count']+=1



print('all count',c)
all_data = []
for k in all_claims:
	all_data.append({'p':k,'count':all_claims[k]['count'], 'label': all_claims[k]['label'] ,'percent': round(all_claims[k]['count']/c *100,2)})			

all_data = sorted(all_data, key = lambda i: i['count'], reverse=True)
ujson.dump(all_data,open(f"{viz_data_dir}wiki_claims_count.json",'w'),indent=2)

with open(f"{viz_data_dir}wiki_claims_count.csv",'w') as out:
	for d in all_data:

		out.write(f"{d['label']} ({d['p']}),{d['count']},{d['percent']}\n")