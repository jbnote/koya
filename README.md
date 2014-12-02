Kafka On YARN (KOYA)
====================

### Goals

  * Use capabilities of YARN for Kafka broker management
  * Automate broker recovery
  * Simplify management tasks (alternative to Kafka command line utilities)
  * Make it easy to deploy, configure and monitor Kafka clusters

JIRA: https://issues.apache.org/jira/browse/KAFKA-1754

Deploy/Run Kafka as YARN application using Slider
-------------------------------------------------

### Prerequisite

1. Checkout slider code (https://github.com/apache/incubator-slider)
2. Create a symbolic link to slider source code folder(ln slider path/to/slider/repo)
3. Download kafka binary package (http://kafka.apache.org/downloads.html)

### Build whole koya package(including slider)

```sh
mvn clean install -DskipTests -Dkafka.src=path/to/kafka_2.10-0.8.1.1.tgz -Dkafka.version=kafka_2.10-0.8.1.1
```

### Build koya slider package only

```sh
cd koya-slider-package
mvn clean install -DskipTests -Dkafka.src=path/to/kafka_2.10-0.8.1.1.tgz -Dkafka.version=kafka_2.10-0.8.1.1
```


