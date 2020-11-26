import requests
import ujson
from pathlib import Path



wikidata_data_file = f"{str(Path.home())}/data/swib_data/wikidata_entities.ndjson"
viz_data_dir = f"{str(Path.home())}/data/swib_data/viz_data_source/"
wikidata_labels = ujson.load(open(f"{str(Path.home())}/data/swib_data/wikidata_labels.json"))


all_label_count = {}

c=0
with open(wikidata_data_file) as infile:
	for line in infile:
		c+=1
		if c % 1000 == 0:
			print(c, len(all_label_count))

		data = ujson.loads(line)
		qid = list(data['entities'].keys())[0]


		label_count = len(list(data['entities'][qid]['labels'].keys()))

		if label_count not in all_label_count:
			all_label_count[label_count]=0

		all_label_count[label_count]+=1



print('all links',c)
all_data = []
for k in all_label_count:
	all_data.append({'label_count':k,'count':all_label_count[k], 'percent': all_label_count[k]/c *100})			

all_data = sorted(all_data, key = lambda i: i['count'], reverse=True)
ujson.dump(all_data,open(f"{viz_data_dir}wiki_label_count.json",'w'),indent=2)
