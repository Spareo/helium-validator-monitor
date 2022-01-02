import time, yaml, logger, schedule
from helium import get_validator_status
from dotenv import load_dotenv
from os import path, getenv
from discord import send_status_message

load_dotenv()
STATUS_CHECK_DELAY_SECONDS = int(getenv('STATUS_CHECK_DELAY_SECONDS'))
PERIODIC_CHECK_DELAY_MINUTES = int(getenv('PERIODIC_CHECK_DELAY_MINUTES'))
ENABLE_PERIODIC_CHECK = bool(getenv('ENABLE_PERIODIC_CHECK'))

log = logger.get_logger(__name__)
validators = None
log.info('Validator status will be checked every {} seconds'.format(STATUS_CHECK_DELAY_SECONDS))

def get_validators():
    """
    Load the validators from the validtors.yaml file and return them as a list.
    """

    basepath = path.dirname(__file__)
    filepath = path.abspath(path.join(basepath, "..", "validators.yaml"))
    log.debug("Loading validators from {}".format(filepath))

    with open(filepath, 'r') as f:
        data = yaml.full_load(f)

        for validator in data['validators']:
            validator['explorer'] = f'https://explorer.helium.com/validators/{validator["address"]}'

        global validators
        validators = data['validators']


def periodic_check():
    """
    Periodically does a status check and always sends a message
    to discord, regardless of what the status is
    """
    
    log.debug("Executing periodic check")
    check_status(is_periodic=True)

def check_status(is_periodic=False):
    """
    Check the status of each validator and send a message to discord if it is offline.
    """

    try:
        if validators is None:
            get_validators()

        for validator in validators:
            name = validator['name']
            explorer = validator['explorer']
            status = get_validator_status(validator['address'])

            if is_periodic:
                send_status_message(name, explorer, status)
            elif status != 'online':
                log.warn("Validator {} is offline".format(name))
                send_status_message(name, explorer, status)
            else: 
                log.info("Validator {} is online".format(validator['name']))

    except Exception:
        log.exception("Error checking validator status")

# Schedule status check
schedule.every(STATUS_CHECK_DELAY_SECONDS).seconds.do(check_status)

# Schedule periodic check only if enabled
if ENABLE_PERIODIC_CHECK:
    schedule.every(PERIODIC_CHECK_DELAY_MINUTES).minutes.do(periodic_check)

while True:
    schedule.run_pending()
    time.sleep(1)