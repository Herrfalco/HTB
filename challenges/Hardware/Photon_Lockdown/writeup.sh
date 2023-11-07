#!/usr/bin/env bash

sudo unsquashfs ONT/rootfs
grep -R "HTB" squashfs-root --exclude-dir=dev 2>/dev/null
