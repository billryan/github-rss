from celery import task
from github.models import Repo
import gh

@task()
def check_db():
    t = Repo.objects.all()
    S = gh.Auth().get_session()
    for col in t:
        owner = col.owner
        repo = col.repo
        print("owner: %s, repo: %s" % (owner, repo))
        gh_repo = gh.Repo()
        repo_info = gh_repo.get_repo_info(S, owner, repo)
        print("description: %s" % (repo_info['description']))
        commits_json = gh_repo.get_commits(S, owner, repo)
        print(len(commits_json))
        commits_info = []
        count = 1
        for commit_json in commits_json:
            print("count: %d" % count)
            count += 1
            commit_info = gh_repo.get_commit_info(S, commit_json)
            commits_info.append(commit_info)
            print(commit_info['author'])

