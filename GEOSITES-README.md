# GeoSites for GeoNode

This is a template for creating a new project utilizing GeoNode's GeoSites. GeoSites is a contrib module to GeoNode starting with 2.4 and is a way to run multiple websites with a single instance of GeoNode. Each GeoSite can have different templates, applications, and data permissions but share a single database, web mapping service (GeoServer), and CSW (pycsw).  This is useful when multiple websites are desired to support different sets of users, but with a similar set of data and overall look and feel of the sites.  Users can be given permission to access multiple sites if needed, which also allows administrative groups can be set up to support all sites with one account.

A GeoSites installation uses a 'master' GeoNode website that has access to all users, groups, and data. Through the Django admin page, Layers, Maps, Documents, Users, and Groups can be added and removed from all sites.  Users can be given access to any number of sites, and data may appear on only a single site, or all of them.  The master site need not be accessible from the outside so that it can be used as an internal tool to the organization. Users created on a site are created with access to just that site (but not the master site).  Data uploaded to a site is given permission on that site as well as the master site. The master site, and all of the individual GeoSites, share a single database. Objects, including users, groups, and data layers, all appear within the database with an additional table indicating which users and sites have access to which data.

## Installation

To create a new project using geosites-project as a template, folllow the steps below to set up a virtual environment, install GeoNode, and create a GeoSites project.  In the examples below project_name is a unique name for your project and example.org is the domain for the GeoNode sites.

    $ sudo pip install virtualenv

    $ virtualenv venv --system-site-packages

    $ source venv/bin/activate

    $ pip install geonode

    $ django-admin.py startproject project_name --template=https://github.com/terranodo/geosites-project/archive/master.zip -epu,rst,yml

    $ cd project_name

    $ bash ./setup.sh example.org


### GeoServer

A single GeoServer instance is used to serve data to all of the GeoSites.  Install GeoServer as normal for GeoNode either on the same machine or a different one. Each site will proxy the /geoserver URL to the address of GeoServer (see the nginx configuration files). However, The default GeoNode installation sets the URL of the GeoNode site in one of the GeoServer config files: Edit the *GEOSERVER_DATA_DIR/security/auth/geonodeAuthProvider/config.xml* by changing the baseUrl field to an empty string:

    <baseUrl></baseUrl>

When baseUrl is empty, GeoServer will attempt to authenticate against the requesting URL.  Since a reverse proxy to GeoServer is configured on the web servers the requesting URL can be used to determine the URL to GeoNode. In fact, setting baseUrl to an empty string will work on a non GeoSites implementation of GeoNode as well, since a proxy is configured by default for a regular GeoNode project as well.

## GeoSites Project

After installing you will have a directory of files for your project. A GeoSites project looks similar to a normal GeoNode project, but with additional folders and settings files for sites. In the project below there is just one directory for the master site. Additional sites will have the same structure as the master site. Each site folder contains a settings file and local_settings with site specific settings, as well as directories for static files and Django templates, and web server and application configuration files (nginx, gunicorn, wsgi.py).

~~~
geosites-project
├── project_name
│   ├── __init__.py
│   ├── local_settings.py
│   ├── master
│   │   ├── conf
│   │   │   ├── gunicorn
│   │   │   └── nginx
│   │   ├── __init__.py
│   │   ├── local_settings.py
│   │   ├── settings.py
│   │   ├── static
│   │   │   ├── css
│   │   │   │   └── site_base.css
│   │   │   ├── img
│   │   │   │   └── README
│   │   │   ├── js
│   │   │   │   └── README
│   │   │   └── README
│   │   ├── templates
│   │   │   ├── site_base.html
│   │   │   ├── site_index.html
│   │   └── wsgi.py
│   ├── post_settings.py
│   ├── pre_settings.py
│   ├── sites.json
│   └── urls.py
├── manage_all.py
├── manage.py
├── README.rst
├── setup.py
└── setup.sh
~~~

## Configuration Hierarchy

GeoSites configuration files (for settings, templates, and static files) work in a hierarchy: first default GeoNode, then GeoSites (from geosites contrib module), then project, then site specific. There is also a sites.json file, which is a JSON file of the sites database table.  This is for convenience, as the file will contain the site IDs and names for all currently enabled sites.  The urls file is a common urls file, although each site could have their own urls file if needed (by creating one and setting it in the site specific settings file *siteX/settings.py*).

