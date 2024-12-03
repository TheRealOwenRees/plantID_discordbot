import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('PLANTNET_API_KEY')
FILE_SERVER_SECRET_KEY = os.getenv('FILE_SERVER_SECRET_KEY')
FILE_SERVER_REMOTE_URL = os.getenv('FILE_SERVER_REMOTE_URL')

SCORE_LOWER_THRESHOLD = 30  # minimum score for a result to be considered valid
ALTERNATIVE_SCORE_LOWER_THRESHOLD = 10  # minimum score for an alternative result to be considered valid

api_base_url = f"https://my-api.plantnet.org/v2"
identify_api_url = f"{api_base_url}/identify/all?api-key={API_KEY}"

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36'}

FILE_SERVER_PORT = 4321
# FILE_SERVER_BASE_URL = f"http://localhost:{FILE_SERVER_PORT}"
FILE_SERVER_BASE_URL = FILE_SERVER_REMOTE_URL
FILE_SERVER_URL = f"{FILE_SERVER_BASE_URL}/plant_id"
FILE_SERVER_IMAGES_URL = f"{FILE_SERVER_BASE_URL}/plant_id"
