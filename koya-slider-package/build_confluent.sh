#! /bin/bash

SOURCE=http://packages.confluent.io/archive/1.0/confluent-1.0-2.10.4.tar.gz
TARGET=$HOME/$(basename $SOURCE)
VERSION=$(echo $(basename $SOURCE) | cut -f1,2 -d'-')

CONFIGS="appConfig.json appConfig-mirror.json appConfig-rest.json resources.json resources-mirror.json resources-rest.json"

wget $SOURCE -O $TARGET
mvn clean install -DskipTests -Dkafka.src=$TARGET -Dkafka.version=$VERSION
