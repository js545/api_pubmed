# DONE Import papers and affiliations for a given keyword
# TODO Classify papers by affiliation
# TODO Generate low-level node/connection relationships
# TODO Map onto Google Maps using JavaScript API

import gmaps
import numpy as np
import pandas as pd
from Bio import Entrez

Entrez.email = 'jake.son@childmind.org'

_term = input('What is your search term?: ')

links = Entrez.esearch(db='pubmed', retmax=100, term=_term)
pubmed_ids = Entrez.read(links)['IdList']

affils = []

for pubmed_id in pubmed_ids:

    try:

        handle = Entrez.efetch(db='pubmed', id=pubmed_id, retmode='xml', rettype='full')
        record = Entrez.read(handle)
        handle.close()
        title = record['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle']
        journal = record['PubmedArticle'][0]['MedlineCitation']['Article']['Journal']
        abstract = record['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']
        authors = record['PubmedArticle'][0]['MedlineCitation']['Article']['AuthorList']

        # Get author affiliations
        for author in range(len(authors)):
            affils.append(
                record['PubmedArticle'][0]['MedlineCitation']['Article']['AuthorList'][int(author)]['AffiliationInfo'][
                    0][
                    'Affiliation'])

    except:

        print(str('There was an issue with this article: pubmed_id={}').format(pubmed_id))

# State affiliation names associated with a medical school
df = pd.read_csv('school_locations.csv')
# TODO Need to include way of including school nicknames such as UCSD for UC San Diego

# Load school latitude/longitude information
lats = []
longs = []

for result in affils:

    for med_school in df.itertuples():

        if med_school.school in result:
            lats.append(med_school.latitude)
            longs.append(med_school.longitude)
            pass
        # TODO Need a way to prevent repeat counts of school (some are similarly named or have two locations)

school_locations = np.array(list(zip(lats, longs)))

# Configure gmaps
gmaps.configure(api_key='AIzaSyB2u_61XI0NgxfDes3S0vfk7-teEHvOAac')

US_coordinates = (38.5, -95.5)
fig = gmaps.figure(center=US_coordinates, zoom_level=4)
heatmap_layer = gmaps.heatmap_layer(school_locations)
heatmap_layer.point_radius = 10
heatmap_layer.max_intensity = 5
# TODO both the radius and intensity must scale with # papers
fig.add_layer(heatmap_layer)
fig
