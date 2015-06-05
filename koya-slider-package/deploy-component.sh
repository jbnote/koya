#! /bin/bash

COMPONENT=${1:-""}
APPNAME=${2:-koya}
slider package --install --replacepkg --name KOYA --package target/koya-slider-package-0.1.zip
for action in stop destroy; do
    slider $action ${APPNAME}-${COMPONENT}
done
# Will mirror with source defined in appConfig-mirror.json -- may need customization
unzip -o target/koya-slider-package-0.1.zip appConfig-${COMPONENT}.json resources-${COMPONENT}.json
slider create ${APPNAME}-${COMPONENT} --filesystem hdfs://root --queue dev --template appConfig-${COMPONENT}.json --resources resources-${COMPONENT}.json
