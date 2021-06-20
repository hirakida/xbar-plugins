#!/bin/bash

PLUGINS_DIR="$HOME"/Library/Application\ Support/xbar/plugins

PLUGINS=(ip.3h.py weather.3h.py)
for plugin in "${PLUGINS[@]}"; do
  ln -fs "$PWD"/plugins/"$plugin" "$PLUGINS_DIR"/
done
