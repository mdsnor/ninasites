# -*- coding: utf-8 -*-

###############################################
# Geosite settings
###############################################

import os
from geonode.contrib import geosites

# Directory of master site - for GeoSites it's two up
GEOSITES_ROOT = os.path.dirname(geosites.__file__)
SITE_ROOT = os.path.dirname(__file__)

try:
    # read in project pre_settings
    execfile(os.path.join(SITE_ROOT, '../', 'pre_settings.py'))
except:
    # if not available, read in GeoSites pre_settings
    execfile(os.path.join(GEOSITES_ROOT, 'pre_settings.py'))


SITE_ID = 1
SITE_NAME = 'Master'
# Should be unique for each site
SECRET_KEY = "fbk3CC3N6jt1AU9mGIcI"

# site installed apps
SITE_APPS = ()

# Site specific databases
SITE_DATABASES = {}



##### Overrides
# Below are some common GeoNode settings that might be overridden for site

# admin email
#THEME_ACCOUNT_CONTACT_EMAIL = ''

# Have GeoServer use this database for this site
#DATASTORE = ''

# Allow users to register
#REGISTRATION_OPEN = True

TEMPLATES  = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
				'/home/matteo.destefano/geonode/geonode/templates/',
				os.path.join(PROJECT_ROOT, "templates"),
				'/home/matteo.destefano/ninasites/ninasites/master/templates',
			],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'django.core.context_processors.debug',
				'django.core.context_processors.i18n',
				'django.core.context_processors.tz',
				'django.core.context_processors.media',
				'django.core.context_processors.static',
				'django.core.context_processors.request',
				'django.contrib.messages.context_processors.messages',
				'account.context_processors.account',
				'geonode.context_processors.resource_urls',
				'geonode.geoserver.context_processors.geoserver_urls',
			],
			'debug': DEBUG,
		},
	},
]
# Read in GeoSites post_settings
try:
    # read in project pre_settings
    execfile(os.path.join(SITE_ROOT, '../', 'post_settings.py'))
except:
    # if not available, read in GeoSites pre_settings
    execfile(os.path.join(GEOSITES_ROOT, 'post_settings.py'))


