#/usr/bin/env python
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

# Dynamically calculate the version based on adzone.VERSION
version_tuple = __import__('vendors').VERSION
if len(version_tuple) == 3:
    version = "%d.%d_%s" % version_tuple
else:
    version = "%d.%d" % version_tuple[:2]

setup(
    name = "django-vendors",
    version = version,
    description = "Vendor management for the Django framework.",
    author = "Colin Powell",
    author_email = "colin.powel@me.com",
    url = "http://github.com/powellc/django-vendors/",
    packages = find_packages(),
    package_data = {
        'vendors': [
            'templates/vendors/*.html',
        ]
    },
    zip_safe = False,
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)


