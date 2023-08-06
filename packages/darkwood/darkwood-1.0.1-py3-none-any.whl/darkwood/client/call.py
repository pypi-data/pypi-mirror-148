import requests
import json
import pprint


def credit_card_mapper(transaction):
    endpoint = "https://api.darkwood.tech/link"
    params = {'transaction_string': transaction}
    result = requests.get(endpoint, params=params)
    return json.loads(result.content.decode("utf-8"))