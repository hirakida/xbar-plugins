#!/usr/bin/env bash

PLUGINS_DIR="$HOME/Library/Application Support/xbar/plugins"

for plugin in "$PWD/plugins"/*; do
  ln -fs "$plugin" "$PLUGINS_DIR/"
done
