from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import User


class Lab(gismodels.Model):
    name = gismodels.CharField(max_length=128, null=False, blank=False)
    desc = gismodels.TextField(null=True, blank=True)

    created_by = gismodels.ForeignKey(User, null=True, blank=True, related_name='+')
    created_at = gismodels.DateTimeField(auto_now_add=True, blank=True, null=True)

    updated_by = gismodels.ForeignKey(User, null=True, blank=True, related_name='+')
    updated_at = gismodels.DateTimeField(auto_now=True, blank=True, null=True)

    deleted_by = gismodels.ForeignKey(User, null=True, blank=True, related_name='+')
    deleted_at = gismodels.DateTimeField(blank=True, null=True)

    point = gismodels.PointField(srid=4326)

    objects = gismodels.GeoManager()

    def __unicode__(self):
        return "Lab #{}".format(
            self.id
        )
