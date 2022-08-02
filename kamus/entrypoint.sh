#!/bin/bash

# Used for the Docker deployments

set -eu

# python3 manage.py check --deploy --fail-level WARNING
python3 manage.py collectstatic --no-input --clear

gunicorn kamus.wsgi:application \
	--bind 0.0.0.0:80 \
	--workers=10 \
	--timeout=600 \
	--log-file=- \
	--error-logfile=- \
	--access-logfile=- \
	--capture-output \
	"$@"
