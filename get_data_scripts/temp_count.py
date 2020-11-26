import glob
from pathlib import Path

lc_data_dir = f"{str(Path.home())}/data/swib_data/lc_entities/"
lc_resource_subject_of_data_dir = f"{str(Path.home())}/data/swib_data/lc_subject_of/"
lc_resource_contributor_to_data_dir = f"{str(Path.home())}/data/swib_data/lc_contributor_to/"
wikidata_data_dir = f"{str(Path.home())}/data/swib_data/wikidata_entities/"


print('lc_data_dir:', len(list(glob.glob(f"{lc_data_dir}*.json"))))

print('lc_resource_subject_of_data_dir:', len(list(glob.glob(f"{lc_resource_subject_of_data_dir}*.json"))))


print('lc_resource_contributor_to_data_dir:', len(list(glob.glob(f"{lc_resource_contributor_to_data_dir}*.json"))))

print('wikidata_data_dir:', len(list(glob.glob(f"{wikidata_data_dir}*.json"))))


