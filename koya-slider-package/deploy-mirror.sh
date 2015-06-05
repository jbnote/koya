#! /bin/bash

APPNAME=${1:-koya}
slider package --install --replacepkg --name KOYA --package target/koya-slider-package-0.1.zip
for action in stop destroy; do
    slider $action ${APPNAME}-mirror
done
# Will mirror with source defined in appConfig-mirror.json -- may need customization
slider create ${APPNAME}-mirror --filesystem hdfs://root --queue dev --template appConfig-mirror.json --resources resources-mirror.json
