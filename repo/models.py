from django.db import models


class Repo(models.Model):
    url = models.URLField()
    owner = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.owner + '/' + self.name