### Settings
Site settings are managed through the use of common settings files as well as site specific settings files. The project folder contains common settings in the pre_settings.py, post_settings.py, and local_settings.py files, while sites contain settings.py and local_settings.py files. An example site settings.py file is shown here.

~~~
import os
from geonode.contrib import geosites

# Read in GeoSites pre_settings
GEOSITES_ROOT = os.path.dirname(geosites.__file__)
execfile(os.path.join(GEOSITES_ROOT, 'pre_settings.py'))

# Site specific variables
SITE_ID = 2
SITE_NAME = 'site2'
SECRET_KEY = "fbk3CC3N6jt1AU9mGIcI"
SITE_APPS = ()
SITE_DATABASES = {}

# Overrides - common settings that might be overridden for site

# urls for all sites
# ROOT_URLCONF = 'projectname.site2.urls'

# admin email
# THEME_ACCOUNT_CONTACT_EMAIL = ''

# Have GeoServer use this database for this site
# DATASTORE = ''

# Allow users to register
# REGISTRATION_OPEN = True

# Read in GeoSites post_settings
execfile(os.path.join(GEOSITES_ROOT, 'post_settings.py'))
~~~

This settings file first reads in the GeoSites pre_settings.py file, which in turns reads in the default GeoNode settings then overrides some of the values.  Then, site specific variables are set: the site ID, name, and secret key.  SITE_APPS are additional apps that should be added to this site, while SITE_DATABASES is used when a site should be using a separate database (such as for a datastore of geospatial data separate from other sites).  In this case add a geospatial DB to the SITE_DATABASES dictionary (or in the local_settings, see below), then set DATASTORE to the key of that database.

To make the sites easier to administrate it is recommended that any site added to a site also be added to the master site settings.py file. This will allow it to be administered throught the admin panel of the master site rather than only through the specific site.

#### Local Settings

Databases are usually set in a local_settings file, as are other production settings.  The local_settings file in the project directory is used by all sites, so it is here where the database is set for all sites. Here is an example project local_settings file.

~~~
# path for static and uploaded files
SERVE_PATH = '/home/myuser/geonodeproject'

# database info
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'geonode',
         'USER': 'geonode',
         'PASSWORD': 'geonode',
     },
    # vector datastore for uploads
    'datastore' : {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
         #'ENGINE': '', # Empty ENGINE name disables 
        'NAME': 'geonode_data',
        'USER' : 'geonode',
        'PASSWORD' : 'geonode',
        'HOST' : 'localhost',
        'PORT' : '5432',
    }
}

# email account for sending email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

#REGISTRATION_OPEN=True
#ACCOUNT_EMAIL_CONFIRMATION_EMAIL=True
#ACCOUNT_EMAIL_CONFIRMATION_REQUIRED=True

# uncomment for production
# PROXY_ALLOWED_HOSTS = ('.{{ domain }}')

# localhost by default
# GEOSERVER_URL = 'http://localhost:8080/'
~~~

SERVE_PATH is the path used for serving of static files for all sites (it is also where webserver logs will be put). DATABASES are any production databases used by all sites. In the example above there is a database for the Django database, and another used for storing geospatial vector data served by GeoServer.  The email account is used by GeoNode to send emails to users when needed. PROXY_ALLOWED_HOSTS should be uncommented in production. The GEOSERVER_URL is the **internal URL** (not the reverse proxy URL) of GeoServer, localhost port 8080 if running on the same machine.

Specific sites must also have a local_settings file in production environments, which sets the SITEURL.

~~~
import os

# Outside URL
SITEURL = 'http://master.example.org'

# databases unique to site if not defined in site settings
"""
SITE_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, '../development.db'),
    },
}
"""
~~~

### Templates and Static Files

The template used for any given page will be be the first one found, so templates in the SITE_ROOT/templates directory will override those in PROJECT_ROOT/templates, which will override those in GEONODE_ROOT/templates.  Static files use a hierarchy similar to the the template directories.  However, they work differently because (on a production server) they are collected and stored in a single location.  Because of this care must be taken to avoid clobbering of files between sites, so each site directory should contain all static files in a subdirectory with the name of the site (e.g., static/siteA/logo.png )

The location of the proper static directory can then be found in the templates syntax such as:

    {{ STATIC_URL }}{{ SITENAME|lower }}/logo.png


## Site Management

