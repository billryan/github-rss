#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getpass
import six
import requests
from feedgen.feed import FeedGenerator


class GitHubCommit:
    """GitHub Commit"""

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
        url = '/'.join([self.auth_url, 'repos', owner, repo, 'commits'])
        commits = s.get(url)
        return commits.json()

    def get_commit_info(self, s, commit_json):
        commit_info = {}
        # url for get_commit_diff
        commit_info['diff_url'] = commit_json['url']
        commit_info['diff'] = self.get_commit_diff(s, commit_info['diff_url'])
        commit_info['html_url'] = commit_json['html_url']
        commit_info['sha'] = commit_json['sha']
        commit = commit_json['commit']
        commit_info['url'] = commit['url']
        author = {}
        author['name'] = commit['author']['name']
        author['email'] = commit['author']['email']
        commit_info['author'] = author
        commit_info['updated'] = commit['author']['date']
        commit_info['message'] = commit['message']

        return commit_info

    def get_commit_diff(self, s, commit_url):
        diff_headers = {'Accept': 'application/vnd.github.diff'}
        print("commit_url: %s" % commit_url)
        commit_diff = s.get(commit_url, headers=diff_headers).text
        return commit_diff

    def get_repo_info(self, s, owner, repo):
        url = '/'.join([self.auth_url, 'repos', owner, repo])
        repo_json = s.get(url).json()
        repo_info = {}
        repo_info['description'] = repo_json['description']
        repo_info['full_name'] = repo_json['full_name']
        repo_info['html_url'] = repo_json['html_url']
        repo_info['updated_at'] = repo_json['updated_at']
        repo_info['author'] = self.get_author(s, owner)
        return repo_info

    def get_author(self, s, owner):
        url = '/'.join([self.auth_url, 'users', owner])
        author_json = s.get(url).json()
        author_info = {}
        author_info['name'] = owner
        author_info['email'] = author_json['email']
        return author_info


class GitHubRSS:
    """GitHub RSS"""
    def __init__(self):
        self.atom = True

    def init_fg(self, repo_info):
        fg = FeedGenerator()
        title = 'Recent commits to ' + repo_info['full_name']
        fg.title(title)
        fg.link(href=repo_info['html_url'])
        fg.updated(repo_info['updated_at'])
        fg.id(repo_info['html_url'])
        fg.author(repo_info['author'])
        return fg

    def add_entry(self, fg, commit_info):
        fe = fg.add_entry()
        fe.title(commit_info['message'])
        fe.link(href=commit_info['html_url'])
        id_prefix = 'tag:github.com,2008:Grit::Commit/'
        entry_id = id_prefix + commit_info['sha']
        fe.id(entry_id)
        fe.author(commit_info['author'])
        fe.published(commit_info['updated'])
        fe.updated(commit_info['updated'])
        fe.content(commit_info['diff'])
        return fg

    def gen_atom(self, fg, atom_fn='atom.xml'):
        fg.atom_file(atom_fn)

if __name__ == "__main__":
    # auth with GitHub username and password
    user = raw_input('Enter your GitHub username: ')
    passwd = getpass.getpass()
    g_commit = GitHubCommit(user, passwd)
    s = requests.Session()
    s.auth = (g_commit.user, g_commit.passwd)
    r = s.get(g_commit.auth_url)
    if r.status_code == 401:
        print("Unauthorized. Wrong username or password!")
        sys.exit("Exit for Unauthorized status")

    owner = 'billryan'
    repo = 'algorithm-exercise'
    repo_info = g_commit.get_repo_info(s, owner, repo)
    commits_json = g_commit.get_commits(s, owner, repo)
    commits_info = []
    for commit_json in commits_json:
        commit_info = g_commit.get_commit_info(s, commit_json)
        commits_info.append(commit_info)

    # generate rss
    rss = GitHubRSS()
    fg_repo = rss.init_fg(repo_info)
    for commit_info in commits_info:
        rss.add_entry(fg_repo, commit_info)

    rss.gen_atom(fg_repo, '/tmp/test/atom_test.xml')
