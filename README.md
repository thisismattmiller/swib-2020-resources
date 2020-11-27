# swib-2020-resources
Code and data from my SWIB20 [presentation](https://github.com/thisismattmiller/swib-2020-resources/blob/main/presentation.pdf) Watch here: https://www.youtube.com/watch?v=OvcBBRZ_sUM


## Data
You are probably most intrested in the data that goes beyond that presented in the slides, the long tails, etc. Best way to view this data is from the PDF presentation, each viz has a link to the data source which has more data. But here are those links:

1 Year of ingest history: https://github.com/thisismattmiller/swib-2020-resources/blob/main/aggregate_data/report_hisogram.csv


Label Changes: https://github.com/thisismattmiller/swib-2020-resources/blob/main/aggregate_data/label_changes.json


Label Vandalism: https://github.com/thisismattmiller/swib-2020-resources/blob/main/aggregate_data/label_changes_possible_vandalism.json


Instace Of for Wikidata Items: https://github.com/thisismattmiller/swib-2020-resources/blob/main/aggregate_data/wiki_instance_of.json


RDF Type for LC authoritites: https://github.com/thisismattmiller/swib-2020-resources/blob/main/aggregate_data/lc_type_of.json


Site links for Wiki items: https://github.com/thisismattmiller/swib-2020-resources/blob/main/aggregate_data/wiki_site_links.json


Identifier links for wiki items: https://github.com/thisismattmiller/swib-2020-resources/blob/main/aggregate_data/wiki_identifier_links.json


Properties for Wiki items: https://github.com/thisismattmiller/swib-2020-resources/blob/main/aggregate_data/wiki_claims_count.json


LC Variant Labels: https://github.com/thisismattmiller/swib-2020-resources/blob/main/aggregate_data/lc_number_of_variant_labels.json


Wiki Variant Labels: https://github.com/thisismattmiller/swib-2020-resources/blob/main/aggregate_data/wiki_label_count.json



## Bulk Data
The data used to create all the information in the presentation is a subset of id.loc.gov and Wikidata. It is available as bulk new line deliminted json files:

All LC Authorties used: https://thisismattmiller.s3.amazonaws.com/swib2020/lc_entities.ndjson.gz


All Wiki Entities used: https://thisismattmiller.s3.amazonaws.com/swib2020/wikidata_entities.ndjson.gz


LC Resource Subject of: https://thisismattmiller.s3.amazonaws.com/swib2020/lc_resources_subject_of.ndjson.gz


LC Resource Contributor to: https://thisismattmiller.s3.amazonaws.com/swib2020/lc_resources_contributor_to.ndjson.gz


Download, ungzip and place them some where

## Code

The scripts in the get_data_scripts directory download the data and build the above bulk files, so no need to run these. 
The script in the build_data_scripts builds the data used in the presentation, to use these just modify where the bulk files are now located on your computer in the vairables at the top of the script.
