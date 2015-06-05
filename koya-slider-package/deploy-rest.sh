#! /bin/bash
base_dir=$(dirname $0)
exec $base_dir/deploy-component.sh rest $@
