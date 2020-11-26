import requests
import ujson
from pathlib import Path



lc_data_file = f"{str(Path.home())}/data/swib_data/lc_entities.ndjson"
viz_data_dir = f"{str(Path.home())}/data/swib_data/viz_data_source/"


types = {}

c=0
with open(lc_data_file) as infile:
	for line in infile:
		c+=1
		if c % 1000 == 0:
			print(c, len(types))

		data = ujson.loads(line)
		use_graph = None
		if '@context' in data:
			about = data['@context']['about']

			for g in data['@graph']:
				if g['@id'] == about:
					use_graph = g


		else:
			longest = {}
			for g in data:
				if len(g) > len(longest):
					longest = g

			use_graph = longest


		for x in use_graph['@type']:

			x = x.replace('http://www.loc.gov/mads/rdf/v1#','madsrdf:')
			x = x.replace('http://www.w3.org/2004/02/skos/core#','skos:')
			x = x.replace('http://www.w3.org/2008/05/skos-xl#Label','skosxl:')


			if x not in types:
				types[x] =0

			types[x]+=1


		
print('total',c)



all_data = []
for k in types:
	all_data.append({'type':k,'count':types[k], 'percent': types[k] / c * 100})			

all_data = sorted(all_data, key = lambda i: i['count'], reverse=True)
ujson.dump(all_data,open(f"{viz_data_dir}lc_type_of.json",'w'),indent=2)
