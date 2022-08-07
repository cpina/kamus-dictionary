#!/bin/bash

docker-compose build --no-cache --pull && (docker-compose down ; docker-compose up -d)

echo
echo "See logs:"
echo "docker logs kamus-dictionary_kamus_1 --follow"
