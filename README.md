# helium-validator-monitor

A simple utility to monitor the status of helium validators and send notifications to discord

## Requirements

* Python 3.9
* [Pipenv](https://github.com/pypa/pipenv)

## Setup

1. Clone the repository
2. Run `pipenv install`
3. Copy `example.env` into `.env` and fill in the values
4. Copy `validators_example.yaml` into `validators.yaml` and fill in the values for your validators
5. Run `pipenv run python helium-validator-monitor/main.py`

## Issues

Look at the code