The top level directory contains two manage scripts, a standard Python setup script and a bash script. The familiar manage.py is a regular Django manage file that uses the master site as the settings file. This is the command that should be used when doing many tasks such as inspecting the database, creating a super-user, or adding a new site.  The manage_all.py script is when a command should be run on all sites, such as syncdb and collectstatic.  The syncdb command will sync the DB using the settings file of each site  and is required if there are different INSTALLED_APPS in each site. The collectstatic command will loop through the sites and collect the static files of all sites in the common location they are served from.

After setting up the project for the first time, or when updating the code, the database needs to be migrated and any seed data loaded. All the GeoSites share the same database that is defined in geosites-project/project_name/local_settings.py file. For development or if you need a separate database uncomment and edit the SITE_DATABASES directive in the settings.py file in that sites directory.

    $ cd project_name

    $ python manage.py syncdb

    $ python manage.py loaddata project_name/sites.json

By default the master site is already registered in the database and has an ID of 1. Additional sites created will have the ID incremented by 1, thus the first site created after the master site will have an ID of 2.

### Adding New Sites

A management command exists to create a new site, which includes all the needed directories, site specific settings file, and website configuration files. Website files currently include nginx (as the web server) and gunicorn (as the application server).  While Apache config files (with mod_wsgi as the application server) are not currently genererated, Apache supports the same configuration necessary for GeoSites to work.

    $ python manage.py addsite mynewgeosite mynewgeosite.example.org

Which will create a new directory of files:
~~~
│   ├── mynewgeosite
│   │   ├── conf
│   │   │   ├── gunicorn
│   │   │   └── nginx
│   │   ├── __init__.py
│   │   ├── local_settings.py
│   │   ├── settings.py
│   │   ├── static
│   │   │   ├── css
│   │   │   │   └── site_base.css
│   │   │   ├── img
│   │   │   │   └── README
│   │   │   ├── js
│   │   │   │   └── README
│   │   │   └── README
│   │   ├── templates
│   │   │   ├── site_base.html
│   │   │   ├── site_index.html
│   │   └── wsgi.py
~~~

#### Permissions by Site

Users are added by default to the site on where they are created and they belong to that site only. However, an admin can add or remove users from sites through the "Site People" admin panel (Admin->GeoSites->sitepeople). Select the desired site and move people between the boxes to enable or disable them from the site. 

By default data added to GeoNode is publicly available. In the case of GeoSites, new data will be publicly available, but only for the site it was added to, and the master site (all data is added to the master site). Sharing a resource with other sites is done through the SiteResources table admin panel (Admin->GeoSites->SiteResource).  Add or remove available data to a site by moving resources between the two panels.

## Production

In summary, to create a new project running on a production machine, take the following steps after following the installation instructions given above.

    - Create local_settings.py in your projectect directory and all site directories (master, site2, etc.) based on the provided local_settings.py.sample

    - Edit project/local_settings.py to contain your unique site information for production: the serve path (which must exist) where static files will be collected, database connection information, Email account info, registration options, and the GeoServer URL.

    - Edit site local_settings in each site directory. Any info that is different than the project local_settings should be provided here, otherwise those will be used (e.g., DATABASES from project/local_settings.py). Otherwise, the only thing that is required in the site local_settings is SITEURL.

    - Initialize the database with syncdb and loaddata as given above under Site Management

    - Add new sites as desired

Now, links can be created for nginx and gunicorn, and the services restart:

    $ cd /etc/nginx/sites-available

    $ ln -s /full/path/to/project/project/master/conf/nginx master

    $ cd /etc/nginx/sites-enabled

    $ ln -s ../sites-available/master ./

    $ cd /etc/gunicorn.d

    $ ln -s /full/path/to/project/project/master/conf/gunicorn master

    $ sudo service nginx restart

    $ sudo service gunicorn restart


## Development

Without the local_settings files that specify database and site url, GeoSites will utilize a SQLlite database and run on localhost, which is used for development. A specific site can be run locally for development purposes by using the runserver command as normal. Run multiple sites be calling runserver multiple times with a different port for each site:

    # for the master site
    $ python manage.py runserver
  
    # for each geosite
    $ python manage.py runserver localhost:XXXX --settings=project_name.siteX.settings

When customizing the look and feel of each specific site or the project as a whole keep in mind the hiearchy described above, which is used for templates as well. Override templates for a site by reproducing the same template folder structure as is provided by the app. If you override templates on one site they will only be used for that specific site, but other sites will still use the default templates.
