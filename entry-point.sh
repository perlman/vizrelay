#!/bin/sh

set -e

stripQuotes() {
  echo $* | sed -e 's/^"//' -e 's/"$//'
}

export RELAY_CONFIG_JSON=$(stripQuotes $RELAY_CONFIG_JSON)
export RELAY_CONFIG_FILE=$(stripQuotes $RELAY_CONFIG_FILE)

exec "$@"