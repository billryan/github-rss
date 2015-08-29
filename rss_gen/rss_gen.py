__author__ = 'billryan'

from feedgen.feed import FeedGenerator

class Atom:
    """GitHub Atom"""
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

    def gen_atom(self, repo_info, commits_info, atom_fn):
        fg_repo = self.init_fg(repo_info)
        for commit_info in commits_info:
            self.add_entry(fg_repo, commit_info)
            fg_repo.atom_file(atom_fn)
