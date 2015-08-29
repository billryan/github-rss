from django.contrib import admin

# Register your models here.
from django.contrib import admin
from kombu.transport.django import models as kombu_models

admin.site.register(kombu_models.Message)