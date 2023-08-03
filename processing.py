import os
import json
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()  # load environment variables for test server
API_KEY = os.getenv('PLANTNET_API_KEY')
api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"

SCORE_LOWER_THRESHOLD = 30  # minimum score for a result to be considered valid
ALTERNATIVE_SCORE_LOWER_THRESHOLD = 10  # minimum score for an alternative result to be considered valid


# SEND IMAGES (Discord CACHED URLS) to PLANTNET API FOR PROCESSING
# I have removed the 'organ' argument from being passed, but kept this functionality in case I wish to bring it back
def plantnet_response(images, *organs):
    # a list of accepted organs that can be used as arguments
    accepted_organs = ['flower', 'leaf', 'bark', 'fruit']

    # create dict of params for requests.get()
    payload = {'images': [], 'organs': []}

    # add params to dict for requests.get()
    for image in images:
        payload['images'].append(image)
    for organ in organs:
        if organ in accepted_organs:
            payload['organs'].append(organ)
        else:
            payload['organs'].append('auto')  # argument default if incorrect or omitted

    # send request to API as a url and return as JSON
    req = requests.get(api_endpoint, params=payload)
    if req.status_code == 200:
        json_data = json.loads(req.text)

    # format output
    results_list = []

    for result in json_data['results']:
        d = {"Score": result['score'], "Scientific Name": result['species']['scientificNameWithoutAuthor'],
             "Genus": result['species']['genus']['scientificNameWithoutAuthor'],
             "Family": result['species']['family']['scientificNameWithoutAuthor'],
             "Common Names": result['species']['commonNames'],
             'GBIF': result['gbif'].get('id') if result['gbif'] else ""}
        results_list.append(d)
    return results_list


# SCRAPE PLANT DATA FROM PFAF.ORG WEBSITE
def pfaf_response(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'}
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        latin_name = soup.find('span', id='ContentPlaceHolder1_lbldisplatinname')
        if latin_name.text:
            return True


# accepts URLs of images and arguments for Plantnet, returning results as JSON
def process_attachments(attachments):
    response = plantnet_response(attachments)

    alternatives_list = []  # a list for all the alternative plant IDs

    plant_score = format(response[0]['Score'] * 100, ".0f")
    if int(plant_score) < SCORE_LOWER_THRESHOLD:
        return "I'm not sure what this is. Please try again with:\n- a clearer image\n- photos of multiple organs\n- " \
               "pictures higher than 600x600px"

    for result in response[1:]:
        score = format(result['Score'] * 100, ".0f")
        if int(score) >= ALTERNATIVE_SCORE_LOWER_THRESHOLD:
            alternatives_list.append(result['Scientific Name'] + " (" + score + "%)")

    # alternatives - join list as string if true
    if alternatives_list:
        alternatives_str = "Alternatives include: " + "*" + ", ".join(
            str(elem) for elem in alternatives_list) + "*."
    else:
        alternatives_str = "No alternatives were found."

    # common names - join list as string if true
    if response[0]['Common Names']:
        common_names_str = "Common names include " + "**" + ", ".join(
            str(elem) for elem in response[0]['Common Names']) + "**."
    else:
        common_names_str = "No common names were found."

    # GBIF data - create url to GBIF if id is found
    gbif_url = "https://www.gbif.org/species/" + response[0]['GBIF']
    gbif_str = f"<{gbif_url}>\n\n" if response[0]['GBIF'] else ""

    # PFAF URL - create url to PFAF if latin name is found
    pfaf_url = "https://pfaf.org/user/Plant.aspx?LatinName=" + response[0]['Scientific Name'].replace(" ", "+")
    pfaf_str = f"<{pfaf_url}>\n\n" if pfaf_response(pfaf_url) else ""

    result_str = (f"My best guess is ***{response[0]['Scientific Name']}*** with {response[0]['Score'] * 100:.0f}% "
                  f"confidence. {common_names_str} For more information visit:\n{pfaf_str}{gbif_str}{alternatives_str}")

    return result_str
