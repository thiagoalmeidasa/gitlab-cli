import argparse
import json
import logging
import pprint
import requests

from session import get_token

global token


def list_projects(token, **kwargs):
    h = {'PRIVATE-TOKEN': token}
    url_base = "https://git.mossteam.com.br/api/v3/"
    u = url_base + "projects/"
    u = u + "?"
    if kwargs['archived']:
        u = u + "&archived=true"
    if kwargs['visibility']:
        u = u + "&visibility=" + kwargs['visibility']
    if kwargs['order_by']:
        u = u + "&order_by=" + kwargs['order_by']
    if kwargs['sort']:
        u = u + "&sort=" + kwargs['sort']
    if kwargs['search']:
        u = u + "&search=" + kwargs['search']
    logging.debug(u)
    r = requests.get(u, headers=h)
    return r.json()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--archived', action='store_true')
    parser.add_argument('--visibility', choices=['public', 'internal', 'private'])
    parser.add_argument('--order-by', choices=['id', 'name', 'updated_at'])
    parser.add_argument('--sort', choices=['asc', 'desc'])
    parser.add_argument('--search', nargs='?')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    pp = pprint.PrettyPrinter(indent=4)

    token = get_token()
    pp.pprint(list_projects(token, archived=args.archived,
visibility=args.visibility, order_by=args.order_by, sort=args.sort,
search=args.search))
