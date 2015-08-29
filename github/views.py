from django.shortcuts import render
from django.http import HttpResponse
import datetime
import re
from github.models import Repo


def index(request):
    if request.method == "GET":
        now = datetime.datetime.now()
        return render(request, 'repo.html', {'current_date': now})
    elif request.method == "POST":
        raw_url = request.POST['raw_url']
        repo_info = filter_repo_url(raw_url)
        if repo_info is None:
            return HttpResponse("Invalid URL!!!")
        else:
            obj, created = Repo.objects.get_or_create(repo_url=repo_info['repo_url'], owner=repo_info['owner'],
                                                      repo=repo_info['repo'])
            obj.save()
    return HttpResponse("Thanks!")

def filter_repo_url(raw_url=''):
    pattern = "(?P<host>(git@|https?://)(github.com)(/|:))(?P<owner>[\w,\-,\_]+)/(?P<repo>[\w,\-,\_]+)(.git){0,1}"
    m = re.search(pattern, raw_url)
    if m is not None:
        owner = m.group('owner')
        repo = m.group('repo')
        repo_url = '/'.join(['https://github.com', owner, repo])
        return {'repo_url': repo_url, 'owner': owner, 'repo': repo}
