#! /bin/bash

SOURCE=http://apache.websitebeheerjd.nl/kafka/0.8.2.1/kafka_2.10-0.8.2.1.tgz
TARGET=$HOME/$(basename $SOURCE)
VERSION=$(basename $TARGET .tgz)

wget $SOURCE -O $TARGET
mvn clean install -DskipTests -Dkafka.src=$TARGET -Dkafka.version=$PREFIX
unzip -o target/koya-slider-package-0.1.zip appConfig.json appConfig-mirror.json resources.json resources-mirror.json
