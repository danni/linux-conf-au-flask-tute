#!/usr/bin/env python

import os

from setuptools import setup, find_packages

PROJECT_ROOT = os.environ.get('OPENSHIFT_REPO_DIR',
                              os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(PROJECT_ROOT, 'requirements.txt')) as file_:
    requirements = [req.strip() for req in file_.xreadlines()]

setup(name='example',
      version='0.0',
      author='Danielle Madeley',
      author_email='danielle@madeley.id.au',
      url='https://github.com/danni/linux-conf-au-flask-tute',
      description='Example deploy to OpenShift',
      install_requires=requirements,
      )
