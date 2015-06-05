#! /bin/bash

APPNAME=${1:-koya}
slider package --install --replacepkg --name KOYA --package target/koya-slider-package-0.1.zip
for action in stop destroy; do
    slider $action $APPNAME
done
# Will mirror with source defined in appConfig-mirror.json -- may need customization
unzip -o target/koya-slider-package-0.1.zip appConfig.json resources.json
slider create ${APPNAME}-mirror --filesystem hdfs://root --queue dev --template appConfig-mirror.json --resources resources-mirror.json
