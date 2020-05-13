#!/usr/bin/env python3
"""Packaging with setuptools for use with pip

https://packaging.python.org/tutorials/packaging-projects/#initial-files

"""
from glob import glob
from os import walk
from os.path import (
    abspath,
    dirname,
    join as join_path)
from setuptools import setup
# You will need versioneer installed, or you can remove this if you don't plan to
# use versioneer
import versioneer


def enumerate_static_content(basedir_list):
    """Recursively enumerate static content to easily include data_files"""
    file_list = []
    for basedir in basedir_list:
        for path, _, files in walk(basedir):
            file_list.append((path, [join_path(path, filename) for filename in files if filename not in EXCLUDE_FILES]))
    return file_list


CURDIR = abspath(dirname(__file__))
EXCLUDE_FILES = (
    'constraints.txt',
    'interactive',
    'pip.ini',
    'pip.ini.socks',
    '.gitignore')
LICENSE = 'Proprietary'
# Include data files when installed. See setup.cfg for the choice of this directory name :>
PACKAGE_DATA_DIRS = ['etc/oilfinder']
SCRIPTS = glob('bin/*')

DATA_FILE_LIST = enumerate_static_content(PACKAGE_DATA_DIRS)

# If you use entry points, you can put them in setup.cfg
# ENTRY_POINTS = {
#     'console_scripts': [
#         'cli_app = app:main',
#     ],
# },

# The below version uses versioneer, you'll need to remove `cmdclass` and change
# `version` to a fixed string like `0.0.1` if you don't want to use versioneer
# If you *do* want versioneer, you'll need to do `versioneer install` inside
# the root of the project to bootstrap it, then make some changes to setup.cfg
setup(
    cmdclass=versioneer.get_cmdclass(),
    version=versioneer.get_version(),
    data_files=DATA_FILE_LIST,
    scripts=SCRIPTS)
