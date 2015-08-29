import os
from celery import task
from github.models import Repo
import github.gh as gh
from rss_gen import Atom


BASE_DIR = os.path.dirname(__file__)

@task()
def rss_gen():
    t = Repo.objects.all()
    S = gh.Auth().get_session()
    for col in t:
        owner = col.owner
        repo = col.repo
        print("owner: %s, repo: %s" % (owner, repo))
        gh_repo = gh.Repo()
        repo_info = gh_repo.get_repo_info(S, owner, repo)
        commits_info = gh_repo.get_commits_info(S, owner, repo)
        # make RSS output dirs recursively
        rss_root = os.path.join(BASE_DIR, 'output')
        owner_path = os.path.join(rss_root, owner)
        mkdir_p(owner_path)
        # generate Atom
        atom_fn = os.path.join(owner_path, repo + '.xml')
        atom = Atom()
        atom.gen_atom(repo_info, commits_info, atom_fn)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
