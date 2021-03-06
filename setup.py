#!/usr/bin/env python

from __future__ import print_function

from glob import glob
import subprocess

from setuptools import setup


setup(name='cardboardlint',
    version='0.0.0',
    description='Cheap lint solution for PRs.',
    scripts=glob("scripts/*"),
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
