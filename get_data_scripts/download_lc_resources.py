import glob
from pathlib import Path
import ujson
import os
import requests

lc_data_dir = f"{str(Path.home())}/data/swib_data/lc_entities/"

lc_resource_subject_of_data_dir = f"{str(Path.home())}/data/swib_data/lc_subject_of/"
lc_resource_contributor_to_data_dir = f"{str(Path.home())}/data/swib_data/lc_contributor_to/"


sub_counter = 0
con_counter = 0
for file in glob.glob(f"{lc_data_dir}*.json"):

	try:
		data = ujson.load(open(file))
	except ValueError:
		print('bad data:',file)

	lccn = file.split('/')[-1].replace('.json','')

	label = None
	# it is not from the dump file
	if type(data) is list:


		for g in data:

			if "@id" in g:
				if '/authorities/' in g['@id'] and f"/{lccn}" in g['@id']:
					if 'http://www.loc.gov/mads/rdf/v1#authoritativeLabel' in g:
						label = g['http://www.loc.gov/mads/rdf/v1#authoritativeLabel'][0]['@value']


	# it is
	else:

		if '@graph' in data:
			for g in data['@graph']:
				if '/authorities/' in g['@id'] and f"/{lccn}" in g['@id']:
					if 'madsrdf:authoritativeLabel' in g:
						try:
							if type(g['madsrdf:authoritativeLabel']) is str:
								label = g['madsrdf:authoritativeLabel']
							else:
								label = g['madsrdf:authoritativeLabel']['@value']
						except TypeError:
							continue



	if label != None:
		if lccn[0] == 'n':
			file = f"{lc_resource_contributor_to_data_dir}{lccn}.json"
			con_counter+=1
			if not os.path.exists(file):
				params = {
					'label' : label
				}
				headers = {
					'Accept' : 'application/json',
					'User-Agent': 'It\'s Matt - Gathering DATATATA '
				}

				r = requests.get('https://id.loc.gov/resources/works/relationships/contributorto/', params=params, headers=headers)

				with open(file,'w') as out:
					out.write(r.text)



			file = f"{lc_resource_subject_of_data_dir}{lccn}.json"
			sub_counter+=1
			if not os.path.exists(file):
				params = {
					'label' : label
				}
				headers = {
					'Accept' : 'application/json',
					'User-Agent': 'It\'s Matt - Gathering DATATATA '
				}

				r = requests.get('https://id.loc.gov/resources/works/relationships/subjectof/', params=params, headers=headers)

				with open(file,'w') as out:
					out.write(r.text)





		else:

			file = f"{lc_resource_subject_of_data_dir}{lccn}.json"
			sub_counter+=1
			if not os.path.exists(file):
				params = {
					'label' : label
				}
				headers = {
					'Accept' : 'application/json',
					'User-Agent': 'It\'s Matt - Gathering DATATATA '
				}

				r = requests.get('https://id.loc.gov/resources/works/relationships/subjectof/', params=params, headers=headers)

				with open(file,'w') as out:
					out.write(r.text)


	print(f"sub: {sub_counter} con: {con_counter}")

	# if label != None:
	# 	print(label)
	# if data['@context']:

	# 	pass
	# else:

	# 	print(file)