import requests
import log
import sys

from collections import namedtuple

logger = log.get_logger(__name__)


def respone_from_url(url, **kwargs):
    """
    Return response from url using requests module

    :param url: (string) **(Required)** A valid url need to fetch data
    :param redirect: (bool) (optional) Allow-redirect. Default is True
    :param timeout: (int) (optional) Time to wait connection. Default is 5
    :return: requests.models.Response
    """

    redirect = kwargs.get('redirect', True)
    timeout = kwargs.get('timeout', 5)

    if not url:
        raise ValueError('No url provied')

    if not url.startswith(('http://', 'https://')):
        url = ''.join(('http://', url))

    try:
        r = requests.get(url, allow_redirects=redirect, timeout=timeout)
    except requests.exceptions.Timeout:
        logger.error('Timeout')
        raise
    except requests.exceptions.InvalidURL:
        logger.error('Invalid URL')
        raise

    if r.status_code != 200:
        return False

    return r


def get_github_repos(user):
    """
    Get all repostorys of github user

    :param user: (string) **(required)** User to get repostories
    :return: (list) The list contains
    repo(name (string), status (bool) url (string))
    status: false, true = private, public
    """
    if not user:
        raise ValueError('Not user provided')

    url_api_github = 'https://api.github.com/users/{}/repos'.format(user)
    resonse = respone_from_url(url_api_github)

    try:
        resonse = resonse.json()
    except ValueError:
        logger.error('Decoding json has failed')
        raise

    repo = namedtuple('repo', 'name private url')
    repos = []
    for node in resonse:
        repos.append(repo(node.get('name'),
                          node.get('private'),
                          node.get('html_url')))
    return repos


def main():
    if len(sys.argv[1:]) != 1:
        raise ValueError('No argument provided')

    print(get_github_repos(sys.argv[1]))


if __name__ == '__main__':
    main()
