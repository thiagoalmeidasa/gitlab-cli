import argparse
import json
import logging
import requests

from session import get_token

global token


def list_issues(token, **kwargs):
    h = {'PRIVATE-TOKEN': token}
    url_base = "https://git.mossteam.com.br/api/v3/"
    u = url_base + "issues/"
    u = u + "?"
    if 'state' in kwargs:
        if kwargs['state'] == 'opened':
            u = u + "state=opened"
        if kwargs['state'] == 'closed':
            u = u + "state=closed"
    if 'labels' in kwargs:
        u = u + "&labels=" + kwargs['labels']
    r = requests.get(u, headers=h)
    return r.json()


def list_project_issues(token, project_id, **kwargs):
    h = {'PRIVATE-TOKEN': token}
    url_base = "https://git.mossteam.com.br/api/v3/"
    u = url_base + "projects/" + project_id + "/issues/"
    r = requests.get(u, headers=h)
    return r.json()


def print_project_issues(json):
    if isinstance(json, dict):
        s = '{0:<2}\t{1:<60}'.format(
            json['id'], json['title'], json['description'])
        print(s)
    else:
        for i in json:
            s = '{0:<2}\t{1:<60}'.format(i['id'], i['title'], i['description'])
            print(s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--state', choices=['opened', 'closed'])
    parser.add_argument('--labels', nargs='?')
    parser.add_argument('--project', nargs='?')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    token = get_token()

    if args.project:
        print_project_issues(list_project_issues(token, args.project))
