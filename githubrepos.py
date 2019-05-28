import sys
from collections import namedtuple

import requests

import log

logger = log.get_logger(__name__)


def get_github_repos(user):
    """
    Get all repostorys of github user

    :param user: (string) User to get repostories
    :return: (list) The list contains
    repo(name (string), status (bool) url (string))
    status: false, true = private, public
    """
    if not user:
        raise ValueError('Not user provided')

    url_api_github = 'https://api.github.com/users/{}/repos'.format(user)
    resp = requests.get(url_api_github)
    resp = resp.json()

    if not resp:
        raise ValueError('No data found')

    repo = namedtuple('repo', 'name private url')
    repos = []
    for node in resp:
        repos.append(repo(node.get('name'),
                          node.get('private'),
                          node.get('html_url')))
    return repos


def main():
    if len(sys.argv[1:]) < 1:
        raise ValueError('No argument provided')

    print(get_github_repos(sys.argv[1]))


if __name__ == '__main__':
    main()
