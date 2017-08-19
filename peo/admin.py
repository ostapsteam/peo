from .models import Lab
from django.contrib.gis import admin as gisadmin
from django.contrib.gis import forms as gisforms


class LabAdminForm(gisforms.ModelForm):
    class Meta:
        model = Lab
        widgets = {
            'point': gisforms.OSMWidget
        }


class LabAdmin(gisadmin.OSMGeoAdmin):
    form = LabAdminForm


gisadmin.site.register(Lab, LabAdmin)