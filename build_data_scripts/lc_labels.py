import requests
import ujson
from pathlib import Path



lc_data_file = f"{str(Path.home())}/data/swib_data/lc_entities.ndjson"
viz_data_dir = f"{str(Path.home())}/data/swib_data/viz_data_source/"


var_count = {}

c=0
with open(lc_data_file) as infile:
	for line in infile:
		c+=1
		if c % 1000 == 0:
			print(c, len(var_count))

		data = ujson.loads(line)
		graphs = None
		if '@context' in data:
			about = data['@context']['about']

			graphs = data['@graph']

					


		else:
			graphs = data

		var_list = []
		for x in graphs:
			var = None
			if 'madsrdf:variantLabel' in x:
				var = x['madsrdf:variantLabel']
			if 'http://www.loc.gov/mads/rdf/v1#variantLabel' in x:
				var = x['http://www.loc.gov/mads/rdf/v1#variantLabel']
			
			
			if var != None:
				if isinstance(var, str) == True:
					var_list.append(var)
				elif isinstance(var, list):
					for v in var:

						if isinstance(v, str) == True:
							var_list.append(v)
						else:
							if '@value' in v:
								var_list.append(v['@value'])
				elif isinstance(var, dict):
					if '@value' in var:
						var_list.append(var['@value'])
				else:
					print(var)		


		if len(var_list) not in var_count:
			var_count[len(var_list)] = 0


		var_count[len(var_list)]+=1




		
print('total',c)



all_data = []
for k in var_count:
	all_data.append({'var_number':k,'count':var_count[k], 'percent': var_count[k] / c * 100})			

all_data = sorted(all_data, key = lambda i: i['count'], reverse=True)
ujson.dump(all_data,open(f"{viz_data_dir}lc_number_of_variant_labels.json",'w'),indent=2)
