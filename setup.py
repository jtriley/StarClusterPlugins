#!/usr/bin/env python
import os
from setuptools import setup, find_packages

install_requires = [
    "setuptools",
    "starcluster",
]

src = os.path.realpath(os.path.dirname(__file__))

setup(
    name='StarClusterPlugins',
    version='0.9999',
    packages=find_packages(src),
    namespace_packages=['starcluster'],
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
