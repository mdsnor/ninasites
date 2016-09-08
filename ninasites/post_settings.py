# settings to apply to all GeoSites
import os

from geonode.contrib import geosites

GEOSERVER_URL = 'http://geoserver..org:8080/geoserver/'

# use GeoSites post_settings
GEOSITES_ROOT = os.path.dirname(geosites.__file__)
execfile(os.path.join(GEOSITES_ROOT, 'post_settings.py'))
