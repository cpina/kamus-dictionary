#!/bin/bash

set -eu

arg_1=${1:-}

if [ "$arg_1" = "--quick" ]
then
	docker_compose_options=""
else
	docker_compose_options="--no-cache --pull"
fi

docker-compose build $docker_compose_options && (docker-compose down ; docker-compose up -d)

echo
echo "See logs:"
echo "docker logs kamus-dictionary_kamus_1 --follow"
