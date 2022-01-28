#!/usr/bin/env bash

EXPORT="export PATH=\$PATH:$PWD/src"
SHELL_CONF="$HOME/.bashrc"

if [[ ! -e $SHELL_CONF ]]; then
	touch $SHELL_CONF
fi

if [[ -z $(grep "$EXPORT" "$SHELL_CONF") ]]; then 
    echo "#############################################################*" >> $SHELL_CONF
    echo "#                                                             #" >> $SHELL_CONF
    echo "#  Taima hook, to allow for system wide taima program calls   #" >> $SHELL_CONF
    echo "#                                                             #" >> $SHELL_CONF
    echo "#############################################################*" >> $SHELL_CONF
	echo $EXPORT >> $SHELL_CONF
fi
