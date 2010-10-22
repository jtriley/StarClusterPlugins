from distutils.core import setup
setup(
    name = 'starcluster-extras',
    packages = ['starcluster-extras'],
    version = '0.0.2',
    description = 'Extra plugins for StarCluster',
    author = 'Austin Godber',
    author_email = 'godber@uberhip.com',
    url = 'http://github.com/godber/starcluster-extras',
    long_description = """\
starcluster-extras
~~~~~~~~~~~~~~~~~~

This package contains plugins that extend StarCluster.  These include the
following plugins:

 * ``PackageLoader`` - Loads packages on all cluster nodes from manifest stored
     in /home/ EBS volume.
"""
)
