import os
from django.shortcuts import render
from django.http import HttpResponse
import datetime
import re
from github.models import Repo

BASE_DIR = os.path.dirname(__file__)

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


def feed_xml(request, owner, repo):
    if request.method == "GET":
        rss_root = os.path.join(BASE_DIR, 'output')
        return HttpResponse(open('/'.join([rss_root, owner, repo, 'diff.xml'])).read(), content_type='text/xml')
