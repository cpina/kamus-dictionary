#!/bin/bash

# Used for the Docker deployments

set -eu

mkdir --parents "$PYWIKIBOT_DIR"

cat <<EOT > "$PYWIKIBOT_DIR/user-config.py"
family = 'wiktionary'
mylang = 'en'
user_agent_description = 'Kamus dictionary; https://kamus.pina.cat; carles@pina.cat'
EOT

# python3 manage.py check --deploy --fail-level WARNING
python3 manage.py collectstatic --no-input --clear

/code/wait-for-mysql.sh
python3 manage.py migrate

gunicorn kamus.wsgi:application \
	--bind 0.0.0.0:80 \
	--workers=10 \
	--timeout=600 \
	--log-file=- \
	--error-logfile=/var/log/gunicorn.err \
	--access-logfile=/var/log/gunicorn.log \
	--capture-output \
	"$@"
