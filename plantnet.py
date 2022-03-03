import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('PLANTNET_API_KEY')
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"


def plantnet_id(images, *organs):

    # a list of accepted organs that can be used as arguments
    accepted_organs = ['flower', 'leaf', 'bark', 'fruit', 'habitat', 'other']

    # create dict of params for requests.get()
    payload = {"images":[], "organs":[]}

    # add params to dict for requests.get()
    for image in images:
        payload["images"].append(image)
    for organ in organs:
        if organ in accepted_organs:
            payload["organs"].append(organ)
        else:
            payload["organs"].append('flower')
    
    # send request to API as a url and return as JSON
    req = requests.get(api_endpoint, params=payload)
    json_data = json.loads(req.text)

    # format output
    # limit to 3 results, because discord embeds have limits
    results_list = []
    
    for i in range(3):
        d= {
            "Score": json_data['results'][i]['score'],
            "Scientific Name": json_data['results'][i]['species']['scientificNameWithoutAuthor'],
            "Genus": json_data['results'][i]['species']['genus']['scientificNameWithoutAuthor'],
            "Family": json_data['results'][i]['species']['family']['scientificNameWithoutAuthor'],
            "Common Names": json_data['results'][i]['species']['commonNames'],
            "GBIF": json_data['results'][i]['gbif'].get("id")
        }
        results_list.append(d)

    return results_list