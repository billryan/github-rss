from celerytask.tasks import add_task

# encoding:utf-8
from django.http import HttpResponse
from django.views.generic import View


class Hello(View):

    def get(self, request, *args, **kwargs):
        add_task.delay('GreenPine')
        return HttpResponse('Hello, World!')