from    __future__  import  with_statement
from    fabric.api  import  local,  settings,   abort,  run,    cd
from    fabric.contrib.console  import  confirm
from fabric.contrib.files import exists,append,contains
from fabric.operations import *
from    fabric.api  import  *
import  os
import  StringIO
#fab    -D  -H  192.168.33.11   -u  vagrant -i  .vagrant/machines/default/virtualbox/private_key    provision

#export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512M -XX:ReservedCodeCacheSize=512m"
APP_USER_SETTINGS = """
export JAVA_HOME=/usr/lib/jvm/java-8-oracle
export HADOOP_HOME=/usr/local/lib/hadoop
export HADOOP_INSTALL=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export YARN_HOME=$HADOOP_HOME
export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=$HADOOP_COMMON_LIB_NATIVE_DIR"
export PATH=$PATH:/usr/local/lib/hbase/bin
export IPYTHON=1
export MAVEN_OPTS="-Xmx2560M -Xss512M -XX:MaxPermSize=1024M -XX:ReservedCodeCacheSize=512m -XX:+CMSClassUnloadingEnabled -XX:-UseGCOverheadLimit"
export PATH=$PATH:/usr/local/lib/spark/bin
export SPARK_SUBMIT_LIBRARY_PATH=/usr/local/lib/hadoop/lib/native
export SPARK_SUBMIT_CLASSPATH=/usr/local/lib/spark/examples/target/spark-examples_2.11-1.5.1.jar
export HB_LIB=/usr/local/lib/hbase/lib
export SPARK_SUBMIT_CLASSPATH=$SPARK_SUBMIT_CLASSPATH:$HB_LIB/hbase-prefix-tree-0.98.15-hadoop2.jar:$HB_LIB/hbase-protocol-0.98.15-hadoop2.jar:$HB_LIB/hbase-client-0.98.15-hadoop2.jar:$HB_LIB/hbase-common-0.98.15-hadoop2.jar:$HB_LIB/hbase-it-0.98.15-hadoop2.jar
export SPARK_SUBMIT_CLASSPATH=$SPARK_SUBMIT_CLASSPATH:$HB_LIB/hbase-server-0.98.15-hadoop2.jar:$HB_LIB/hbase-common-0.98.15-hadoop2.jar:$HB_LIB/htrace-core-2.04.jar:$HB_LIB/guava-12.0.1.jar
"""

def	provision():
    install_java8()
    create_app_user()
    install_hadoop()
    install_hbase()
    install_spark()
    install_python_modules()
    install_scala_modules()
    start_all()

def start_all():
    with settings(sudo_user='hadoop'):
        sudo("/usr/local/lib/hadoop/sbin/start-dfs.sh", warn_only=True)
        sudo("/usr/local/lib/hadoop/sbin/start-yarn.sh", warn_only=True)
        sudo("/usr/local/lib/hbase/bin/start-hbase.sh", warn_only=True)
        sudo("/usr/local/lib/hbase/bin/hbase-daemon.sh start thrift", warn_only=True)
        #sudo("/usr/local/lib/hbase/bin/local-master-backup.sh start 2 3", warn_only=True)
        #sudo("/usr/local/lib/hbase/bin/local-regionservers.sh start 2 3", warn_only=True)
    
def install_python_modules():
    sudo("apt-get install -y python-pip")
    sudo("easy_install -U pip")
    sudo("pip install ipython")
    sudo("pip install tweepy")
    sudo("pip install happybase")
    
def install_scala_modules():
    sudo("wget www.scala-lang.org/files/archive/scala-2.11.6.deb")
    sudo("dpkg -i scala-2.11.6.deb")
    sudo("apt-get update")
    sudo("apt-get install scala")
    sudo("wget https://bintray.com/artifact/download/sbt/debian/sbt-0.13.9.deb")
    sudo("dpkg -i sbt-0.13.9.deb")
    sudo("apt-get update")
    sudo("apt-get install sbt")
    
