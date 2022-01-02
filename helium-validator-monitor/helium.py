import requests, logger
from retrying import retry

logger = logger.get_logger(__name__)

BASE_URL = "https://api.helium.io/v1/validators"

@retry(wait_exponential_multiplier=5000, wait_exponential_max=60000)
def get_validator_status(validator_address):
    """
    Get the current status of a validator
    """

    url = f'{BASE_URL}/{validator_address}'
    response = requests.get(url, headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15'})

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error("Error getting validator status: {}".format(e))
        raise e

    return response.json()['data']['status']['online']