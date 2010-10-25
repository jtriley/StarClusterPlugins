#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

install_requires = [
    "starcluster",
]

src = os.path.realpath(os.path.dirname(__file__))

setup(
    name='StarClusterPlugins',
    version='0.9999',
    package_dir={'starcluster_plugins': 'starcluster_plugins'},
    packages=find_packages(src),
    #scripts=['bin/starcluster'],
    install_requires=install_requires,
    zip_safe=True,
    download_url='http://github.com/jtriley/StarClusterPlugins',
    license='LGPL3',
    author='Justin Riley',
    author_email='justin.t.riley@gmail.com',
    url="http://web.mit.edu/starcluster",
    description="A collection of user-contributed plugins for StarCluster",
    long_description="""
    A collection of user-contributed plugins for StarCluster
    """,
    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Clustering',
    ],
)
