import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('PLANTNET_API_KEY')
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"


def plantnet_id(images, *organs):

    # a list of accepted organs that can be used as arguments
    accepted_organs = ['flower', 'leaf', 'bark', 'fruit']

    # create dict of params for requests.get()
    payload = {'images':[], 'organs':[]}

    # add params to dict for requests.get()
    for image in images:
        payload['images'].append(image)
    for organ in organs:
        if organ in accepted_organs:
            payload['organs'].append(organ)
        else:
            payload['organs'].append('auto')      # argument defaults to 'flower' if incorrect or omitted
    
    # send request to API as a url and return as JSON
    req = requests.get(api_endpoint, params=payload)
    json_data = json.loads(req.text)

    # format output
    results_list = []
    
    for result in json_data['results']:
        d= {
            "Score": result['score'],
            "Scientific Name": result['species']['scientificNameWithoutAuthor'],
            "Genus": result['species']['genus']['scientificNameWithoutAuthor'],
            "Family": result['species']['family']['scientificNameWithoutAuthor'],
            "Common Names": result['species']['commonNames'],
            # "GBIF": result['gbif'].get('id')
        }
        d['GBIF'] = result['gbif'].get('id') if result['gbif'] else ""

        results_list.append(d)

    return results_list