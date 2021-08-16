#!/bin/sh

blocklist.py > /dev/stdout
gzip -fk "${OUTPUT_DIR}/blocklist.p2p"
