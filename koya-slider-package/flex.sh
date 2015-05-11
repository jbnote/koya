#! /bin/bash

APPNAME=${1:-koya}
slider flex $APPNAME --component BROKER0 12 --filesystem hdfs://root
