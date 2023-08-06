""" darkwood v1.0.0
"""
# Standard library imports
import os
import sys
import argparse
import os
from darkwood.client.call import credit_card_mapper

root_path = os.path.expanduser("~")
parser = argparse.ArgumentParser(prog='Darkwood Data', description='Utilize Darkwood')


def main() -> None:
    subparsers = parser.add_subparsers()
    parser_a = subparsers.add_parser('configure')
    parser_a.add_argument('cli', type=str)
    parser_b = subparsers.add_parser('entity-mapper')
    parser_b.add_argument('--transaction', type=str, help='Transaction to be mapped')
    args = parser.parse_args()
    dict_args = vars(args)
    if dict_args.get('cli'):
        set_credentials_file()
    elif dict_args.get('transaction'):
        creds = read_creds()

        transaction = dict_args.get('transaction')
        print(credit_card_mapper(transaction=transaction, creds=creds))


def set_credentials_file():
    credentials = input("Enter your Darkwood provided API key: ")
    write_credentials_file(credentials)


def load_creds():
    # If creds don't exist ask user to create.
    if do_creds_exist():
        return read_creds()
    else:
        set_credentials_file()


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


def do_creds_exist():
    folder = os.path.join(root_path, '.darkwood','credentials.txt')
    return os.path.exists(folder)


def create_creds_dir():
    folder = os.path.join(root_path, '.darkwood')
    # Check whether the specified path exists or not
    isExist = os.path.exists(folder)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(folder)


def write_credentials_file(credentials):
    create_creds_dir()
    folder = os.path.join(root_path, '.darkwood','credentials.txt')
    with open(folder, 'w') as credentials_file:
        credentials_file.write("DARKWOOD_DATA_API_KEY={}".format(credentials))


if __name__ == "__main__":
    main()
