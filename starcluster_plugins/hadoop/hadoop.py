#!/usr/bin/env python
"""
Hadoop Plugin for StarCluster

Author: Justin Riley

Use this plugin with any StarCluster AMI that has "hadoop" in
it's name. You can check for hadoop compatible AMIs in the output of
'starcluster listpublic'.
"""
import posixpath

from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

core_site_templ = """\
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<!-- In: conf/core-site.xml -->
<property>
  <name>hadoop.tmp.dir</name>
  <value>%(hadoop_tmpdir)s</value>
  <description>A base for other temporary directories.</description>
</property>

<property>
  <name>fs.default.name</name>
  <value>hdfs://%(master)s:54310</value>
  <description>The name of the default file system.  A URI whose
  scheme and authority determine the FileSystem implementation.  The
  uri's scheme determines the config property (fs.SCHEME.impl) naming
  the FileSystem implementation class.  The uri's authority is used to
  determine the host, port, etc. for a filesystem.</description>
</property>

</configuration>
"""

hdfs_site_templ = """\
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<!-- In: conf/hdfs-site.xml -->
<property>
  <name>dfs.permissions</name>
  <value>false</value>
</property>
<property>
  <name>dfs.replication</name>
  <value>%(num_nodes)d</value>
  <description>Default block replication.
  The actual number of replications can be specified when the file is created.
  The default is used if replication is not specified in create time.
  </description>
</property>
</configuration>
"""

mapred_site_templ = """\
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<!-- In: conf/mapred-site.xml -->
<property>
  <name>mapred.job.tracker</name>
  <value>%(master)s:54311</value>
  <description>The host and port that the MapReduce job tracker runs
  at.  If "local", then jobs are run in-process as a single map
  and reduce task.
  </description>
</property>
</configuration>
"""


class Hadoop(ClusterSetup):
    """
    Configures Hadoop on StarCluster
    """

    def __init__(self, hadoop_tmpdir='/mnt/hadoop'):
        self.hadoop_tmpdir = hadoop_tmpdir
        self.hadoop_conf = '/etc/hadoop-0.20/conf.starcluster'
        self.empty_conf = '/etc/hadoop-0.20/conf.empty'

    def _configure_hadoop(self, master, nodes, user):
        log.info("Configuring Hadoop...")
        log.info("Adding user %s to hadoop group" % user)
        for node in nodes:
            node.ssh.execute('gpasswd -a %s hadoop' % user)
        node_aliases = map(lambda n: n.alias, nodes)
        cfg = {'master': master.alias, 'num_nodes': len(nodes),
               'hadoop_tmpdir': posixpath.join(self.hadoop_tmpdir,
                                               'hadoop-${user.name}')}
        for node in nodes:
            node.ssh.execute('cp -r %s %s' % (self.empty_conf, self.hadoop_conf))
            cmd = 'update-alternatives --install /etc/hadoop-0.20/conf '
            cmd += 'hadoop-0.20-conf %s 50' % self.hadoop_conf
            node.ssh.execute(cmd)
        log.info("Configuring environment...")
        for node in nodes:
            env_file_sh = posixpath.join(self.hadoop_conf, 'hadoop-env.sh')
            node.ssh.remove_lines_from_file(env_file_sh, 'JAVA_HOME')
            env_file = node.ssh.remote_file(env_file_sh, 'a')
            env_file.write('export JAVA_HOME=/usr/lib/jvm/java-6-sun/jre\n')
            env_file.close()
        log.info("Configuring MapReduce Site...")
        for node in nodes:
            mapred_site_xml = posixpath.join(self.hadoop_conf, 'mapred-site.xml')
            mapred_site = node.ssh.remote_file(mapred_site_xml)
            mapred_site.write(mapred_site_templ % cfg)
            mapred_site.close()
        log.info("Configuring Core Site...")
        for node in nodes:
            core_site_xml = posixpath.join(self.hadoop_conf, 'core-site.xml')
            core_site = node.ssh.remote_file(core_site_xml)
            core_site.write(core_site_templ % cfg)
            core_site.close()
        log.info("Configuring HDFS Site...")
        for node in nodes:
            hdfs_site_xml = posixpath.join(self.hadoop_conf, 'hdfs-site.xml')
            hdfs_site = node.ssh.remote_file(hdfs_site_xml)
            hdfs_site.write(hdfs_site_templ % cfg)
            hdfs_site.close()
        log.info("Configuring masters file...")
        for node in nodes:
            masters_file = posixpath.join(self.hadoop_conf, 'masters')
            masters_file = node.ssh.remote_file(masters_file)
            masters_file.write(master.alias)
            masters_file.close()
        log.info("Configuring slaves file...")
        for node in nodes:
            slaves_file = posixpath.join(self.hadoop_conf, 'slaves')
            slaves_file = node.ssh.remote_file(slaves_file)
            slaves_file.write('\n'.join(node_aliases))
            slaves_file.close()
        log.info("Formatting HDFS...")
        for node in nodes:
            self._setup_hadoop_dir(node, self.hadoop_tmpdir, 'hdfs', 'hadoop')
            mapred_dir = posixpath.join(self.hadoop_tmpdir, 'hadoop-mapred')
            self._setup_hadoop_dir(node, mapred_dir, 'mapred', 'hadoop')
            userdir = posixpath.join(self.hadoop_tmpdir, 'hadoop-%s' % user)
            self._setup_hadoop_dir(node, userdir, user, 'hadoop')
            hdfsdir = posixpath.join(self.hadoop_tmpdir, 'hadoop-hdfs')
            if not node.ssh.isdir(hdfsdir):
                node.ssh.execute("su hdfs -c 'hadoop namenode -format'")
            self._setup_hadoop_dir(node, hdfsdir, 'hdfs', 'hadoop')

    def _setup_hadoop_dir(self, node, path, user, group, permission="775"):
        if not node.ssh.isdir(path):
            node.ssh.mkdir(path)
        node.ssh.execute("chown -R %s:hadoop %s" % (user, path))
        node.ssh.execute("chmod -R %s %s" % (permission, path))

    def _start_hadoop(self, master, nodes):
        log.info("Starting namenode...")
        master.ssh.execute('/etc/init.d/hadoop-0.20-namenode restart')
        log.info("Starting secondary namenode...")
        master.ssh.execute('/etc/init.d/hadoop-0.20-secondarynamenode restart')
        for node in nodes:
            log.info("Starting datanode on %s..." % node.alias)
            node.ssh.execute('/etc/init.d/hadoop-0.20-datanode restart')
        log.info("Starting jobtracker...")
        master.ssh.execute('/etc/init.d/hadoop-0.20-jobtracker restart')
        for node in nodes:
            log.info("Starting tasktracker on %s..." % node.alias)
            node.ssh.execute('/etc/init.d/hadoop-0.20-tasktracker restart')

    def run(self, nodes, master, user, user_shell, volumes):
        self._configure_hadoop(master, nodes, user)
        self._start_hadoop(master, nodes)
