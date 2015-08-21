from django.db import models


class Repo(models.Model):
    repo_url = models.URLField(max_length=200)
    owner = models.CharField(max_length=200)
    repo = models.CharField(max_length=200)

    def __unicode__(self):
        return self.owner + '/' + self.repo
