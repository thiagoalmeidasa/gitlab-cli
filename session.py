import argparse
import json
import requests


def get_token():
    with open('.gitlabrc', 'r') as file:
        j = json.load(file)
        return j['private_token']


def session(email, password):
    url_base = "https://git.mossteam.com.br/api/v3/"
    u = url_base + "session?email=" + args.email + "&password=" + args.password
    r = requests.post(u)
    return r.json()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', nargs='?')
    parser.add_argument('--password', nargs='?')
    args = parser.parse_args()
    s = session(args.email, args.password)
    with open('.gitlabrc', 'w') as file:
        json.dump(s, file)
