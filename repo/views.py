from django.shortcuts import render
from django.http import HttpResponse
import datetime

def index(request):
    if request.method == "GET":
        now = datetime.datetime.now()
        return render(request, 'repo.html', {'current_date': now})
    elif request.method == "POST":
        return HttpResponse("Thanks!")


