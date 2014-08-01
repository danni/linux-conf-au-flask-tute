#!/bin/sh

: ${APP_USER:=app}
: ${WEB_CONCURRENCY:=1}
export WEB_CONCURRENCY

if [ "x$(whoami)" != "x$APP_USER" ]; then
    # Call back into ourselves as the app user
    exec sudo -sE -u "$APP_USER" -- "$0" "$@"
else
    . ./python_env/bin/activate
    case "$1" in
        deploy)
            shift 1  # consume command from $@
            ./manage.py db upgrade
            ;;

        serve)
            gunicorn -w "$WEB_CONCURRENCY" \
              -b 0.0.0.0:8000 "webapp:app"
            ;;

        *)
            ./manage.py "$@"
            ;;
    esac
fi
