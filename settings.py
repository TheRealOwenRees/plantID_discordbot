import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('PLANTNET_API_KEY')

SCORE_LOWER_THRESHOLD = 30  # minimum score for a result to be considered valid
ALTERNATIVE_SCORE_LOWER_THRESHOLD = 10  # minimum score for an alternative result to be considered valid

base_url = f"https://my-api.plantnet.org/v2/identify/all?api-key={API_KEY}"

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'}
