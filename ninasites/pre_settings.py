
# Settings to apply to all GeoSites

import os
from geonode.contrib import geosites

# Start with GeoSites pre_settings
GEOSITES_ROOT = os.path.dirname(geosites.__file__)
execfile(os.path.join(GEOSITES_ROOT, 'pre_settings.py'))

# global settings

# base urls for all sites
ROOT_URLCONF = 'ninasites.urls'

# Zinnia blog app
INSTALLED_APPS = INSTALLED_APPS + (
)

THEME_ACCOUNT_CONTACT_EMAIL = ''
