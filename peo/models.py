from django.contrib.gis.db import models as gismodels
from protos.models.proto import GeoProto


class Lab(gismodels.Model, GeoProto):

    objects = gismodels.GeoManager()

    def __unicode__(self):
        return "Lab {}".format(
            self.id
        )
