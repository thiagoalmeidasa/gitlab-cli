import argparse
import json
import logging
import pprint
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--state', choices=['opened', 'closed'])
    parser.add_argument('--labels', nargs='?')
    args = parser.parse_args()
    pp = pprint.PrettyPrinter(indent=4)

    token = get_token()
