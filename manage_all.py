#!/usr/bin/env python

import os
import sys
import subprocess

PROJECT = 'ninasites'

if __name__ == "__main__":
    sites = [os.path.basename(d) for d in os.listdir(PROJECT) if os.path.isfile(os.path.join(PROJECT, d, 'settings.py'))]
    for site in sites:
        print 'Managing %s' % site
        path = '%s/%s/settings.py' % (PROJECT, site)
        if os.path.exists(path):
            os.environ["DJANGO_SETTINGS_MODULE"] = "%s.%s.settings" % (PROJECT, site)
            # call manage.py with above settings to avoid django caching settings in a single session
            subprocess.call(['python', 'manage.py'] + sys.argv[1:])
