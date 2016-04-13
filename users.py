import argparse
import json
import requests

from session import get_token

global token


def list_users(token, **kwargs):
    url_base = "https://git.mossteam.com.br/api/v3/"
    h = {'PRIVATE-TOKEN': token}
    u = url_base + "users"
    if kwargs['id']:
        u = u + "/" + kwargs['id']
    elif kwargs['username']:
        u = u + "?username=" + kwargs['username']
    r = requests.get(u, headers=h)
    return r.json()


def print_list_users(json):
    if isinstance(json, dict):
        s = '{0:<2}\t{1:<30}\t{2}'.format(json['id'], json['username'], json['email'])
        print(s)
    else:
        for i in json:
            s = '{0:<2}\t{1:<30}\t{2}'.format(i['id'], i['username'], i['email'])
            print(s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', nargs='?')
    parser.add_argument('--username', nargs='?')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    token = get_token()
    print_list_users(list_users(token, id=args.id, username=args.username))