def install_spark():
    #sudo("apt-get purge maven maven2 maven3")
    #sudo("apt-add-repository -y ppa:andrei-pozolotin/maven3")
    #sudo("apt-get update")
    #sudo("apt-get install -y maven3")
    
    #sudo("export GOOD_RELEASE='precise'")
    #sudo("export BAD_RELEASE="`lsb_release -cs`"")
    #sudo("cd /etc/apt")
    #sudo("sed -i '/natecarlson\/maven3/d' sources.list")
    #sudo("cd sources.list.d")
    #sudo("rm -f natecarlson-maven3-*.list*")
    #sudo("apt-add-repository -y ppa:natecarlson/maven3")
    #sudo("mv natecarlson-maven3-${BAD_RELEASE}.list natecarlson-maven3-${GOOD_RELEASE}.list")
    #sudo("sed -i "s/${BAD_RELEASE}/${GOOD_RELEASE}/" natecarlson-maven3-${GOOD_RELEASE}.list")
    #sudo("apt-get update")
    
    #sudo("sudo add-apt-repository -y 'deb http://ppa.launchpad.net/natecarlson/maven3/ubuntu precise main'")
    #sudo("sudo apt-get -y update")
    #sudo("sudo apt-get install -y maven3 --force-yes")
    #sudo("export PATH=/usr/share/maven3/bin:$PATH")
    sudo("cd /usr/local")
    sudo("wget http://it.apache.contactlab.it/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz")
    sudo("tar xzvf apache-maven-3.3.3-bin.tar.gz")
    sudo("rm apache-maven-3.3.3-bin.tar.gz")
    sudo("mv apache-maven-3.3.3 /usr/local" )
    #sudo("export PATH=/usr/local/apache-maven-3.3.3/bin:$PATH")
    #sudo("cd")
    #sudo("source .profile")
    sudo("ln -s /usr/local/apache-maven-3.3.3/bin/mvn /usr/bin/mvn")
    
    #sudo("sudo ln -s /usr/bin/mvn3 /usr/bin/mvn")
    #sudo("sudo mvn package")
    
    #sudo("ln -s /usr/share/maven3/bin/mvn /usr/bin/mvn")
    #sudo("apt-get install -y maven")
    if not exists("/usr/local/lib/spark-1.5.1"):
        with cd('/usr/local/lib'):
            if not exists("spark-1.5.1.tgz"):
                sudo("wget http://www.eu.apache.org/dist/spark/spark-1.5.1/spark-1.5.1.tgz")
            sudo("tar -xvf spark-1.5.1.tgz")
            sudo("ln -s spark-1.5.1 spark")
        with cd('/usr/local/lib/spark'):
            sudo('sudo mvn package -Pyarn -Dyarn.version=2.6.1 -Phadoop-2.6 -Dhadoop.version=2.6.1 -Phive -DskipTests')
        with cd('/usr/local/lib'):
            sudo("chown hadoop -R spark-1.5.1")
            sudo("chmod -R u+rw spark-1.5.1")
    
def install_hbase():
    '''
    http://hbase.apache.org/book.h\tml#quickstart
    '''
    if not exists("/usr/local/lib/hbase-0.98.15-hadoop2"):
        with cd('/usr/local/lib'):
            if not exists("hbase-0.98.15-hadoop2-bin.tar.gz"):
                sudo("wget http://www.apache.org/dist/hbase/0.98.15/hbase-0.98.15-hadoop2-bin.tar.gz")
            sudo("tar -xvf hbase-0.98.15-hadoop2-bin.tar.gz")
            sudo("ln -s hbase-0.98.15-hadoop2 hbase")
    with cd("/usr/local/lib/hbase/conf"):
        hbase_site_xml_content= """
        <configuration>
        <property>
          <name>hbase.rootdir</name>
          <value>hdfs://localhost:9000/hbase</value>
        </property>
          <property>
            <name>hbase.zookeeper.property.dataDir</name>
            <value>/home/hadoop/zookeeper</value>
          </property>
          <property>
              <name>hbase.cluster.distributed</name>
              <value>true</value>
          </property>
        </configuration>
        """
        _replace_file_content("hbase-site.xml", hbase_site_xml_content)
    with cd('/usr/local/lib'):
        sudo("chown hadoop -R hbase-0.98.15-hadoop2")
        sudo("chmod -R u+rw hbase-0.98.15-hadoop2")

def install_hadoop():
    '''
    http://tecadmin.net/setup-hadoop-2-4-single-node-cluster-on-linux/
    '''
    _download_hadoop()
    _configure_hadoop()
    
def _download_hadoop():
    if not exists("/usr/local/lib/hadoop-2.6.0"):
        with cd('/usr/local/lib'):
            if not exists("hadoop-2.6.0.tar.gz"):
                sudo("wget http://apache.claz.org/hadoop/common/hadoop-2.6.0/hadoop-2.6.0.tar.gz")
            sudo("tar -xvf hadoop-2.6.0.tar.gz")
            sudo("ln -s hadoop-2.6.0 hadoop")

def _replace_file_content(fname, content):
    fcontent = StringIO.StringIO()
    fcontent.write(content)
    sudo("rm -rf %s" % fname)
    put(fcontent, fname, use_sudo=True)
    fcontent.close()

