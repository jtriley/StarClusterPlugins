from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log
import os.path

class PackageLoader(ClusterSetup):
    """
    Loads a list of packages out of the /home/.starcluster-packages
    file.  This file is a dselect package list and can be managed manually.
    The utility ``cluster-install`` is provided to automatically manage this
    file while also installing the packages on all nodes.  This plugin assumes
    that /home/ is an EBS volume.

    Warning: This will upgrade any packages that are out of date.  So you might
    end up with slightly different builds of packages.
    """
    def __init__(self):
        log.debug('Running PackageLoader plugin.')
    def run(self, nodes, master, user, user_shell, volumes):
        pkgfile = '/home/.starcluster-packages'
        mconn = master.ssh
        # Test for the package file on the master node
        if mconn.path_exists(pkgfile):
            log.info("[PackageLoader] Package file found at: %s" % pkgfile)
            for node in nodes:
                log.info("[PackageLoader] Installing packages on %s" % node.alias)
                node.ssh.execute('dpkg --set-selections < ' + pkgfile)
                node.ssh.execute('apt-get update && apt-get -y dselect-upgrade')
        else:
            log.info("[PackageLoader] No package file found at: %s" % pkgfile)

