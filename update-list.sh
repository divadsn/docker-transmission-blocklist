#!/bin/sh

blocklist.py && gzip -fk "${OUTPUT_DIR}/blocklist.p2p"
