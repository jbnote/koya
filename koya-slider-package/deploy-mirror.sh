#! /bin/bash

base_dir=$(dirname $0)
exec $base_dir/deploys-component.sh mirror $@
