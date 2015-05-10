Kafka On YARN (KOYA)
====================

### Goals

  * Use capabilities of YARN for Kafka broker management
  * Automate broker recovery
  * Make it easy to deploy, configure and monitor Kafka clusters
  * Simplify management tasks (alternative to Kafka command line utilities)

JIRA: https://issues.apache.org/jira/browse/KAFKA-1754

Kafka as YARN application using Slider
-----------------------------------------------

### Prerequisite

1. Checkout Slider code (https://github.com/apache/incubator-slider)
2. Create symbolic link to Slider source code (`ln -s /path/to/repo/incubator-slider/ slider`) 
3. Download Kafka binary package (http://kafka.apache.org/downloads.html)

### Build
Ensure the Slider version you checked out matches ${slider.version} in pom.xml
```sh
mvn clean install -DskipTests -Dkafka.src=path/to/kafka_2.10-0.8.1.1.tgz -Dkafka.version=kafka_2.10-0.8.1.1
```
Artifacts:

 - Archive with embedded Slider: __`target/koya-with-slider.zip`__
 - Separate Slider application package: __`target/koya-slider-package-0.1.zip`__

###Installation

####Install Slider

To use the archive with embedded Slider, copy it to the machine from which you launch YARN applications (Hadoop client, gateway or edge node). Extract the file and configure Slider:

If the environment variables `HADOOP_CONF_DIR` or `JAVA_HOME` are not already defined through your Hadoop installation, you can export them in  `slider-0.80.0-incubating/conf/slider-env.sh` 

Example for CDH 5.4:
 
`export HADOOP_CONF_DIR=/etc/hadoop/conf`
`export JAVA_HOME=/usr/java/jdk1.7.0_45-cloudera`

If the registry ZooKeeper quorum was not already configured through Hadoop, modify `slider-0.80.0-incubating/conf/slider-client.xml`: 
```
  <property>
    <name>hadoop.registry.zk.quorum</name>
    <value>node26:2181,node27:2181,node28:2181</value>
  </property>
```
Above steps are not required with HDP 2.2

More information regarding Slider client configuration refer to http://slider.incubator.apache.org/docs/client-configuration.html

### Configure KOYA application package

Before the Kafka cluster can be launched, the brokers need to be defined. Currently Slider does not support [configuration properties at instance level](https://issues.apache.org/jira/browse/SLIDER-851), therefore each broker has to be configured as a component.

If you use the full archive, the configuration file templates are already in your working directory. Otherwise extract them from the Slider package.

####Configure appConfig.json

Define each broker as component, for example:
```
  "components": {
    "BROKER0": {
    },
    "BROKER1": {
    },
```
Modify required properties in the global section: 
```
    "application.def": "koya-slider-package-0.1.zip",
    "java_home": "/usr/lib/jvm/java-7-oracle/",
    "system_configs": "BROKER-COMMON,BROKER0,BROKER1",
    "package_list": "files/kafka_2.10-0.8.1.1.tgz",

    "site.global.app_root": "${AGENT_WORK_ROOT}/app/install/kafka_2.10-0.8.1.1",
    "site.global.kafka_version": "kafka_2.10-0.8.1.1",
    "site.global.xmx_val": "256m",
    "site.global.xms_val": "128m",

    "site.BROKER0.broker.id": "0",
    "site.BROKER1.broker.id": "1",
    "site.BROKER-COMMON.zookeeper.connect": "127.0.0.1:2181"
```
These settings will be used to configure server.properties and launch Kafka.

####Configure resources.json

Replicate the per broker:
```
  "components" : {
    "BROKER0" : {
      "yarn.role.priority" : "1",
      "yarn.component.instances" : "1",
      "yarn.memory" : "768",
      "yarn.vcores" : "1",
      "yarn.component.placement.policy":"1"
    },
    "BROKER1" : {
      "yarn.role.priority" : "2",
      "yarn.component.instances" : "1",
      "yarn.memory" : "768",
      "yarn.vcores" : "1",
      "yarn.component.placement.policy":"1"
    },
```

####metainfo.xml

This file is part of the package and assumes a maximum of 10 brokers. If you require more, modify [metainfo-default.xml](koya-slider-package/metainfo-default.xml) and specify the --metainfo option with the slider create command when deploying the package.

More information about the application configuration can be found [here](http://slider.incubator.apache.org/docs/configuration/core.html).

### Deploy KOYA Cluster

The Slider application package needs to be copied to the HDFS location that was specified as application.def in appConfig.json:
```
hdfs dfs -copyFromLocal koya-slider-package-0.1.zip /path/in/appConfig
```
Now the KOYA cluster can be deployed and launched:
```
slider-0.80.0-incubating/bin/slider create koya --template ~/koya/appConfig.json  --resources ~/koya/resources.json
```
