import argparse
import json
import logging
import requests

from session import get_token

global token


def list_project_events(id):
    h = {'PRIVATE-TOKEN': token}
    url_base = "https://git.mossteam.com.br/api/v3/"
    u = url_base + "projects/"
    u = u + id + "/events"
    logging.debug(u)
    r = requests.get(u, headers=h)
    return r.json()

def list_project(id):
    h = {'PRIVATE-TOKEN': token}
    url_base = "https://git.mossteam.com.br/api/v3/"
    u = url_base + "projects/"
    u = u + id
    logging.debug(u)
    r = requests.get(u, headers=h)
    return r.json()


def list_projects(token, **kwargs):
    h = {'PRIVATE-TOKEN': token}
    url_base = "https://git.mossteam.com.br/api/v3/"
#    u = url_base + "projects/"
    u = url_base + "/projects/all?per_page=100"
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


def print_list_project(json):
    if isinstance(json, dict):
        s = '{0:<2}\t{1:<30}\t{2:30}\t{3:60}'.format(
            json['id'], json['name'], json['owner']['name'], json['web_url'])
        print(s)


def print_list_project_events(json):
    for i in json:
        s = '{0:<30}\t{1:<30}\t{2:30}'.format(
            i['target_type'], i['title'], i['target_title'])
        print(s)


def print_list_projects(json):
    if isinstance(json, dict):
        s = '{0:<2}\t{1:<30}\t{2:30}\t{3:60}'.format(
                json['id'], json['name'],
                json['owner']['name'],
                json['web_url'])
        print(s)
    else:
        for i in json:
            s = '{0:<2}\t{1:<30}\t{2:60}'.format(
                i['id'], i['name'], i['web_url'])
            print(s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--archived', action='store_true')
    parser.add_argument('--events', action='store_true')
    parser.add_argument(
        '--visibility',
        choices=['public', 'internal', 'private'])
    parser.add_argument('--order-by', choices=['id', 'name', 'updated_at'])
    parser.add_argument('--sort', choices=['asc', 'desc'])
    parser.add_argument('--search', nargs='?')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--id', nargs='?')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    token = get_token()

    if args.id and not args.events:
        print_list_project(list_project(args.id))
    elif args.events:
        print_list_project_events(list_project_events(args.id))
    else:
        print_list_projects(list_projects(token, archived=args.archived,
        visibility=args.visibility, order_by=args.order_by, sort=args.sort,
        search=args.search))
