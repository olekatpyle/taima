#!/usr/bin/env bash

# Shell routine to remove the PATH edit from the .bashrc. On next login
# the path should be in a state prior to the taima application install.

PATH_FILE="./.dollar_path"
SHELL_CONF="$HOME/.bashrc"

STRING=`cat $PATH_FILE`

grep -v "$STRING" $SHELL_CONF > tmp

cp ./tmp $SHELL_CONF
rm ./tmp
