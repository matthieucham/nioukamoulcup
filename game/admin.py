from django.contrib import admin
from game import models
from ligue1.admin import admin_site


# Register your models here.
admin_site.register(models.JourneeScoring)