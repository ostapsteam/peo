from .models import Lab
from django.contrib.gis import admin as gisadmin
from django.contrib.gis import forms as gisforms


class LabAdminForm(gisforms.ModelForm):
    point = gisforms.PointField(
        widget=gisforms.OSMWidget(attrs={'display_raw': True})
    )


class LabAdmin(gisadmin.OSMGeoAdmin):
    form = LabAdminForm


gisadmin.site.register(Lab, LabAdmin)