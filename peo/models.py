from django.db import models
from protos.models.proto import GeoProto


class Lab(GeoProto):

    def __unicode__(self):
        return "Lab {}".format(
            self.id
        )
