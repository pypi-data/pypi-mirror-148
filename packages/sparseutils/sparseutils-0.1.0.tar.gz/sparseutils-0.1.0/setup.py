#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3',
    'Topic :: Utilities',
]

setup(
    name='sparseutils',
    author='Richard Ipsum',
    author_email='richardipsum@vx21.xyz',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.0',
    description='Utilities for interacting with sparse files',
    classifiers=classifiers,
    keywords='sparse',
    packages=['sparseutils'],
    zip_safe=False,
    entry_points= {
        'console_scripts': [
            'mksparse=sparseutils.mksparse:main',
            'sparsemap=sparseutils.sparsemap:main'
        ]
    },
)
