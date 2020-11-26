import glob
from pathlib import Path
import ujson


data_dir = f"{str(Path.home())}/data/swib_data/"
lc_data_dir = f"{str(Path.home())}/data/swib_data/lc_entities/"
lc_resource_subject_of_data_dir = f"{str(Path.home())}/data/swib_data/lc_subject_of/"
lc_resource_contributor_to_data_dir = f"{str(Path.home())}/data/swib_data/lc_contributor_to/"
wikidata_data_dir = f"{str(Path.home())}/data/swib_data/wikidata_entities/"

# c = 0
# with open(f"{data_dir}lc_entities.ndjson", 'w') as out:

# 	print('finding lc files...')
# 	for file in glob.glob(f"{lc_data_dir}*.json"):

		
# 		with open(file) as infile:

# 			json_text = infile.read()
# 			try:
# 				data = ujson.loads(json_text)
# 			except ValueError:
# 				print('Error on',file)
# 				continue
# 			c+=1
# 			if c % 1000 == 0:
# 				print(c)

# 			out.write(ujson.dumps(data) +"\n")


# c = 0
# with open(f"{data_dir}wikidata_entities.ndjson", 'w') as out:

# 	print('finding wd files...')
# 	for file in glob.glob(f"{wikidata_data_dir}*.json"):

		
# 		with open(file) as infile:

# 			json_text = infile.read()
# 			try:
# 				data = ujson.loads(json_text)
# 			except ValueError:
# 				print('Error on',file)
# 				continue
# 			c+=1
# 			if c % 1000 == 0:
# 				print(c)

# 			out.write(ujson.dumps(data) +"\n")

c = 0
with open(f"{data_dir}lc_resources_subject_of.ndjson", 'w') as out:

	print('finding lc subject of files...')
	for file in glob.glob(f"{lc_resource_subject_of_data_dir}*.json"):

		
		with open(file) as infile:

			lccn = file.split('/')[-1].replace('.json','')

			json_text = infile.read()
			try:
				data = ujson.loads(json_text)
			except ValueError:
				print('Error on',file)
				continue

			data['lccn'] = lccn
			c+=1
			if c % 1000 == 0:
				print(c)

			out.write(ujson.dumps(data) +"\n")


c = 0
with open(f"{data_dir}lc_resources_contributor_to.ndjson", 'w') as out:

	print('finding lc subject of files...')
	for file in glob.glob(f"{lc_resource_contributor_to_data_dir}*.json"):

		
		with open(file) as infile:

			lccn = file.split('/')[-1].replace('.json','')

			json_text = infile.read()
			try:
				data = ujson.loads(json_text)
			except ValueError:
				print('Error on',file)
				continue

			data['lccn'] = lccn
			c+=1
			if c % 1000 == 0:
				print(c)

			out.write(ujson.dumps(data) +"\n")

