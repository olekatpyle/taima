#!/usr/bin/env bash

EXPORT="export PATH=\$PATH:$PWD/src"
SHELL_CONF="$HOME/.bashrc"

if [[ ! -e $SHELL_CONF ]]; then
	touch $SHELL_CONF
fi

if [[ -z $(grep "$EXPORT" "$SHELL_CONF") ]]; then 
	echo $EXPORT >> $SHELL_CONF
fi

echo $EXPORT >> .dollar_path
