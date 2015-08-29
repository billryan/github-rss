# encoding:utf-8
from celery import Celery
import os
import time
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'osf.settings')
#os.environ['CELERY_CONFIG_MODULE'] = 'celerytask.celeryconfig'
app = Celery('test')
# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('celerytask.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task()
def add_task(name):
    for i in range(1,10):
        print 'hello:%s %s'%(name,i)
        time.sleep(1)
    return 1
if __name__ == '__main__':
    app.start()