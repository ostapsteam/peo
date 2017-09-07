import os
import peo
import logging

log = logging.getLogger(__file__)

d = os.path.dirname(__file__)
major, minor = peo.VERSION
log.info("Current peo version %s", peo.VERSION)
minor += 1

with open(os.path.join(d, "__init__.py"), "w") as vers:
    vers.write("VERSION = {}, {}\n".format(major, minor))

log.info("Updated to %s", (major, minor))
