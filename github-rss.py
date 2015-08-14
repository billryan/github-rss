#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getpass
import six
import requests


class GitHubRSS:
    """GitHub RSS"""

    def __init__(self, user=None, passwd=None):
        self.auth_url = 'https://api.github.com'
        if isinstance(user, six.string_types):
            self.user = user
        else:
            self.user = ''
        if isinstance(passwd, six.string_types):
            self.passwd = passwd
        else:
            self.passwd = ''

    def get_commits(self, s, owner, repo, nums=30):
        repo_url = '/'.join([self.auth_url, 'repos', owner, repo, 'commits'])
        commits = s.get(repo_url)
        return commits.json()

    def get_commit_url(self, commit_json):
        return commit_json['url']

    def get_commit_diff(self, s, commit_url):
        diff_headers = {'Accept': 'application/vnd.github.diff'}
        commit_diff = s.get(commit_url, headers=diff_headers)

if __name__ == "__main__":
    # auth with GitHub username and password
    user = raw_input('Enter your GitHub username: ')
    passwd = getpass.getpass()
    rss = GitHubRSS(user, passwd)
    s = requests.Session()
    s.auth = (rss.user, rss.passwd)
    r = s.get(rss.auth_url)
    if r.status_code == 401:
        print("Unauthorized. Wrong username or password!")
        sys.exit("Exit for Unauthorized status")

    commits = rss.get_commits(s, 'billryan', 'algorithm-exercise')
