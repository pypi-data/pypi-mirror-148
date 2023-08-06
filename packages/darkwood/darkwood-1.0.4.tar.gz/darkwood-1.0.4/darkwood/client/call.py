import requests
import json
import pprint
import os

root_path = os.path.expanduser("~")


def read_creds():
    folder = os.path.join(root_path, '.darkwood', 'credentials.txt')
    try:
        with open(folder, 'r') as credentials_file:
            credentials_line = credentials_file.readline()
            credentials = credentials_line.strip(' ').strip('\n').split('=')[1]
            return credentials
    except Exception as e:
        raise RuntimeError("Darkwood credentials file incorrectly formatted. "
                           "Please re-run darkwood-data configure cli to rectify")


def credit_card_mapper(transaction, creds=''):
    if not creds:
        creds = read_creds()
    endpoint = "https://api.darkwood.tech/link"
    params = {'transaction_string': transaction}
    result = requests.get(endpoint, params=params, headers={'x-api-key': creds})
    return json.loads(result.content.decode("utf-8"))