from .models import Lab
from django.contrib.gis import admin as gisadmin
from django.contrib.gis import forms as gisforms
from django.contrib.gis.db import models as gismodels


class LabAdmin(gisadmin.OSMGeoAdmin):
    formfield_overrides = {
        gismodels.PointField: {'widget': gisforms.OSMWidget},
    }


gisadmin.site.register(Lab, LabAdmin)