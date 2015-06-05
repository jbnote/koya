#! /bin/bash

SOURCE=http://packages.confluent.io/archive/1.0/confluent-1.0-2.10.4.tar.gz
TARGET=$HOME/$(basename $SOURCE)
VERSION=$(echo $(basename $SOURCE) | cut -f1,2 -d'-')

wget $SOURCE -O $TARGET
mvn clean install -DskipTests -Dkafka.src=$TARGET -Dkafka.version=$VERSION
unzip -o target/koya-slider-package-0.1.zip appConfig.json appConfig-mirror.json resources.json resources-mirror.json
