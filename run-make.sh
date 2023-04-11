#!/usr/bin/env bash
#

if [ $# -lt 1 ]
then
	usage="This is a make wrapper that loads env variables from .env, before calling make. Last declared env variable value overrides previous values. Eg: run-make.sh run"
    echo $usage;
	exit -1
fi

pushd .
cd -P -- "$(dirname -- "$0")"


set -o allexport

if [ -f .env ]
then
    source .env
fi

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH

set +o allexport
make $@
popd
