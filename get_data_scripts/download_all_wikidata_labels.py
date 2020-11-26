import requests
import ujson
from pathlib import Path



wikidata_data_file = f"{str(Path.home())}/data/swib_data/wikidata_entities.ndjson"
wikidata_data_label_file = f"{str(Path.home())}/data/swib_data/wikidata_labels.json"
wikidata_data_label_dir = f"{str(Path.home())}/data/swib_data/wikidata_labels/"

all_ids = {}

c=0
with open(wikidata_data_file) as infile:


	for line in infile:

		c+=1
		if c % 1000 == 0:
			print(c, len(all_ids))

		data = ujson.loads(line)
		qid = list(data['entities'].keys())[0]

		# get the P used
		for p in data['entities'][qid]['claims']:
			if p not in all_ids:
				all_ids[p] = True

		# get the instance of
		if 'P31' in data['entities'][qid]['claims']:
			for p31 in data['entities'][qid]['claims']['P31']:
				if 'datavalue' in p31['mainsnak']:
					all_ids[p31['mainsnak']['datavalue']['value']['id']] = True

	


# download the labels

headers = {
	'Accept' : 'application/json',
	'User-Agent': 'USER thisismattmiller - Data Analysis '
}
c=0
for a_id in all_ids:

	url = f"https://www.wikidata.org/wiki/Special:EntityData/{a_id}.json"

	r = requests.get(url, headers=headers)

	data = ujson.loads(r.text)
	qid = list(data['entities'].keys())[0]


	# save it for later just in case	
	with open(f"{wikidata_data_label_dir}{qid}.json",'w') as out:
		out.write(r.text)

	label = None
	# see if there is an en label, otherwise grab the first one
	if 'en' in data['entities'][qid]['labels']:
		label = data['entities'][qid]['labels']['en']['value']
	else:
		first_key = list(data['entities'][qid]['labels'].keys())[0]
		label = data['entities'][qid]['labels'][first_key]['value']
		print("---No EN label -----")
		print(url)
		print(label)


	all_ids[a_id] = label

	c+=1
	if c % 100 == 0:
		print(c, '/', len(all_ids))
		ujson.dump(all_ids,open(wikidata_data_label_file,'w'),indent=2)


ujson.dump(all_ids,open(wikidata_data_label_file,'w'),indent=2)

# url = "https://query.wikidata.org/sparql"


# sparql = """
# 	SELECT ?item ?o 
# 	WHERE 
# 	{
# 	  ?item wdt:P244 ?o.
# 	}
# """

# params = {
# 	'query' : sparql
# }

# headers = {
# 	'Accept' : 'application/json',
# 	'User-Agent': 'USER thisismattmiller - Data Analysis '
# }

# r = requests.get(url, params=params, headers=headers)

# data = json.loads(r.text)

# all_p244 = []

# for result in data['results']['bindings']:
# 	all_p244.append({'q':result['item']['value'].split("/")[-1], 'lccn':result['o']['value']})


# for entitiy in all_p244:

# 	file = f"{wikidata_data_dir}{entitiy['q']}.json"

# 	try:

# 		if not os.path.exists(file):

# 			url = f"https://www.wikidata.org/wiki/Special:EntityData/{entitiy['q']}.json"

# 			r = requests.get(url, headers=headers)

# 			with open(file,'w') as out:
# 				out.write(r.text)

# 		else:
# 			print(f'skip {file}')
			
# 	except:
		
# 		continue


