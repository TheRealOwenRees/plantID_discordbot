import json
import requests

from bs4 import BeautifulSoup
from settings import base_url, headers, SCORE_LOWER_THRESHOLD, ALTERNATIVE_SCORE_LOWER_THRESHOLD


def plantnet_response(images):
    """
    Send images (Discord cached URLs) to PlantNet API for processing
    :param images: {'images': [], 'organs': []}
    :return: results_list: list of dicts
    """
    results_list = []
    payload = {'images': [], 'organs': []}

    for image in images:
        payload['images'].append(image)
        payload['organs'].append('auto')  # TODO test if this part of the payload can be omitted

    req = requests.get(base_url, params=payload)
    if req.status_code == 200:
        json_data = json.loads(req.text)

        for result in json_data['results']:
            results_list.append(
                {
                    "Score": result['score'], "Scientific Name": result['species']['scientificNameWithoutAuthor'],
                    "Genus": result['species']['genus']['scientificNameWithoutAuthor'],
                    "Family": result['species']['family']['scientificNameWithoutAuthor'],
                    "Common Names": result['species']['commonNames'],
                    "GBIF": result['gbif'].get('id') if result['gbif'] else ""
                })
    return results_list


def pfaf_plant_exists(url):
    """
    Returns a boolean indicating if the latin name is found on the PFAF website
    :param url: https://pfaf.org/user/Plant.aspx?LatinName= + Scientific+Name
    :return: boolean
    """
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        latin_name = soup.find('span', id='ContentPlaceHolder1_lbldisplatinname')
        if latin_name.text:
            return True


def get_common_names_str(response):
    if response[0]['Common Names']:
        return "Common names include " + "**" + ", ".join(str(elem) for elem in response[0]['Common Names']) + "**."
    else:
        return "No common names were found."


def get_alternatives_list(response):
    alternatives_list = []
    for result in response[1:]:
        score = format(result['Score'] * 100, ".0f")
        if int(score) >= ALTERNATIVE_SCORE_LOWER_THRESHOLD:
            alternatives_list.append(result['Scientific Name'] + " (" + score + "%)")
    return alternatives_list


def get_alternatives_str(alternatives_list):
    if alternatives_list:
        return "Alternatives include: " + "*" + ", ".join(str(elem) for elem in alternatives_list) + "*."
    else:
        return "No alternatives were found."


def process_response(attachments):
    """
    Process the response from PlantNet API, returning a string to be sent to the user depending on the score
    :param attachments: image attachments from ApplicationContext
    :return: string
    """
    response = plantnet_response(attachments)

    plant_score = format(response[0]['Score'] * 100, ".0f")
    if int(plant_score) < SCORE_LOWER_THRESHOLD:
        return "I'm not sure what this is. Please try again with:\n- a clearer image\n- photos of multiple organs\n- " \
               "pictures higher than 600x600px"

    alternatives_list = get_alternatives_list(response)
    alternatives_str = get_alternatives_str(alternatives_list)
    common_names_str = get_common_names_str(response)

    gbif_url = "https://www.gbif.org/species/" + response[0]['GBIF']
    gbif_str = f"<{gbif_url}>\n\n" if response[0]['GBIF'] else ""

    pfaf_url = "https://pfaf.org/user/Plant.aspx?LatinName=" + response[0]['Scientific Name'].replace(" ", "+")
    pfaf_str = f"<{pfaf_url}>\n\n" if pfaf_plant_exists(pfaf_url) else ""

    result_str = (f"My best guess is ***{response[0]['Scientific Name']}*** with {response[0]['Score'] * 100:.0f}% "
                  f"confidence. {common_names_str} For more information visit:\n{pfaf_str}{gbif_str}{alternatives_str}")

    return result_str
