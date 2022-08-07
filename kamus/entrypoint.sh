#!/bin/bash

# Used for the Docker deployments

set -eu

# TODO: not using yet the configuration but needs
# to exist to make it use it for temporary files
mkdir -p "$PYWIKIBOT_DIR"
touch "$PYWIKIBOT_DIR/user-config.py"
# since we deal with this we add user_agent_description
# (TODO needs testing)
# TODO: move to the config
echo "user_agent_description = Kamus dictionary; https://kamus.pina.cat; carles@pina.cat"

# python3 manage.py check --deploy --fail-level WARNING
python3 manage.py collectstatic --no-input --clear

/code/wait-for-mysql.sh
python3 manage.py migrate

gunicorn kamus.wsgi:application \
	--bind 0.0.0.0:80 \
	--workers=10 \
	--timeout=600 \
	--log-file=- \
	--error-logfile=- \
	--access-logfile=- \
	--capture-output \
	"$@"
