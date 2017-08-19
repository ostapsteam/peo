from django.db import models
from protos.models.proto import GeoProto, Proto

# Create your models here.
class Lab(Proto, GeoProto):
    pass
