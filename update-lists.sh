#!/bin/sh

USER_AGENT="Mozilla/5.0 (X11; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"

if [ ! -d "/var/www/transmission" ]; then
    mkdir -p /var/www/transmission
fi

# Download lists, unpack and filter, write to gzipped file 
curl -A "$USER_AGENT" -s https://www.iblocklist.com/lists.php \
    | sed -n "s/.*value='\(http:.*\)'.*/\1/p" \
    | sed "s/\&amp;/\&/g" \
    | sed "s/http/\"http/g" \
    | sed "s/gz/gz\"/g" \
    | xargs curl -s -L \
    | gunzip \
    | egrep -v '^#' \
    | gzip - > /var/www/transmission/blocklist.p2p.gz