def _configure_hadoop():
    with cd("/usr/local/lib/hadoop/etc/hadoop"):
        core_site_xml_content= """
        <configuration>
            <property>
              <name>fs.default.name</name>
                <value>hdfs://localhost:9000</value>
            </property>
        </configuration>
        """
        _replace_file_content("core-site.xml", core_site_xml_content)
        
        hdfs_site_xml_content="""
        <configuration>
            <property>
             <name>dfs.replication</name>
             <value>1</value>
            </property>

            <property>
              <name>dfs.name.dir</name>
                <value>file:///home/hadoop/hadoopdata/hdfs/namenode</value>
            </property>

            <property>
              <name>dfs.data.dir</name>
                <value>file:///home/hadoop/hadoopdata/hdfs/datanode</value>
            </property>
        </configuration>
        """
        _replace_file_content("hdfs-site.xml", hdfs_site_xml_content)
        
        mapred_site_xml_content = """
        <configuration>
         <property>
          <name>mapreduce.framework.name</name>
           <value>yarn</value>
         </property>
        </configuration>
        """
        _replace_file_content("mapred-site.xml", mapred_site_xml_content)
        
        yarn_site_xml_content = """
        <configuration>
         <property>
          <name>yarn.nodemanager.aux-services</name>
            <value>mapreduce_shuffle</value>
         </property>
        </configuration>
        """
        _replace_file_content("yarn-site.xml", yarn_site_xml_content)
    with settings(sudo_user='hadoop'):
        sudo("/usr/local/lib/hadoop/bin/hdfs namenode -format -nonInteractive", warn_only=True)     
    with cd('/usr/local/lib'):
        sudo("chown hadoop -R hadoop-2.6.0")
        sudo("chmod -R u+rw hadoop-2.6.0")

    
def create_app_user():
    #sudo("sudo locale-gen UTF-8")
    user_exists = run("id -u hadoop", warn_only=True)
    if user_exists.return_code == 1:
        sudo("useradd hadoop --password hadoop -d /home/hadoop -s /bin/bash")
    if not exists("/home/hadoop/.ssh"):
        sudo("mkdir -p /home/hadoop/.ssh")
        sudo("chown -R hadoop /home/hadoop")
        bash_login_content = """
    if [ -f ~/.bashrc ]; then
        . ~/.bashrc
    fi
    """
    _replace_file_content("/home/hadoop/.bash_login", bash_login_content)
    with settings(sudo_user='hadoop'):
        if not exists('/home/hadoop/.ssh/id_rsa'):
            sudo('ssh-keygen -t rsa -P "" -f /home/hadoop/.ssh/id_rsa')
            sudo("cat /home/hadoop/.ssh/id_rsa.pub >> /home/hadoop/.ssh/authorized_keys")
            sudo("chmod 0600 /home/hadoop/.ssh/authorized_keys")
            sudo("ssh-keyscan -H localhost >> /home/hadoop/.ssh/known_hosts")
            sudo("ssh-keyscan -H 0.0.0.0 >> /home/hadoop/.ssh/known_hosts")
            
        if not exists("/home/hadoop/.bashrc"):
            sudo("touch /home/hadoop/.bashrc")
        if not contains("/home/hadoop/.bashrc", "export HADOOP_HOME=/usr/local/lib/hadoop"):
            append("/home/hadoop/.bashrc", APP_USER_SETTINGS, use_sudo=True)
        
    
def install_java8():
    '''
    http://www.webupd8.org/2014/03/how-to-install-oracle-java-8-in-debian.html
    '''
    java_version = run('java -version',warn_only=True)
    if '1.8' not in java_version:
        print 'java 1.8 not found,  installing'
        sudo('echo  "deb    http://ppa.launchpad.net/webupd8team/java/ubuntu    trusty  main"   |   tee /etc/apt/sources.list.d/webupd8team-java.list')
        sudo('echo  "deb-src    http://ppa.launchpad.net/webupd8team/java/ubuntu    trusty  main"   |   tee -a  /etc/apt/sources.list.d/webupd8team-java.list')
        sudo('apt-key   adv --keyserver hkp://keyserver.ubuntu.com:80   --recv-keys EEA14886')
        sudo('apt-get   update')
        sudo('echo  oracle-java8-installer  shared/accepted-oracle-license-v1-1 select  true    |   sudo    /usr/bin/debconf-set-selections')
        sudo('apt-get   install -y  oracle-java8-installer')
        sudo('sudo  apt-get -y  install oracle-java8-set-default')