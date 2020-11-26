import requests
import ujson
from pathlib import Path



lc_resources_contributor_to = f"{str(Path.home())}/data/swib_data/lc_resources_contributor_to.ndjson"
viz_data_dir = f"{str(Path.home())}/data/swib_data/viz_data_source/"
lc_resources_subject_of = f"{str(Path.home())}/data/swib_data/lc_resources_subject_of.ndjson"


total_contrib_to = 0


c=0
with open(lc_resources_contributor_to) as infile:
	for line in infile:
		c+=1
		if c % 1000 == 0:
			print(c, total_contrib_to)

		data = ujson.loads(line)
		
		total_contrib_to =total_contrib_to + data['summary']['total']


total_subject_of = 0


c=0
with open(lc_resources_subject_of) as infile:
	for line in infile:
		c+=1
		if c % 1000 == 0:
			print(c, total_subject_of)

		data = ujson.loads(line)
		
		total_subject_of =total_subject_of + data['summary']['total']

print('total_contrib_to',total_contrib_to)
print('total_subject_of',total_subject_of)
